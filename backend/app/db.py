import os
from sqlmodel import create_engine, SQLModel, Session

# use DATABASE_URL env var if present (supports sqlite and postgres)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quotes.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
