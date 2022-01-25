from typing import Optional

from pydantic import BaseModel, Field


class News(BaseModel):
    title: str = Field(example="消される、天安門事件の「記憶」香港の大学、親中派が圧力")
    summary: str = Field(
        example="消される天安門事件の記憶。香港の大学、親中派が圧力。香港の大学で、民主化を求める学生らが北京で武力弾圧された1989年の天安門事件"
    )
    url: str = Field(example="url")
    crawled_at: Optional[str] = Field(example="2021年12月30日11時53分33秒")

    class Config:
        orm_mode = True
