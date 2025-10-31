output "vpc_id" {
  value       = aws_vpc.this.id
  description = "ID de la VPC principal"
}

output "private_subnet_ids" {
  value       = [aws_subnet.private_a.id, aws_subnet.private_b.id]
  description = "IDs de las subnets privadas"
}

output "public_subnet_ids" {
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
  description = "IDs de las subnets públicas"
}

output "rds_security_group_id" {
  value       = aws_security_group.rds_sg.id
  description = "Security Group ID para RDS"
}

output "lambda_security_group_id" {
  value       = aws_security_group.lambda_sg.id
  description = "Security Group ID para Lambdas"
}

output "nat_gateway_ids" {
  value       = [aws_nat_gateway.nat_a.id]
  description = "IDs de los NAT Gateway"
}
