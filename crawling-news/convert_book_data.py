import json
from os import read
from get_summary import GetSummary

# 本の情報をjson形式に変換してフォルダーに格納するクラス
class ConvertBookData:

    def __init__(self, book_lists, filepath):
        self.book_lists = book_lists
        self.filepath = filepath

    def convert(self):
        # 本の情報を追加する際は、一度jsonファイル内の全てのデータを読み取って変数に格納してから、その変数に随時格納していく

        # jsonファイル内が空の状態で読み取るとエラーが出るための例外処理を用意する
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                read_data = json.load(f)
                dict_book = read_data
        except:
            dict_book = {}

        # 複数の本のデータが「タイトル、ISBNコード」の順で二次元配列で渡される
        for data in self.book_lists:
            title = data[0]
            ISBN = data[1]

            # ISBNコードを使用してAPIを叩き本の要約を取得する
            summary = GetSummary(ISBN).get_suumary()

            # dict_bookにISBNコードをキーとしてデータを格納する
            dict_book[ISBN] = dict((["title", title], ["summary", summary]))



        # 指定されたjsonファイルにデータを格納する
        # データは辞書型からjson形式に変換する
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(dict_book, f, indent=4, ensure_ascii=False)
