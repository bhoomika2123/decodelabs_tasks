import os
import base64
from flask import Flask, render_template, request, jsonify
from config import Config
from services.preprocessing_service import load_image, image_to_png_bytes
from services.object_detection_service import ObjectDetector, ModelUnavailableError

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

detector = ObjectDetector(
    app.config["MODEL_CONFIG"],
    app.config["MODEL_WEIGHTS"],
    app.config["MODEL_LABELS"],
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}


def valid_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_upload():
    if "image" not in request.files:
        return None, (jsonify(success=False, message="Please choose an image."), 400)
    file = request.files["image"]
    if not file or not file.filename:
        return None, (jsonify(success=False, message="No image was selected."), 400)
    if not valid_extension(file.filename):
        return None, (jsonify(success=False, message="Unsupported file type. Use PNG, JPG, JPEG, BMP, or WEBP."), 415)
    data = file.read()
    if not data:
        return None, (jsonify(success=False, message="The uploaded file is empty."), 400)
    if len(data) > app.config["MAX_CONTENT_LENGTH"]:
        return None, (jsonify(success=False, message="Image exceeds the 10 MB upload limit."), 413)
    try:
        image = load_image(data)
    except ValueError as exc:
        return None, (jsonify(success=False, message=str(exc)), 400)
    return (data, image), None


@app.errorhandler(413)
def too_large(_error):
    return jsonify(success=False, message="Image exceeds the 10 MB upload limit."), 413


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/detection")
def detection_page():
    return render_template("detection.html")


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        app="Image Recognition",
        detection_model_available=detector.available,
    )


@app.post("/api/detection")
def detection_api():
    upload, error = read_upload()
    if error:
        return error
    _data, image = upload
    try:
        threshold = float(request.form.get("threshold", "0.80"))
    except ValueError:
        return jsonify(success=False, message="Confidence threshold must be a number."), 400
    if not 0.30 <= threshold <= 0.95:
        return jsonify(success=False, message="Confidence threshold must be between 0.30 and 0.95."), 400
    try:
        annotated, detections = detector.detect(image, threshold)
        encoded = image_to_png_bytes(annotated)
        return jsonify(
            success=True,
            detections=detections,
            count=len(detections),
            threshold=threshold,
            annotated_image="data:image/png;base64," + base64.b64encode(encoded).decode(),
            message="Object detection completed." if detections else
                    "No objects passed the selected confidence threshold.",
        )
    except ModelUnavailableError as exc:
        return jsonify(success=False, message=str(exc)), 503
    except Exception:
        app.logger.exception("Object detection failed")
        return jsonify(
            success=False,
            message="Object detection failed. Check the model files and try again.",
        ), 500


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
