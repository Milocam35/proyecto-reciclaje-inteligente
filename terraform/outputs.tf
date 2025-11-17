output "bucket_name" {
  value = module.s3_bucket.bucket_name
}

output "bucket_arn" {
  value = module.s3_bucket.bucket_arn
}

output "rds_endpoint" {
  value       = module.rds.rds_endpoint
  description = "Endpoint del RDS desde el módulo"
}

output "rds_id" {
  value       = module.rds.rds_id
  description = "ID del RDS desde el módulo"
}


output "api_endpoint" {
  value = module.api_gateway.api_endpoint
}

output "ecr_repository_url" {
  value = module.ecr.ecr_repository_url
}
