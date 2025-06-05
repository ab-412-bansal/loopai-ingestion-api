import time
import pytest
from app.main import app
from flask.testing import FlaskClient

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_ingestion_and_status(client: FlaskClient):
    # Step 1: Send a valid ingestion request
    response = client.post('/ingest', json={
        "ids": [1, 2, 3, 4, 5],
        "priority": "HIGH"
    })
    assert response.status_code == 200
    ingestion_id = response.get_json()["ingestion_id"]
    assert ingestion_id is not None

    # Step 2: Immediately check status
    status_response = client.get(f'/status/{ingestion_id}')
    assert status_response.status_code == 200
    status_data = status_response.get_json()
    assert status_data["status"] in ["yet_to_start", "triggered"]

    # Step 3: Wait and check for completed status
    time.sleep(15)  # 2 batches = at least 10 seconds, add margin

    status_response = client.get(f'/status/{ingestion_id}')
    assert status_response.status_code == 200
    status_data = status_response.get_json()
    assert status_data["status"] == "completed"
