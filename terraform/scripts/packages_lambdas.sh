#!/bin/bash
set -e

LAMBDAS_DIR="./lambdas"
DIST_DIR="./dist"

echo "📦 Iniciando empaquetado de Lambdas..."
mkdir -p "$DIST_DIR"

for LAMBDA_PATH in "$LAMBDAS_DIR"/*; do
    if [ -d "$LAMBDA_PATH" ]; then
        LAMBDA_NAME=$(basename "$LAMBDA_PATH")
        ZIP_FILE="$DIST_DIR/$LAMBDA_NAME.zip"

        echo "🧩 Empaquetando Lambda: $LAMBDA_NAME"

        # Limpia posibles instalaciones previas
        find "$LAMBDA_PATH" -type d -name "__pycache__" -exec rm -rf {} +
        rm -f "$ZIP_FILE"

        # Instala dependencias dentro de la carpeta de la Lambda
        if [ -f "$LAMBDA_PATH/requirements.txt" ]; then
            echo "   📚 Instalando dependencias..."
            pip install -r "$LAMBDA_PATH/requirements.txt" --target "$LAMBDA_PATH" >/dev/null
        fi

        # Crea el ZIP desde la carpeta raíz de la Lambda
        (cd "$LAMBDA_PATH" && zip -r9 "$(realpath "../../$ZIP_FILE")" . >/dev/null)

        echo "   ✅ Empaquetado: $ZIP_FILE"
    fi
done

echo ""
echo "🎉 Todas las Lambdas han sido empaquetadas exitosamente en la carpeta $DIST_DIR/"
