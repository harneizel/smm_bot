import hashlib
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from bot.utils.config import MRH_LOGIN, PASS_2
from bot.database import requests as rq

app = FastAPI()

# Настройка CORS
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники, можно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)'''

# Mount the static directory
app.mount("/js", StaticFiles(directory="web-app/js"), name="js")

# получение данных платежки для подтвержденияS
@app.post('/get-payment')
async def get_payment(request: Request):
    #data = await request.json()
    # argument = data.get("argument")
    print("get payment получен")
    OutSum = request.query_params['OutSum']  # сумма платежа
    InvId = request.query_params['InvId']  # id клиента
    Fee = request.query_params['Fee']  # комиссия
    EMail = request.query_params['Email']  # email указанный при оплате
    SignatureValue = request.query_params['SignatureValue']  # полученная контрольная сумма
    PaymentMethod = request.query_params['PaymentMethod']  # метод платежа
    IncCurrLabel = request.query_params['IncCurrLabel']  # валюта платежа
    Id = request.query_params['Shp_id']  # tg_id клиента
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
    
'''
@app.post('/get-payment')
async def get_payment(data = Body()):
    print("get payment получен")
    OutSum = int(data['OutSum'])  # сумма платежа
    InvId = int(data['InvId'])  # id клиента
    Fee = data['Fee']  # комиссия
    EMail = data['Email']  # email указанный при оплате
    SignatureValue = data['SignatureValue']  # полученная контрольная сумма
    PaymentMethod = data['PaymentMethod']  # метод платежа
    IncCurrLabel = data['IncCurrLabel']  # валюта платежа
    Id = int(data['Shp_id'])  # tg_id клиента
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
'''

# главная страница web app
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

# забирание инфо о пользователе
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
        uvicorn.run(app, host="0.0.0.0", port=443)#, ssl_keyfile="web-app/ssl/YOURPRIVATE.key", ssl_certfile="web-app/ssl/YOURPUBLIC.pem")
    except:
        print("Ошибка")
