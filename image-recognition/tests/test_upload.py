import io
from app import app

def test_home_page():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_missing_ocr_upload():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post("/api/ocr", data={})
    assert response.status_code == 400
    assert response.json["success"] is False

def test_invalid_image_content():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post("/api/ocr", data={"image": (io.BytesIO(b"not an image"), "bad.png")}, content_type="multipart/form-data")
    assert response.status_code == 400
