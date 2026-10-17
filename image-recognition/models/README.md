# Object detection model setup

This application uses OpenCV's Caffe MobileNet-SSD interface. Model configuration and weights must be a compatible pair. This ZIP intentionally does not contain model weights.

Expected files:
- `MobileNetSSD_deploy.prototxt` — network configuration
- `MobileNetSSD_deploy.caffemodel` — matching pretrained weights
- `labels.txt` — one class label per line in the exact class-ID order expected by the selected model

A commonly referenced MobileNet-SSD Caffe model uses the 21 Pascal VOC labels in `services/object_detection_service.py`. Do not mix these labels with a model trained on a different dataset or class ordering. Obtain the model files from a documented, trustworthy repository, review its license, and record the exact source/version here before use.

After adding the files, restart Flask and open `/health`. The `detection_model_available` field should be `true`. If it is `false`, the app reports a setup message instead of returning fabricated detections.
