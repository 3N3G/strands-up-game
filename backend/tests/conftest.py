import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def requires_openai():
    """Skip test if OPENAI_API_KEY is not set."""
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable not set")

@pytest.fixture(autouse=True)
def setup_environment():
    """Setup any required environment variables."""
    pass  # We'll handle specific requirements in individual fixtures 