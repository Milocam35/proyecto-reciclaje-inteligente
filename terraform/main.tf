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


# --- S3 Bucket ---

module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.project_name}-bucket"
  project_name = var.project_name
  environment = var.environment
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
  filename                 = "${path.root}/dist/lambda_db_init.zip"
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
  filename                 = "${path.root}/dist/consult_db.zip"
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
  filename                  = "${path.root}/dist/events.zip" #dependencias
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

  environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}


# --- Lambda para manejar stats ---
module "stats_handler" {
  source = "./modules/lambda"
  function_name            = "${var.project_name}-lambda-stats-handler"
  lambda_role_arn           = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  source_path               = "${path.root}/lambdas/stats"
  filename                  = "${path.root}/dist/stats.zip" #dependencias
  private_subnet_ids        = module.vpc.private_subnet_ids
  lambda_security_group_id  = module.vpc.lambda_security_group_id

  environment_variables = {
    DB_HOST = module.rds.rds_endpoint
    DB_USER = var.db_username
    DB_PASS = var.db_password
    DB_NAME = var.db_name
  }
}


# --- ECR para la imagen de la Lambda de clasificacion ---
module "ecr" {
  source       = "./modules/ecr"
  project_name = var.project_name
}

# --- Lambda para clasificacion de imagenes que usa imagen desde ECR ---

resource "aws_lambda_function" "image_classifier" {
  function_name = "${var.project_name}-lambda-image-classifier"

  package_type  = "Image"
  image_uri     = "${module.ecr.ecr_repository_url}:latest"

  architectures = ["x86_64"]

  role = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"

  # TensorFlow completo con TFLite - balance entre recursos
  timeout = 900        # 15 minutos
  memory_size = 2048   # 2GB

  ephemeral_storage {
    size = 1024  # 1GB
  }

  environment {
    variables = {
      BUCKET_NAME           = module.s3_bucket.bucket_name
      DB_HOST               = module.rds.rds_endpoint
      DB_USER               = var.db_username
      DB_PASS               = var.db_password
      DB_NAME               = var.db_name
      # Optimizaciones de TensorFlow
      TF_CPP_MIN_LOG_LEVEL  = "2"         # Reducir logs
      TF_ENABLE_ONEDNN_OPTS = "0"         # Desactivar optimizaciones innecesarias
      PYTHONUNBUFFERED      = "1"
      API_GATEWAY_URL       = "https://rdn6x8ojtd.execute-api.us-east-1.amazonaws.com/events"
    }
  }

  vpc_config {
    subnet_ids         = module.vpc.private_subnet_ids
    security_group_ids = [module.vpc.lambda_security_group_id]
  }
}


resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3InvokeClassifier"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_classifier.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3_bucket.bucket_arn
}

resource "aws_s3_bucket_notification" "notify_lambda" {
  bucket = module.s3_bucket.bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.image_classifier.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "uploads/"
    filter_suffix       = ".jpg"
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
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
    },
    {
      route_key  = "GET /events" #endpoint para listar eventos
      lambda_arn = module.events_handler.lambda_arn
      statement_id = "AllowInvoke-GET-events"
    },
    {
      route_key  = "GET /events/{id}" #endpoint para obtener un evento por ID
      lambda_arn = module.events_handler.lambda_arn
      statement_id = "AllowInvoke-GET-events-id"
    },
    {
      route_key  = "PUT /events/{id}/tipo" #endpoint para actualizar el tipo real de un evento
      lambda_arn = module.events_handler.lambda_arn
      statement_id = "AllowInvoke-PUT-events-id-tipo"
    },
    {
      route_key  = "DELETE /events/{id}" #endpoint para eliminar un evento por ID
      lambda_arn = module.events_handler.lambda_arn
      statement_id = "AllowInvoke-DELETE-events-id"
    },
    {

      route_key  = "POST /stats" #endpoint para calcular stats
      lambda_arn = module.stats_handler.lambda_arn
      statement_id = "AllowInvoke-POST-stats"
    },
    {
      route_key  = "GET /stats" #endpoint para obtener todas las stats
      lambda_arn = module.stats_handler.lambda_arn
      statement_id = "AllowInvoke-GET-stats"
    },
    {
      route_key  = "GET /stats/{id}" #endpoint para obtener un stat por ID
      lambda_arn = module.stats_handler.lambda_arn
      statement_id = "AllowInvoke-GET-stats-id"
    }
  ]
}
