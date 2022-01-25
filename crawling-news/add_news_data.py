from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
import datetime


# Firebaseにデータを追加するためのクラス
class AddNewsData:

    def __init__(self, news_list, json_path):
        self.news_list = news_list
        self.json_path = json_path

    def add_database(self):

        # Firebaseの初期化
        # Firebaseが初期化されているかの確認
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.json_path)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        # 現在時刻の取得
        datetime_now = datetime.datetime.now()

        # 取得した現在時刻を任意のフォーマットに変更
        formated_time = datetime_now.strftime("%Y年%m月%d日%H時%M分%S秒")

        # Firestoreのcollectionの名前を"news_{現在時刻}"という形式にする
        collection_name = f"news_{formated_time}"

        for data in self.news_list:
            try:
                title = data[0]
                summary = data[1]
                link = data[2]

                # Firestoreにアクセスして上記のcollection_name変数に格納した名前のcollectionを作成する。
                # Firestoreの場合、指定されたコレクションが存在しない場合は、自動的に生成される。
                base_ref = db.collection("news_data").document("data_set")
                doc_ref = base_ref.collection(collection_name)

                # collectionにタイトルと要約、リンクを追加していく。
                doc_ref.add({
                    "title": title,
                    "summary": summary,
                    "link": link,
                })
            except:
                pass

        # コレクションの名前をFirestoreに格納する
        # Firestoreではコレクションの名前をライブラリなどで取得することができない。そのため、コレクションの名前をデータとして格納することで、疑似的にコレクション名を取得できるようにする。
        doc_ref = db.collection("collections_name")
        doc_ref.add({"name": collection_name})


        return collection_name
