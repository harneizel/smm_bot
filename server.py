from flask import Flask, request
import hashlib
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

from bot.utils.config import MRH_LOGIN, PASS_2
from bot.database import requests as rq

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники, можно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/js", StaticFiles(directory="web-app/js"), name="js")

# получение данных для подтверждения
@app.get('/get-payment')
async def get_payment():
    print("get payment получен")
    OutSum: str = request.form.get('OutSum')  # сумма платежа
    InvId: int = request.form.get('InvId')  # id клиента
    Fee = request.form.get('Fee')  # комиссия
    EMail = request.form.get('Email')  # email указанный при оплате
    SignatureValue = request.form.get('SignatureValue')  # полученная контрольная сумма
    PaymentMethod = request.form.get('PaymentMethod')  # метод платежа
    IncCurrLabel = request.form.get('IncCurrLabel')  # валюта платежа
    Id = request.form.get('Shp_id')  # tg_id клиента
    print(OutSum, InvId, Fee, EMail, SignatureValue, PaymentMethod, IncCurrLabel, Id)
    pass_2 = PASS_2
    SignatureIntended = hashlib.md5(f"{OutSum}:{InvId}:{pass_2}:Shp_id={Id}".encode('utf-8')).hexdigest()  # предполагаемая подпись
    SignatureIntended = SignatureIntended.upper()
    print(SignatureValue, SignatureIntended)
    if SignatureIntended == SignatureValue:
        print(f"ПОДПИСИ СОВПАЛИ, ID: {Id}")
        asyncio.run(rq.sub_type_paid(int(Id)))
        return f"OK{InvId}"
    print("подписи не совпали")

@app.get('/app')
async def open_app():
    print("Приложение открыто")
    with open('./web-app/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/app/knowledge')
async def open_app():
    print("knowledge открыто")
    with open('./web-app/knowledge.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/app/networking')
def open_app():
    print("networking открыт")
    with open('./web-app/networking.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/user_info/{user_id}')
async def user_info(user_id: int):
    print(user_id)
    user_data = await rq.get_user_data(user_id)
    print(user_data)
    data = {'desc': user_data[0], 'tag1': user_data[1], 'tag2': user_data[2],
            'tag3': user_data[3], 'tag4': user_data[4],'tag5': user_data[5]}
    #json_data = json.dumps(data)
    return data

# Запуск сервера с HTTPS
if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=443, ssl_keyfile="web-app/ssl/private.pem", ssl_certfile="web-app/ssl/public.pem")
    except:
        print("Ошибка")
