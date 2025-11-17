import json
import boto3
import requests
from datetime import datetime, timezone, timedelta
from utils.classify import ImageClassifier
import os

s3 = boto3.client("s3")
classifier = ImageClassifier()

# URL del API Gateway para enviar eventos
API_GATEWAY_URL = os.environ.get(
    "API_GATEWAY_URL", 
    "https://rdn6x8ojtd.execute-api.us-east-1.amazonaws.com/events"
)

def handler(event, context):
    print("=== EVENTO DE S3 ===")
    print(json.dumps(event))

    try:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        event_time_raw = record["eventTime"]  # "2025-01-23T18:12:45.456Z"
        
        # Crear URL de acceso directo (pública)
        image_url = f"https://{bucket}.s3.amazonaws.com/{key}"
        
        # Formatear hora de sincronización (cuando se subió la imagen)
        hora_sincronizado = format_time(event_time_raw)
        print(f"Imagen subida: {image_url} a las {hora_sincronizado}")

        # Descargar imagen desde S3
        print("Descargando imagen desde S3...")
        file_obj = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = file_obj["Body"].read()
        print(f"Imagen descargada: {len(image_bytes)} bytes")

        # Clasificar imagen
        print("Clasificando imagen...")
        label, confidence = classifier.classify(image_bytes)
        print(f"Clasificación: {label} (confianza: {confidence:.2f}%)")

        # Obtener hora actual de clasificación (hora de Colombia UTC-5)
        hora_clasificado = get_colombia_time()
        print(f"Hora de clasificación: {hora_clasificado}")

        # Calcular duración (diferencia entre clasificación y subida)
        duracion = calculate_duration(event_time_raw, hora_clasificado)
        print(f"Duración del procesamiento: {duracion} segundos")

        # Crear payload del evento
        event_payload = {
            "horaClasificado": hora_clasificado,
            "horaSincronizado": hora_sincronizado,
            "duracion": duracion,
            "rutaImagen": image_url,
            "tipoClasificado": label,
            "confianza": confidence
        }

        print("=== EVENTO A ENVIAR ===")
        print(json.dumps(event_payload, indent=2))

        # Enviar evento al API Gateway
        print(f"Enviando evento a {API_GATEWAY_URL}...")
        response = requests.post(
            API_GATEWAY_URL,
            json=event_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        response.raise_for_status()
        print(f"✅ Evento enviado exitosamente. Status: {response.status_code}")
        print(f"Respuesta: {response.text}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "ok",
                "file": key,
                "clasificacion": label,
                "confianza": round(confidence * 100, 1),
                "evento_enviado": True,
                "api_response": response.json() if response.text else None
            })
        }

    except Exception as e:
        print(f"❌ Error en el handler: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            })
        }


def format_time(event_time_raw):
    """
    Convierte el tiempo UTC del evento de S3 a hora de Colombia (UTC-5)
    Input: "2025-01-23T18:12:45.456Z"
    Output: "2025-01-23 13:12:45"
    """
    # Convertir a datetime con tzinfo=UTC
    event_time_utc = datetime.strptime(
        event_time_raw,
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)

    # Convertir a Colombia (UTC-5)
    colombia_time = event_time_utc.astimezone(timezone(timedelta(hours=-5)))

    # Formatear: "YYYY-MM-DD HH:MM:SS"
    return colombia_time.strftime("%Y-%m-%d %H:%M:%S")


def get_colombia_time():
    """
    Obtiene la hora actual en Colombia (UTC-5)
    Output: "2025-01-23 13:15:30"
    """
    # Hora actual en UTC
    now_utc = datetime.now(timezone.utc)
    
    # Convertir a Colombia (UTC-5)
    colombia_time = now_utc.astimezone(timezone(timedelta(hours=-5)))
    
    # Formatear: "YYYY-MM-DD HH:MM:SS"
    return colombia_time.strftime("%Y-%m-%d %H:%M:%S")


def calculate_duration(event_time_raw, hora_clasificado):
    """
    Calcula la duración en segundos entre la subida y la clasificación
    """
    # Parsear hora de subida (UTC)
    event_time_utc = datetime.strptime(
        event_time_raw,
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)
    
    # Parsear hora de clasificación (Colombia UTC-5)
    clasificado_time = datetime.strptime(
        hora_clasificado,
        "%Y-%m-%d %H:%M:%S"
    ).replace(tzinfo=timezone(timedelta(hours=-5)))
    
    # Calcular diferencia en segundos
    duration = (clasificado_time - event_time_utc).total_seconds()
    
    return round(duration, 1)