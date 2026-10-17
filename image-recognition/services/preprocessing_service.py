from io import BytesIO
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

def load_image(data: bytes) -> np.ndarray:
    try:
        pil = Image.open(BytesIO(data))
        pil.verify()
        pil = Image.open(BytesIO(data)).convert("RGB")
        arr = np.array(pil)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError("The uploaded file is not a valid, readable image.")

def image_to_png_bytes(image: np.ndarray) -> bytes:
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode processed image.")
    return encoded.tobytes()
