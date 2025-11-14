# Antes de ejecutar el build, asegúrate de tener Docker Buildx configurado para ARM64
# docker buildx create --use --name lambda_builder
# docker buildx inspect --bootstrap

# Imagen base oficial de AWS Lambda para Python (ARM64 recomendado)
FROM public.ecr.aws/lambda/python:3.11-arm64

# Establecer el entorno de trabajo
WORKDIR /var/task

# Copiar requirements y el código
COPY requirements.txt ./

# Instalar dependencias livianas
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (clasificador + utils + modelo)
COPY . .

# Comando de entrada del Lambda Handler
CMD ["handler.lambda_handler"]
