variable "project_name" {
  type = string
}

variable "username" {
  type = string
}

variable "password" {
  type = string
  sensitive = true
}

variable "db_name" {
  type    = string
  default = "reciclaje_db"
}

variable "subnet_ids" {
  type = list(string)
}

variable "rds_security_group_id" {
  description = "ID del Security Group que permite acceso al RDS"
  type        = string
}
