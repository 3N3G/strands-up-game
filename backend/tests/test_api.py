import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Word Search Game API is running"}

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_game(client):
    response = client.post("/api/game/generate", json={"seed_word": "music"})
    assert response.status_code == 200
    
    data = response.json()
    assert "theme" in data
    assert "spangram" in data
    assert "words" in data
    assert "board" in data
    assert "placement_info" in data
    
    # Check board structure
    assert isinstance(data["board"], list)
    assert len(data["board"]) > 0
    assert isinstance(data["board"][0], list)
    
    # Check placement info
    assert "spangram" in data["placement_info"]
    assert "words" in data["placement_info"]
    
def test_generate_game_no_seed(client):
    response = client.post("/api/game/generate", json={})
    assert response.status_code == 200
    
    data = response.json()
    assert "theme" in data
    assert "spangram" in data
    assert "words" in data
    assert "board" in data
    assert "placement_info" in data 