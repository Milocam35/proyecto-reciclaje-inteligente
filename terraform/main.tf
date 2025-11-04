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
    DB_NAME = "reciclaje_db"
  }
}

data "aws_caller_identity" "current" {}


module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.project_name}-bucket"
  environment = var.environment
  tags        = {
    Project = var.project_name
  }
}
