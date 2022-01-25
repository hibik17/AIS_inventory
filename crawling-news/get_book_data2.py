import os
from dotenv import load_dotenv
import requests
import json
import time
load_dotenv()


# 楽天ブックスを使用して本の情報を得るためのクラス
class GetBookData2:

    def __init__(self, ISBN, app_id):
        self.ISBN = ISBN
        self.app_id = app_id

    def read(self):
        # 楽天ブックスのapiは1秒に一回しかリクエストできない
        time.sleep(1)

        # 楽天ブックスのapiを使用して本の情報を入手する。
        url = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId={self.app_id}&isbn={self.ISBN}"
        response = requests.get(url)
        text = response.text

        # 入手した本の情報を読み込む
        data = json.loads(text)
        book_text = ""

        # 入手した情報の中に欲しい情報（今回の場合は本の要約）が含まれているのか調べる
        if data["count"] != 0:
            if "Item" in data["Items"][0] and "itemCaption" in data["Items"][0]["Item"]:
                book_text = data["Items"][0]["Item"]["itemCaption"]
            else:
                pass
        else:
            pass

        return book_text
