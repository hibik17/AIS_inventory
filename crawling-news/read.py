from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials


# 指定されたコレクションのデータを読み取るためのクラス
class ReadCollection:

    def __init__(self, collection_name, json_path):
        self.collection_name = collection_name
        self.json_path = json_path


    def read(self):
        # Firebaseが初期化されているかの確認
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.json_path)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        base_ref = db.collection("news_data").document("data_set")
        docs = base_ref.collection(self.collection_name).get()

        for doc in docs:
            data = doc.to_dict()
            print(data)
