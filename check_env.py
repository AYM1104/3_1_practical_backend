from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# 環境変数を取得
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# 環境変数を出力
print(f"DB_USER: {db_user}")
print(f"DB_PASSWORD: {db_password}")
print(f"DB_HOST: {db_host}")
print(f"DB_PORT: {db_port}")
print(f"DB_NAME: {db_name}")