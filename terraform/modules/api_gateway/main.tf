# --- Crear la API HTTP ---
resource "aws_apigatewayv2_api" "this" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
}

# --- Integraciones dinámicas con Lambdas ---
resource "aws_apigatewayv2_integration" "lambda_integration" {
  for_each = { for r in var.routes : r.route_key => r }

  api_id           = aws_apigatewayv2_api.this.id
  integration_type = "AWS_PROXY"
  integration_uri  = each.value.lambda_arn
}

# --- Rutas dinámicas ---
resource "aws_apigatewayv2_route" "lambda_routes" {
  for_each = aws_apigatewayv2_integration.lambda_integration

  api_id    = aws_apigatewayv2_api.this.id
  route_key = each.key
  target    = "integrations/${each.value.id}"
}

# --- Stage ---
resource "aws_apigatewayv2_stage" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = var.stage_name
  auto_deploy = true
}

# --- Permisos para invocar Lambdas ---
resource "aws_lambda_permission" "allow_invoke" {
  for_each = { for r in var.routes : r.route_key => r }

  statement_id  = try(each.value.statement_id, "AllowInvoke-${replace(replace(each.key, "/", "-"), " ", "-")}")
  action        = "lambda:InvokeFunction"
  function_name = each.value.lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/*/*"
}
