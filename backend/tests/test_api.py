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


def test_validation_rejects_missing_text(client):
    payload = {"author": "No Text", "tags": []}
    r = client.post("/quotes", json=payload)
    assert r.status_code == 422


def test_filter_by_author(client):
    a1 = {"text": "One", "author": "Alice", "tags": []}
    a2 = {"text": "Two", "author": "Bob", "tags": ["x"]}
    client.post("/quotes", json=a1)
    client.post("/quotes", json=a2)

    r = client.get("/quotes?author=Alice")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["author"] == "Alice"


def test_list_empty_start(client):
    # create a fresh engine/session and verify listing when no quotes
    import app.db as db
    from sqlalchemy import create_engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    # temporarily override get_session to use the fresh empty engine
    from app.db import get_session as real_get_session
    def get_empty_session():
        from sqlmodel import Session as SQLSession
        with SQLSession(engine) as s:
            yield s
    app.dependency_overrides[real_get_session] = get_empty_session

    r = client.get("/quotes")
    assert r.status_code == 200
    assert r.json() == []

    app.dependency_overrides.pop(real_get_session, None)