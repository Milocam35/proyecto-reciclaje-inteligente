# Subnet group (para permitir RDS en las subnets privadas)
resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# Instancia RDS privada con MySQL
resource "aws_db_instance" "this" {
  identifier              = "${var.project_name}-rds"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  db_name                 = var.db_name
  username                = var.username
  password                = var.password
  vpc_security_group_ids  = [var.security_group_id]
  db_subnet_group_name    = aws_db_subnet_group.this.name

  publicly_accessible     = false       # 🔒 Privada
  skip_final_snapshot     = true
  deletion_protection     = false
  backup_retention_period = 1
  multi_az                = false

  tags = {
    Name = "${var.project_name}-rds"
  }
}
