#用来查看前段发来的信息
from flask import Flask, request
import requests,json,os
from run import app

#app = Flask(__name__)
@app.route('/', methods=['POST'])

def wx():
    # 接收微信发来的消息
    rec_data = request.get_json()
    openid = request.headers.get('x-wx-openid')
    message = rec_data['message']
    response = {
        "content": message
    }
    return response