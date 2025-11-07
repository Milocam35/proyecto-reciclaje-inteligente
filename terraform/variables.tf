variable "region" {
  description = "Región AWS"
  type        = string
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno actual (dev/prod)"
  type        = string
}

variable "db_username" { type = string }
variable "db_password" { type = string }
variable "db_name" { type = string }



