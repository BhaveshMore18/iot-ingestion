from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ingest_reading():
    response = client.post("/readings", json={
        "sensor_id": "sensor-001",
        "metric": "temperature",
        "value": 23.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == "sensor-001"
    assert data["value"] == 23.5
    assert "timestamp" in data