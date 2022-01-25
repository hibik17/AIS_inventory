from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials


# 最も新しく追加されたコレクションの名前を取得するためのクラス
class GetCollenctionName:

    def __init__(self, json_path):
        self.json_path = json_path

    def read(self):
        # Firebaseの初期化
        # Firebaseが初期化されているかの確認
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.json_path)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        # collections_nameのデータを取得
        docs = db.collection("collections_name").get()

        # collections_nameのデータの値をリストに格納
        names_list = sorted([doc.to_dict()["name"] for doc in docs])

        # リストの最後尾の値（最も新しく追加されたコレクション名）を返す
        return names_list[-1]
