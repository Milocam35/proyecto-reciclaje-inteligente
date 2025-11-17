#!/bin/bash
set -e

IMAGE_NAME="reciclaje-inteligente-image-classifier"
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$IMAGE_NAME"

echo "=========================================="
echo "🚀 Deploy Lambda Image Classifier"
echo "=========================================="

# Verificar que existe el directorio
if [ ! -d "./image_classifier" ]; then
    echo "❌ Error: directorio ./image_classifier no encontrado"
    exit 1
fi

# Verificar que existe el modelo
if [ ! -f "./image_classifier/model/model_fp16.tflite" ]; then
    echo "⚠️  Warning: modelo model_fp16.tflite no encontrado"
    echo "   Verificando en ./image_classifier/model/"
    ls -lh ./image_classifier/model/ || true
fi

echo ""
echo "📋 Información del deploy:"
echo "   Account ID: $ACCOUNT_ID"
echo "   Region: $REGION"
echo "   Repository: $IMAGE_NAME"
echo "   Image URI: $REPO_URI:latest"
echo ""

# 1. Verificar/crear repositorio ECR
echo "🔍 Verificando repositorio ECR..."
aws ecr describe-repositories --repository-names $IMAGE_NAME --region $REGION >/dev/null 2>&1 || {
    echo "📦 Creando repositorio ECR..."
    aws ecr create-repository \
        --repository-name $IMAGE_NAME \
        --region $REGION \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256 >/dev/null
    echo "✅ Repositorio creado"
}

# 2. Login a ECR
echo ""
echo "🔐 Autenticando con ECR..."
aws ecr get-login-password --region $REGION \
    | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# 3. Limpiar imágenes antiguas (opcional - descomenta si quieres)
#echo ""
#echo "🧹 Limpiando imágenes antiguas..."
#aws ecr batch-delete-image \
#    --repository-name $IMAGE_NAME \
#    --region $REGION \
#    --image-ids imageTag=latest >/dev/null 2>&1 || true

# 4. Build imagen
echo ""
echo "🏗️  Construyendo imagen Docker (esto puede tardar varios minutos)..."
echo "   Platform: linux/amd64"
echo "   TensorFlow: 2.15.0"
echo "   Runtime: Python 3.11"
echo ""

docker build \
    --platform linux/amd64 \
    -t $IMAGE_NAME:latest \
    -t $REPO_URI:latest \
    ./image_classifier

# 5. Push a ECR
echo ""
echo "📤 Subiendo imagen a ECR..."
docker push $REPO_URI:latest

# 5. Verificar imagen en ECR
echo ""
echo "✅ Verificando imagen en ECR..."
IMAGE_DIGEST=$(aws ecr describe-images \
    --repository-name $IMAGE_NAME \
    --region $REGION \
    --image-ids imageTag=latest \
    --query 'imageDetails[0].imageDigest' \
    --output text)

IMAGE_SIZE=$(aws ecr describe-images \
    --repository-name $IMAGE_NAME \
    --region $REGION \
    --image-ids imageTag=latest \
    --query 'imageDetails[0].imageSizeInBytes' \
    --output text)

IMAGE_SIZE_MB=$((IMAGE_SIZE / 1024 / 1024))

echo "=========================================="
echo "🎉 ¡Deploy completado exitosamente!"
echo "=========================================="
echo ""
echo "📊 Detalles de la imagen:"
echo "   URI: $REPO_URI:latest"
echo "   Digest: $IMAGE_DIGEST"
echo "   Size: ${IMAGE_SIZE_MB} MB"
echo ""
echo "🔄 Próximos pasos:"
echo "   1. Actualizar Lambda con: terraform apply"
echo "   2. O manualmente con:"
echo "      aws lambda update-function-code \\"
echo "        --function-name reciclaje-inteligente-lambda-image-classifier \\"
echo "        --image-uri $REPO_URI:latest"
echo ""
echo "🧪 Probar Lambda:"
echo "   aws lambda invoke \\"
echo "     --function-name reciclaje-inteligente-lambda-image-classifier \\"
echo "     --payload '{\"image\":{\"url\":\"https://example.com/image.jpg\"}}' \\"
echo "     --cli-binary-format raw-in-base64-out \\"
echo "     response.json"
echo ""
echo "=========================================="