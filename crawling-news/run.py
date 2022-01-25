from dotenv import load_dotenv
import os
from crawling import CrawlingNews
from convert_news_data import ConvertNewsData
from convert_book_data import ConvertBookData
import datetime
import json



# ニュース記事のRSSのURL
URL = "https://www.news24.jp/rss/index.rdf"

# FirebaseのAPIキー
load_dotenv()
JSON_PATH = os.environ["FIREBASE_API_KEY"]


# ニュースデータのクローリング
news_data = CrawlingNews(URL)
news_list = news_data.crawling()

# 現在時刻をjsonファイルのファイル名にする
datetime_now = datetime.datetime.now()
formated_time = datetime_now.strftime("%Y年%m月%d日%H時%M分%S秒")
file_name= f"news_{formated_time}"
file_path = f"./news_files/{file_name}.json"

# ニュースデータのjsonファイルへの変換処理
json_data = ConvertNewsData(news_list, file_path)
json_data.convert()


# テストデータ1
isbn_list = [["信長の原理〈上〉","9784041098646"], ["信長の原理〈下〉", "9784041098653"], ["じんかん", "9784065192702"], ["渦 : 妹背山婦女庭訓魂結び", "9784163909875"], ["銀閣の人", "9784041072356"]]

# テストデータ2
isbn_list = [["織田信長と安土城", "4422201042"], ["織田信長 : 中世最後の覇者", "412100843X"]]

# 本のデータのjsonファイルへの変換処理
folder_path = "./book_files/book.json"
datas = ConvertBookData(isbn_list, folder_path)
datas.convert()

# 本のデータの読み取り用処理
data_list = os.listdir("./book_files/")

for i in data_list:

    with open(f"./book_files/{i}", "r", encoding="utf-8") as f:
        print(json.loads(f.read()))
