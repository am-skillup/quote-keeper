import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app
from app.db import get_session
from app.models import Quote

@pytest.fixture(name="session")
def session_fixture():
    # use StaticPool so the in-memory SQLite DB is shared across connections
    from sqlalchemy.pool import StaticPool
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # import models so SQLModel metadata is populated before creating tables
    import app.models  # registers models with SQLModel metadata
    SQLModel.metadata.create_all(engine)

    # make the app use the in-memory engine for tests
    import app.db as db
    db.engine = engine
    # ensure tables exist on the test engine (in case startup already ran)
    from app.db import create_db_and_tables
    create_db_and_tables()

    with Session(engine) as session:
        yield session

@pytest.fixture(autouse=True)
def client(session):
    def get_session_override():
        # create a fresh session for each request bound to the test engine
        import app.db as db
        from sqlmodel import Session as SQLSession
        with SQLSession(db.engine) as s:
            yield s

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
    if r.status_code != 200:
        print('DEBUG /quotes/random status:', r.status_code, 'body:', r.text)
    assert r.status_code == 200

    r = client.delete(f"/quotes/{qid}")
    assert r.status_code == 204

    r = client.get(f"/quotes/{qid}")
    assert r.status_code == 404
