import numpy as np
from PIL import Image
import io

IMG_SIZE = (224, 224)

def load_and_preprocess_image(image_bytes):
    """Carga y preprocesa una imagen desde bytes (archivo S3)."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0).astype("float32")  # importante para TFLite

