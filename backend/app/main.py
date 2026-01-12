from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from sqlmodel import select

from .models import Quote, QuoteCreate
from .db import create_db_and_tables, get_session
from sqlmodel import Session

app = FastAPI(title="Quote Keeper")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health", include_in_schema=False)
def health():
    """Simple health endpoint used by PaaS providers and load balancers."""
    return {"status": "ok", "message": "alive"}


@app.post("/quotes", status_code=201)
def create_quote(quote: QuoteCreate, session: Session = Depends(get_session)):
    db_quote = Quote.from_orm(quote)
    session.add(db_quote)
    session.commit()
    session.refresh(db_quote)
    return db_quote

@app.get("/quotes", response_model=List[Quote])
def list_quotes(author: Optional[str] = None, tag: Optional[str] = None, limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    q = select(Quote)
    if author:
        q = q.where(Quote.author == author)
    results = session.exec(q.offset(offset).limit(limit)).all()
    if tag:
        results = [r for r in results if r.tags and tag in r.tags]
    return results

import random

@app.get("/quotes/random", response_model=Quote)
def random_quote(session: Session = Depends(get_session)):
    q = select(Quote)
    results = session.exec(q).all()
    if not results:
        raise HTTPException(status_code=404, detail="No quotes found")
    return random.choice(results)

@app.get("/quotes/{quote_id}", response_model=Quote)
def get_quote(quote_id: int, session: Session = Depends(get_session)):
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@app.delete("/quotes/{quote_id}", status_code=204)
def delete_quote(quote_id: int, session: Session = Depends(get_session)):
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    session.delete(quote)
    session.commit()
    return None

# Serve frontend static files from the `frontend` directory when deployed as a single service
from pathlib import Path
from fastapi.staticfiles import StaticFiles

# compute path relative to backend package: backend/frontend
_frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
if _frontend_dir.exists():
    # mount static files at the root to allow index and assets to be served at '/'
    # Mounting AFTER the API routes ensures API endpoints take precedence (prevents StaticFiles from
    # intercepting POST/DELETE methods for API paths).
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
