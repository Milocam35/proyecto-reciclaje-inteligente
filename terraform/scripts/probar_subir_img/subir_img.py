import requests
import json

# === 1️⃣ Endpoint correcto ===
GENERATE_URL_ENDPOINT = "https://rdn6x8ojtd.execute-api.us-east-1.amazonaws.com/generate-url"

# === 2️⃣ Pedir la URL prefirmada ===
payload = {"filename": "organico.jpg"}
headers = {"Content-Type": "application/json"}

response = requests.post(GENERATE_URL_ENDPOINT, json=payload, headers=headers)

print("🔹 Status:", response.status_code)
print("🔹 Respuesta:", response.text)

if response.status_code != 200:
    raise Exception("Error al generar la URL prefirmada")

data = response.json()
upload_url = data.get("upload_url")

if not upload_url:
    raise ValueError("No se encontró el campo con la URL prefirmada en la respuesta")

print("✅ URL prefirmada obtenida:")
print(upload_url)

# === 3️⃣ Subir la imagen a la URL prefirmada ===
image_path = "scripts/probar_subir_img/organico.jpg"

with open(image_path, "rb") as f:
    upload_response = requests.put(upload_url, data=f, headers={"Content-Type": "image/jpeg"})

print("🔹 Respuesta de subida:", upload_response.status_code)

if upload_response.status_code in [200, 201]:
    print("✅ Imagen subida correctamente a S3")
else:
    print("❌ Error al subir la imagen:", upload_response.text)
