resource "aws_ecr_repository" "newrelic_ecr" {
  name                 = "${local.naming_convention}-ecr"
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}

resource "null_resource" "docker_build_push" {
  # ECR Login
  provisioner "local-exec" {
    command = "aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${aws_ecr_repository.newrelic_ecr.repository_url}"
  }

  # Build Image
  provisioner "local-exec" {
    command = "docker build -t ${aws_ecr_repository.newrelic_ecr.repository_url}:latest ../demo-app"
  }

  # Push Image
  provisioner "local-exec" {
    command = "docker push ${aws_ecr_repository.newrelic_ecr.repository_url}:latest"
  }

  depends_on = [aws_ecr_repository.newrelic_ecr]
}
