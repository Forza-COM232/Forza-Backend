from src.forza_backend.main import app
from src.forza_backend.models.sample import SampleModel
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def test_client() -> TestClient:
    client = TestClient(app)
    return client

def test_sample_model(test_client: TestClient):
    response = test_client.get(url="/sample/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Sample User"
    