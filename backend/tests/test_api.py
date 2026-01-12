import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app
from app.db import get_session
from app.models import Quote

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(autouse=True)
def client(session):
    def get_session_override():
        with session:
            yield session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_and_get_quote(client):
    payload = {"text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde", "tags": ["inspirational"]}
    r = client.post("/quotes", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["text"] == payload["text"]
    qid = data["id"]

    r = client.get(f"/quotes/{qid}")
    assert r.status_code == 200
    assert r.json()["author"] == "Oscar Wilde"

    r = client.get("/quotes")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/quotes?tag=inspirational")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/quotes/random")
    assert r.status_code == 200

    r = client.delete(f"/quotes/{qid}")
    assert r.status_code == 204

    r = client.get(f"/quotes/{qid}")
    assert r.status_code == 404
