resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = merge({
    Name        = var.bucket_name
    Environment = var.environment
  }, var.tags)
}

# Opcional: habilita versionado
resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.this.id
  acl    = var.acl
}

# Opcional: habilita versionado
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = "Enabled"
  }
}
