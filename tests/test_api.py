import pytest
from fastapi.testclient import TestClient
from backend.main import app

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

def test_create_playlist():
    response = client.get("/create_playlist/")
    assert response.status_code == 200





