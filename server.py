from flask import Flask, request
import hashlib
from waitress import serve
import asyncio

from bot.utils.config import MRH_LOGIN, PASS_2
from bot.database import requests as rq

app = Flask(__name__)

@app.route('/')
def default():
    return "Привет"

#
@app.route('/send-app', methods=["GET"])
def send_app():
    print("Приложение отправлено")

# получение данных для подтверждения
@app.route('/get-payment', methods=['POST'])
def get_payment():
    print("get payment получен")
    OutSum = request.form.get('OutSum') # сумма платежа
    InvId = request.form.get('InvId') # id клиента
    Fee = request.form.get('Fee') # комиссия
    EMail = request.form.get('Email') # email указанный при оплате
    SignatureValue = request.form.get('SignatureValue') # полученная контрольная сумма
    PaymentMethod = request.form.get('PaymentMethod') # метод платежа
    IncCurrLabel = request.form.get('IncCurrLabel') # валюта платежа
    Id = request.form.get('Shp_id') # tg_id клиента
    print(OutSum, InvId, Fee, EMail, SignatureValue, PaymentMethod, IncCurrLabel, Id)
    pass_2 = PASS_2
    SignatureIntended = hashlib.md5(f"{OutSum}:{InvId}:{pass_2}:Shp_id={Id}".encode('utf-8')).hexdigest() # предполагаемая подпись
    SignatureIntended = SignatureIntended.upper()
    print(SignatureValue, SignatureIntended)
    if SignatureIntended==SignatureValue:
        print(f"ПОДПИСИ СОВПАЛИ, ID: {Id}")
        asyncio.run(rq.sub_type_paid(int(Id)))
        return f"OK{InvId}"
    print("подписи не совпали")

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0") # запуск сервера
    except:
        print("Завершение работы")
