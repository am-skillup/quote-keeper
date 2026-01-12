from typing import List, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import JSON

class QuoteBase(SQLModel):
    text: str
    author: Optional[str] = None
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

class Quote(QuoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class QuoteCreate(QuoteBase):
    ...
