import os
import cv2

class ModelUnavailableError(RuntimeError):
    pass

DEFAULT_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car",
    "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

class ObjectDetector:
    """MobileNet-SSD Caffe detector. Supply a matching config and weights pair."""
    def __init__(self, config_path, weights_path, labels_path=None):
        self.config_path = config_path
        self.weights_path = weights_path
        self.labels_path = labels_path
        self.net = None
        self.labels = DEFAULT_LABELS
        if labels_path and os.path.isfile(labels_path):
            with open(labels_path, encoding="utf-8") as f:
                loaded = [line.strip() for line in f if line.strip()]
            if loaded:
                self.labels = loaded
        if os.path.isfile(config_path) and os.path.isfile(weights_path):
            try:
                self.net = cv2.dnn.readNetFromCaffe(config_path, weights_path)
            except cv2.error:
                self.net = None

    @property
    def available(self):
        return self.net is not None

    def detect(self, image, threshold=0.80):
        if self.net is None:
            raise ModelUnavailableError(
                "Object-detection model files are missing or incompatible. Read models/README.md and place the matching MobileNet-SSD configuration and weights in the models folder."
            )
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
                                     (300, 300), 127.5)
        self.net.setInput(blob)
        output = self.net.forward()
        annotated = image.copy()
        detections = []
        for i in range(output.shape[2]):
            confidence = float(output[0, 0, i, 2])
            if confidence < threshold:
                continue
            class_id = int(output[0, 0, i, 1])
            if class_id < 0 or class_id >= len(self.labels):
                continue
            box = output[0, 0, i, 3:7] * [width, height, width, height]
            x1, y1, x2, y2 = [int(v) for v in box]
            x1, y1 = max(0, min(width - 1, x1)), max(0, min(height - 1, y1))
            x2, y2 = max(x1, min(width - 1, x2)), max(y1, min(height - 1, y2))
            label = self.labels[class_id]
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (30, 120, 230), 2)
            cv2.putText(annotated, f"{label} {confidence:.0%}", (x1, max(20, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (30, 120, 230), 2)
            detections.append({
                "label": label, "confidence": round(confidence, 4),
                "box": {"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1}
            })
        return annotated, detections
