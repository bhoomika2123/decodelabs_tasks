from app import app, detector

def test_health_endpoint():
    app.config["TESTING"] = True
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert "detection_model_available" in response.json

def test_missing_model_fails_gracefully():
    # Model files are intentionally external; API should return a useful setup message.
    if not detector.available:
        import io
        response = app.test_client().post("/api/detection",
            data={"image": (io.BytesIO(b""), "empty.jpg")}, content_type="multipart/form-data")
        assert response.status_code in (400, 413)
