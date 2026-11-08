import os

from fastapi.testclient import TestClient
from socratic_ai_tutor.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200

def test_tutor():
    image_path = os.path.join(os.path.dirname(__file__), "test_problem.jpg")
    with open(image_path, "rb") as f:
        files = {"file": ("test_problem.jpg", f.read(), "image/jpeg")}

    response = client.post("/tutor/start", files=files)

    output_path = os.path.join(os.path.dirname(__file__), "ai_output.md")
    with open(output_path, "w") as f:
        f.write(response.text)
    
    assert response.status_code == 200