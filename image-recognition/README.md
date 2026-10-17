# DecodeLabs Project 4 — Image Recognition (Object Detection)

A beginner-friendly Flask web application that detects supported objects in uploaded images using a pretrained MobileNet-SSD model and OpenCV DNN.

This is an educational project. Results can be incorrect and should be verified. The model only detects the object classes it supports.

## Features
- Upload and preview an image
- Supports PNG, JPG, JPEG, BMP, and WEBP
- 10 MB upload size limit
- Object labels and confidence scores
- Annotated output image with bounding boxes
- Bounding-box coordinates in a results table
- Adjustable confidence threshold (default 80%)
- Clear errors when model files are missing or incompatible

## Technology
Python, Flask, OpenCV, NumPy, Pillow, HTML, CSS, JavaScript, and Bootstrap.

## Folder structure
```text
image-text-recognition/
├── app.py
├── config.py
├── requirements.txt
├── services/
│   ├── __init__.py
│   ├── preprocessing_service.py
│   └── object_detection_service.py
├── models/
│   └── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── detection.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── uploads/
├── outputs/
└── tests/
```

## Setup on Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Model files required
The model weights are not bundled in this ZIP. Put a compatible MobileNet-SSD Caffe model pair in `models/` with these exact names:
- `MobileNetSSD_deploy.prototxt`
- `MobileNetSSD_deploy.caffemodel`

Review `models/README.md` for notes on selecting compatible files and labels. Do not rename unrelated model files and assume they are compatible. The `labels.txt` file is optional depending on the detector implementation.

## Run
```powershell
python app.py
```
Open http://127.0.0.1:5000.

## API endpoints
- `GET /` — home page
- `GET /detection` — object detection page
- `POST /api/detection` — image upload and object detection
- `GET /health` — app and model status

## Tests
Run:
```powershell
pytest -q
```

## Limitations
- This is not a universal object recognizer.
- Accuracy depends on the image and supported model classes.
- Confidence scores are model estimates, not guarantees.
- Model files must be obtained separately and their licensing checked.
- Image processing is performed locally; no cloud AI API is used.
