resource "aws_s3_bucket" "this" {
  bucket        = "${var.project_name}-catimages"
  force_destroy = true
  tags = {
    Name = "${var.project_name}-catimages"
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


