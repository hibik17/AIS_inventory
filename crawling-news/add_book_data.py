from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from get_summary import GetSummary
from dotenv import load_dotenv
import os


class AddBookData:

    def __init__(self,json_path, book_list):
        self.json_path = json_path
        self.book_list = book_list

    def add_database(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.json_path)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        for data in self.book_list:
            print(data)
            try:
                title = data[0]
                ISBN = data[1]
                book = GetSummary(ISBN)
                summary = book.get_suumary()

                base_ref = db.collection("book_data").document("data_set")
                doc_ref = base_ref.collection(ISBN)


                doc_ref.add({
                    "title": title,
                    "summary": summary
                })

            except:
                pass

load_dotenv()
JSON_PATH = os.environ["FIREBASE_API_KEY"]
data_list = [["こころ","9784101010137"],["Inclusive design patterns : coding accessibility into web design","9784862463876"]]


data = AddBookData(JSON_PATH, data_list)
data.add_database()
