import os

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["SECRET_KEY"] = (
    "test-secret"
)

os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from app.main import app

from app.database import init_db


init_db()


client = TestClient(app)