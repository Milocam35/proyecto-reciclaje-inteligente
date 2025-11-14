#!/bin/bash
set -e

IMAGE_NAME="reciclaje-inteligente-image-classifier"
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$IMAGE_NAME"

echo "🚀 [1/5] Verificando repositorio ECR..."

# Crear repo si no existe
aws ecr describe-repositories --repository-names $IMAGE_NAME >/dev/null 2>&1 || \
  aws ecr create-repository --repository-name $IMAGE_NAME >/dev/null

echo "🐳 [2/5] Logeando contra ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $REPO_URI

echo "🔧 [3/5] Habilitando buildx..."
docker buildx create --use --name lambda_builder >/dev/null 2>&1 || docker buildx use lambda_builder
docker buildx inspect --bootstrap

echo "📦 [4/5] Construyendo imagen Docker ARM64..."
docker buildx build \
  --platform linux/arm64 \
  -t $IMAGE_NAME \
  -t $REPO_URI:latest \
  ./image_classifier \
  --push

echo "🎉 [5/5] Imagen subida a ECR exitosamente:"
echo "👉 $REPO_URI:latest"
