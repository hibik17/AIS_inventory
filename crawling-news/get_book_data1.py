import json
import requests


# openBDを使用して本の情報を得るためのクラス
class GetBookData1:

    def __init__(self, ISBN):
        self.ISBN = ISBN

    def read(self):
        # openbdのapiを使って本の情報を入手する。
        response = requests.get(f"https://api.openbd.jp/v1/get?isbn={self.ISBN}")
        text = response.text

        # 入手した情報を読み込む
        data = json.loads(text)[0]

        book_text = ""

        # 入手した情報の中に欲しい情報（今回の場合は本の要約）が含まれているのか調べる
        if not data == None:
            if "CollateralDetail" in data["onix"] and "TextContent" in data["onix"]["CollateralDetail"]:
                for text in data["onix"]["CollateralDetail"]["TextContent"]:
                    book_text += text["Text"]
            else:
                pass
        else:
            pass

        return book_text
