import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_expand_acronyms():
    response = client.post(
        "/expand",
        json={"message": "FYI, LOL!"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "For your information, Laugh out loud!"
    }

def test_invalid_input():
    response = client.post(
        "/expand",
        json={"invalid_key": "test"}
    )
    assert response.status_code == 422  # Validation error
    assert response.json() == {
        "detail": "Message text is required"
    }

