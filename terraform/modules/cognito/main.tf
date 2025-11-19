# ============================
# COGNITO USER POOL
# ============================
resource "aws_cognito_user_pool" "this" {
  name = "${var.project_name}-userpool"

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  # Atributo estándar: nombre
  schema {
    name                = "name"
    attribute_data_type = "String"
    mutable             = true
    required            = false
  }

  schema {
    name                = "usuario"
    attribute_data_type = "String"
    mutable             = true
    required            = false

    string_attribute_constraints {
      min_length = 1
      max_length = 30
    }
  }
}

# ============================
# CLIENTE DEL USER POOL
# ============================
resource "aws_cognito_user_pool_client" "client" {
  name         = "${var.project_name}-client"
  user_pool_id = aws_cognito_user_pool.this.id

  generate_secret = false

  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["openid", "email", "profile"]

  callback_urls = var.callback_urls
  logout_urls   = var.logout_urls

  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]
}

# ============================
# DOMINIO PUBLICO DE COGNITO
# ============================
resource "aws_cognito_user_pool_domain" "domain" {
  domain       = "${var.project_name}-auth"
  user_pool_id = aws_cognito_user_pool.this.id
}

# ============================
# USUARIO ADMIN
# ============================
resource "aws_cognito_user" "admin" {
  depends_on  = [aws_cognito_user_pool.this]

  user_pool_id = aws_cognito_user_pool.this.id
  username     = var.admin_email

  attributes = {
    email           = var.admin_email
    email_verified  = true
    name            = var.admin_name
    "custom:usuario" = var.admin_username
  }

  message_action = "SUPPRESS"
}

# ============================
# CONTRASEÑA PERMANENTE CON AWS CLI
# ============================
resource "null_resource" "admin_set_password" {
  depends_on = [
    aws_cognito_user.admin,
    aws_cognito_user_pool_client.client
  ]

  triggers = {
    user_pool_id = aws_cognito_user_pool.this.id
    username     = var.admin_email
    password     = var.admin_password
  }

  provisioner "local-exec" {
    command = <<EOT
aws cognito-idp admin-set-user-password \
  --user-pool-id ${aws_cognito_user_pool.this.id} \
  --username ${var.admin_email} \
  --password '${var.admin_password}' \
  --permanent
EOT
  }
}
