import json
import boto3
from datetime import datetime, timezone, timedelta
from utils.classify import ImageClassifier

s3 = boto3.client("s3")
classifier = ImageClassifier()

def handler(event, context):
    print("=== EVENTO DE S3 ===")
    print(json.dumps(event))

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    event_time_raw = record["eventTime"]  # viene como string ISO 8601: "2025-01-23T18:12:45.456Z"
    
    # Crear URL de acceso directo NO presignada
    image_url = f"https://{bucket}.s3.amazonaws.com/{key}"

    event_time_formatted = format_time(event_time_raw)
    print(f"Imagen subida: {image_url} a las {event_time_formatted}")

    # Descargar imagen desde S3
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    image_bytes = file_obj["Body"].read()

    # Clasificar imagen
    label, confidence = classifier.classify(image_bytes)

    print(f"Clasificación: {label} (confianza: {confidence})")

    return {
        "status": "ok",
        "file": key,
        "clasificacion": label,
        "confianza": confidence
    }

def format_time(event_time_raw):
    # Convertir a datetime con tzinfo=UTC
    event_time_utc = datetime.strptime(
        event_time_raw,
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)

    # Convertir a Colombia (UTC-5)
    colombia_time = event_time_utc.astimezone(timezone(timedelta(hours=-5)))

    # Formatear fecha y hora en Colombia
    event_time_formatted = colombia_time.strftime("%Y-%m-%d %H:%M:%S")
    return event_time_formatted