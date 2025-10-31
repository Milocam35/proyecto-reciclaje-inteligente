variable "bucket_name" {
  description = "Nombre del bucket S3"
  type        = string
}

variable "acl" {
  description = "Política de acceso"
  type        = string
  default     = "private"
}

variable "environment" {
  description = "Nombre del entorno (dev, prod)"
  type        = string
}

variable "tags" {
  description = "Tags adicionales para el bucket"
  type        = map(string)
  default     = {}
}
