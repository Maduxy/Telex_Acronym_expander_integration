import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_invalid_input():
    response = client.post(
        "/expand",
        json={"invalid_key": "test"}
    )
    assert response.status_code == 500  # Validation error
    assert response.json() == {
        "detail": "Internal Server Error"
    }


def test_expand_endpoint():
    payload = {"message": "LOL, IDK what to do. BRB!"}
    response = client.post("/expand", json=payload)
    assert response.status_code == 200
    
    # Expected modified text based on the acronyms provided above.
    expected_message = "Laugh Out Loud, I Don't Know what to do. Be Right Back!"
    assert response.json() == {
        "status": "success",
        "message": expected_message
    }

def test_integration_json_endpoint():
    response = client.get("/integration.json")
    assert response.status_code == 200
    json_response = response.json()
    
    # Check that the integration JSON contains a top-level "data" key
    assert "data" in json_response