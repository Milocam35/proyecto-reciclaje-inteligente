resource "aws_ecr_repository" "image_classifier_repo" {
  name = "${var.project_name}-image-classifier"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.image_classifier_repo.repository_url
}
