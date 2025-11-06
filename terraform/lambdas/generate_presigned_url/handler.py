import boto3
import os
import json
from datetime import datetime
import uuid

s3 = boto3.client("s3")
BUCKET = os.environ["BUCKET_NAME"]

def handler(event, context):
    try:
        # Carpeta por fecha: uploads/YYYY/MM/DD/
        date_path = datetime.now().strftime("uploads/%Y/%m/%d")
        filename = f"{date_path}/{uuid.uuid4()}.jpg"

        url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET,
                "Key": filename,
                "ContentType": "image/jpeg"
            },
            ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "upload_url": url,
                "object_key": filename
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
