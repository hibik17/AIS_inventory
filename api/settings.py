# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()
# 環境変数を参照
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
