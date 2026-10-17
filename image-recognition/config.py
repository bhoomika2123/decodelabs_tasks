import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "local-development-key-change-me")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
    MODEL_CONFIG = os.path.join(BASE_DIR, "models", "MobileNetSSD_deploy.prototxt")
    MODEL_WEIGHTS = os.path.join(BASE_DIR, "models", "MobileNetSSD_deploy.caffemodel")
    MODEL_LABELS = os.path.join(BASE_DIR, "models", "labels.txt")
