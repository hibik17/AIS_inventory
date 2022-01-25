from typing import Optional
from pydantic import BaseModel, Field
from .book import Book
from .news import News


class NewsSimilarBook(BaseModel):
    news: News
    book: Book

    class Config:
        orm_mode = True
