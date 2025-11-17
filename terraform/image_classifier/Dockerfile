# Imagen base oficial de AWS Lambda para Python 3.11
#Instrucciones para construir y subir la imagen a ECR:
# 2. Build SIN usar buildx (esto evita el image index)
#docker build --platform linux/amd64 \
#  -t reciclaje-inteligente-image-classifier:latest \
#  .
#
# 3. Tag
#docker tag reciclaje-inteligente-image-classifier:latest \
#  670018058027.dkr.ecr.us-east-1.amazonaws.com/reciclaje-inteligente-image-classifier:latest

# 4. Login a ECR
#aws ecr get-login-password --region us-east-1 | \
#  docker login --username AWS --password-stdin \
#  670018058027.dkr.ecr.us-east-1.amazonaws.com

# 5. Push
#docker push 670018058027.dkr.ecr.us-east-1.amazonaws.com/reciclaje-inteligente-image-classifier:latest
FROM public.ecr.aws/lambda/python:3.11

# Define directorio de trabajo
WORKDIR /var/task

# Copiar requirements primero para usar cache
COPY requirements.txt .

# Instalar dependencias - REMOVER el flag --platform
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    --only-binary=:all: \
    -r requirements.txt

# Copiar todo el código
COPY . .

# Comando de handler para Lambda
CMD ["handler.handler"]