from typing import Any, List
from fastapi import APIRouter, Depends
from datetime import datetime


import api.schemas.book as schemas_book


router = APIRouter()


@router.get("/books", response_model=List[schemas_book.Book])
def get_books():
    # 書籍一覧取得
    return [
        schemas_book.Book(
            id=1,
            book_collection_number="所蔵番号",
            book_unique_number="書誌番号",
            title="タイトル",
            author="著者",
            publisher="出版社",
            created_at="2021-11-06T08:19:09.035Z",
            updated_at="2021-11-06T08:19:09.035Z",
        )
    ]


@router.post("/books", response_model=schemas_book.Book)
def create_book():
    # 書籍作成

    return schemas_book.Book(
        id=1,
        book_collection_number="所蔵番号",
        book_unique_number="書誌番号",
        title="タイトル",
        author="著者",
        publisher="出版社",
        created_at="2021-11-06T08:19:09.035Z",
        updated_at="2021-11-06T08:19:09.035Z",
    )


@router.get("/books/{book_id}", response_model=schemas_book.Book)
def show_book(book_id):
    # 書籍詳細
    return schemas_book.Book(
        id=1,
        book_collection_number="所蔵番号",
        book_unique_number="書誌番号",
        title="タイトル",
        author="著者",
        publisher="出版社",
        created_at="2021-11-06T08:19:09.035Z",
        updated_at="2021-11-06T08:19:09.035Z",
    )


@router.put("/books/{book_id}", response_model=schemas_book.Book)
def update_book(book_id):
    # 書籍更新
    return schemas_book.Book(
        id=1,
        book_collection_number="所蔵番号",
        book_unique_number="書誌番号",
        title="タイトル",
        author="著者",
        publisher="出版社",
        created_at="2021-11-06T08:19:09.035Z",
        updated_at="2021-11-06T08:19:09.035Z",
    )


@router.delete("/books/{book_id}", response_model=schemas_book.Book)
def delete_book(book_id):
    # 書籍削除
    return schemas_book.Book(
        id=1,
        book_collection_number="所蔵番号",
        book_unique_number="書誌番号",
        title="タイトル",
        author="著者",
        publisher="出版社",
        created_at="2021-11-06T08:19:09.035Z",
        updated_at="2021-11-06T08:19:09.035Z",
    )


# @router.post("/books", response_model=)
