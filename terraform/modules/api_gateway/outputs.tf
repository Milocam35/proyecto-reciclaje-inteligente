output "api_id" {
  value = aws_apigatewayv2_api.this.id
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.this.api_endpoint
}

output "routes" {
  value = [for r in var.routes : r.route_key]
}

output "integrations" {
  description = "Map of route_key => integration_id"
  value       = { for k, v in aws_apigatewayv2_integration.lambda_integration : k => v.id }
}

