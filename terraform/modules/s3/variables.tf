
variable "bucket_name" {
  description = "Nombre por defecto del bucket S3. Se puede sobrescribir al instanciar el módulo."
  type        = string
  default     = ""
}

variable "bucket_acl" {
  description = "ACL del bucket S3"
  type        = string
  default     = "private"
}

variable "bucket_tags" {
  description = "Tags por defecto para los buckets S3"
  type        = map(string)
  default     = {}
}

variable "environment" {
  description = "Nombre del entorno (dev, prod)"
  type        = string
  default     = ""
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}
