from typing import List, Optional
from sqlmodel import SQLModel, Field

class QuoteBase(SQLModel):
    text: str
    author: Optional[str] = None
    tags: Optional[List[str]] = None

class Quote(QuoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class QuoteCreate(QuoteBase):
    ...
