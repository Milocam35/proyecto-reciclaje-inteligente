terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# --- VPC ---
module "vpc" {
  source           = "./modules/vpc"
  region           = var.region
  project_name     = var.project_name
  cidr_block       = "10.0.0.0/16"
  private_subnet_a = "10.0.1.0/24"
  private_subnet_b = "10.0.2.0/24"
  public_subnet_a  = "10.0.3.0/24"
  public_subnet_b  = "10.0.4.0/24"
}

# --- RDS ---
module "rds" {
  source            = "./modules/rds"
  project_name      = var.project_name
  username          = var.db_username
  password          = var.db_password
  subnet_ids        = module.vpc.private_subnet_ids
  rds_security_group_id = module.vpc.rds_security_group_id 
}



# --- lambda testear db privada ---
module "lambda_test_db" {
  source                   = "./modules/lambda"
  function_name             = "${var.project_name}-lambda-test-db"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/test_db"
  filename                  = "${path.root}/dist/test_db.zip"
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

  environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}

data "aws_caller_identity" "current" {}


# --- lambda init db

# --- Crea la Lambda usando tu módulo genérico ---
module "lambda_db_init" {
  source = "./modules/lambda"
  function_name            = "${var.project_name}-lambda-db-init"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/lambda_db_init"
  filename                 = "${path.module}/dist/lambda_db_init.zip"
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

   environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}

# --- Lambda para consultar la base de datos ---
module "consult_db" {
  source = "./modules/lambda"
  function_name            = "${var.project_name}-lambda-consult-db"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/consult_db"
  filename                 = "${path.module}/dist/consult_db.zip"
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

   environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}

# --- Lambda para generar URL pre-firmadas ---
module "generate_presigned_url" {
  source = "./modules/lambda"
  function_name            = "${var.project_name}-lambda-generate-presigned-url"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/generate_presigned_url"
  filename                 = "${path.module}/dist/generate_presigned_url.zip"
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

   environment_variables = {
    BUCKET_NAME = module.s3_bucket.bucket_name
  }
}

# --- Lambda para manejar eventos ---
module "events_handler" {
  source = "./modules/lambda"
  function_name            = "${var.project_name}-lambda-events-handler"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/events"
  filename                  = "${path.root}/dist/events.zip"
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

  environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}

# --- API Gateway que expone la Lambda ---
module "api_gateway" {
  source       = "./modules/api_gateway"
  project_name = "reciclaje-inteligente"

  routes = [
    {
      route_key  = "POST /generate-url"  # La ruta real en API Gateway mantiene el formato con /
      lambda_arn = module.generate_presigned_url.lambda_arn
      statement_id = "AllowInvoke-POST-generate-url"  # ID sin caracteres especiales
    },
    {
      route_key  = "POST /events" #endpoint para crear un evento
      lambda_arn = module.events_handler.lambda_arn
      statement_id = "AllowInvoke-POST-events"
    }
  ]
}

# --- S3 Bucket ---

module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.project_name}-bucket"
  project_name = var.project_name
  environment = var.environment
}
