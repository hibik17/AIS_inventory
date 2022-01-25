from typing import Any, List
from fastapi import APIRouter, Depends
from datetime import datetime

# import api.crawling.get_from_json_file as crawling 
import api.crawling.get_from_s3 as crawling
import api.doc2vec.predict_similar_book as doc2vec

import api.schemas.news_book as schemas_news_book

router = APIRouter()



@router.get(
    "/news-similar-books", response_model=List[schemas_news_book.NewsSimilarBook]
)
def get_news_and_similar_books(limit: int = 10):
    # newsと、それに関連する本をいくつか（デフォルト10個）返す
    # news_list = crawling.fetch_updated_news_data_from_s3(limit)
    # @FIXME: 
    news_list = crawling.make_news_for_demo()
    news_similar_books_array = []
    for news_dict in news_list:
        similar_book_dict = doc2vec.predict_similar_book_by_news(news_dict)
        news_similar_book = {"news": news_dict, "book": similar_book_dict}
        news_similar_books_array.append(news_similar_book)
    return news_similar_books_array
