from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(example="「日中摩擦」を検証する")
    author: str = Field(example="東城 久夫")
    description: str = Field(example="教師・家庭・地域・スクールカウンセラー連携でとりくむ学校づくり。学校臨床、その実践と可能性。")
    publisher: str = Field(example="新曜社")
    published_year: str = Field(example="2002.12")
    location: str = Field(example="相1F一般300")
    isbn: str = Field(example="478850829X")
    similarity: Optional[float] = Field(example=0.552038)

    class Config:
        orm_mode = True
