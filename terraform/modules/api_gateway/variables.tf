variable "project_name" {
  description = "Nombre del proyecto o prefijo para los recursos"
  type        = string
}

variable "routes" {
  description = <<EOT
Lista de rutas a crear. Cada elemento debe tener:
- route_key: ejemplo "POST /generate-url"
- lambda_arn: ARN del Lambda a invocar
- statement_id: (opcional) ID personalizado para el permiso de Lambda
EOT
  type = list(object({
    route_key    = string
    lambda_arn   = string
    statement_id = optional(string)
  }))
}

variable "stage_name" {
  description = "Nombre del stage del API (por defecto $default)"
  type        = string
  default     = "$default"
}
