import os
from dotenv import load_dotenv
from get_book_data1 import GetBookData1
from get_book_data2 import GetBookData2
load_dotenv()

# 本の情報を得るための処理をまとめたクラス
class GetSummary:

    def __init__(self, ISBN):
        self.ISBN = ISBN

    def get_suumary(self):
        summary = ""

        # 最初にopenBDを使った方法で本の要約の取得を試みる
        book1 = GetBookData1(self.ISBN)
        summary = book1.read()

        # 仮にopenBDを使って本の要約を取得できなかったら、楽天ブックスを使って取得を試みる
        if summary == "":
            APP_ID = os.environ["RAKUTEN_BOOKS_APP_ID"]
            book2 = GetBookData2(self.ISBN, APP_ID)
            summary = book2.read()
        else:
            pass

        return summary
