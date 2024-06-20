from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
from bot.utils.config import MRH_LOGIN, PASS_2
from waitress import serve

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
    if SignatureIntended==SignatureValue:
        print(f"ПОДПИСИ СОВПАЛИ, ID: {Id}")
        return f"OK{InvId}"

if __name__ == '__main__':
    try:
        serve(app, host="0.0.0.0", port=8080) # запуск сервера
    except:
        print("Завершение работы")