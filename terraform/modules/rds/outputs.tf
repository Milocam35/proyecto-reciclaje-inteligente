output "rds_endpoint" {
  description = "Endpoint del RDS"
  value       = aws_db_instance.this.endpoint
}

output "rds_id" {
  description = "ID de la instancia RDS"
  value       = aws_db_instance.this.id
}

