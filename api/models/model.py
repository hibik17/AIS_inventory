from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp


from api.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    book_collection_number = Column(String(255), nullable=False)
    book_unique_number = Column(String(255))
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    created_at = Column(Timestamp, nullable=False,
                        server_default=text('current_timestamp'))
    updated_at = Column(Timestamp, nullable=False,
                        server_default=text('current_timestamp'))
