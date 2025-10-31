variable "function_name" {}
variable "lambda_role_arn" {}
variable "filename" {}
variable "source_path" {}
variable "handler" { default = "handler.handler" }
variable "runtime" { default = "python3.11" }
variable "timeout" { default = 10 }
variable "private_subnet_ids" {
  type = list(string)
}
variable "lambda_security_group_id" {}
variable "environment_variables" {
  type    = map(string)
  default = {}
}
