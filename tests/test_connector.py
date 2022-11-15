from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)
