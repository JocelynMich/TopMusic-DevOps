import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_homepage():
    """Prueba si la raíz de la API devuelve un 404 (o el código esperado)."""
    response = client.get("/")
    assert response.status_code == 404

def test_scrape():
    """Prueba si el endpoint de scraping responde correctamente."""
    response = client.get("/scrape/")
    assert response.status_code == 200
def test_songs():
    """Prueba si el endpoint de songs responde correctamente."""
    response = client.get("/songs/")
    assert response.status_code == 200

def test_create_playlist():
    """Prueba la creación de una playlist en Spotify (sin detalles de autenticación)."""
    response = client.get("/create_playlist/")
    assert response.status_code == 200





