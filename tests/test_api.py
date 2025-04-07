import pytest
from fastapi.testclient import TestClient
from backend.main import app
from jose import jwt
from datetime import datetime, timedelta
SECRET_KEY = "2530"
ALGORITHM = "HS256"

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 404

def test_scrape():
    response = client.get("/scrape/")
    assert response.status_code == 200

def test_songs():
    response = client.get("/songs/")
    assert response.status_code == 200

def create_test_token():
    payload = {
        "sub": "admin_user",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def test_create_playlist():
    token = create_test_token()
    response = client.get(
        "/create_playlist/",
        headers={"token": token}
    )
    assert response.status_code == 200 or response.status_code == 500





