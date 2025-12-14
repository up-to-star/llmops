import pytest
import sys
import os
from fastapi.testclient import TestClient
import dotenv

# Add project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.http import app

dotenv.load_dotenv()

@pytest.fixture
def client():
    client = TestClient(app)
    yield client
