variable "project_name" {}
variable "admin_email" {}
variable "admin_password" { sensitive = true }
variable "admin_name" {}
variable "admin_username" {}

variable "callback_urls" {
  type = list(string)
}

variable "logout_urls" {
  type = list(string)
}


