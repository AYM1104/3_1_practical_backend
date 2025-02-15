from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
import json
from db_control import crud, mymodels_MySQL

import pymysql
import os


# MySQLのテーブル作成
# from db_control.create_tables import init_db

# # アプリケーション初期化時にテーブルを作成
# init_db()


class Customer(BaseModel):
    customer_id: str = Field(..., description="顧客IDは必須です")
    customer_name: str
    age: int
    gender: str


app = FastAPI(
    title="My FastAPI App",
    description="This is a FastAPI application",
    version="1.0",
    docs_url="/docs",  # ← ここがないと `/docs` は使えない！
    redoc_url="/redoc"  # ← これは ReDoc（任意）
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.post("/customers")
def create_customer(customer: Customer):
    values = customer.dict()
    tmp = crud.myinsert(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values.get("customer_id"))

    if result:
        result_obj = json.loads(result)
        return result_obj if result_obj else None
    return None


@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels_MySQL.Customers)
    # 結果がNoneの場合は空配列を返す
    if not result:
        return []
    # JSON文字列をPythonオブジェクトに変換
    return json.loads(result)


@app.put("/customers")
def update_customer(customer: Customer):
    values = customer.dict()
    values_original = values.copy()
    tmp = crud.myupdate(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values_original.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()



@app.get("/test-db")
def test_db_connection():
    try:
        conn = pymysql.connect(
            host="tech0-gen-9-step3-1-db-3.mysql.database.azure.com",
            user="tech0gen9student",
            password="vY7JZNfU",
            database="step3-1_enchan_db",
            port=3306,
            ssl_ca="/Users/ayu/Tech0/Step3/Step3-1/practical/sample4/DigiCertGlobalRootCA.crt.pem"
        )
        conn.close()
        return {"message": "✅ FastAPI から MySQL に接続成功！"}
    except Exception as e:
        return {"error": str(e)}