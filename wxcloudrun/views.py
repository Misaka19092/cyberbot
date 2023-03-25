from flask import Flask, request
import requests
from run import app

@app.route('/', methods=['POST'])

def wx():
    # rec_data = request.get_json()
    # openid = request.headers.get('x-wx-openid')
    # message = rec_data['message']
    # data = {
    #     "touser": openid,
    #     "msgtype": "text",
    #     "text": {
    #         "content": "Hello World,{}".format(message)
    #     }
    # }
    # url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send"
    # r = requests.post(url, json=data)
    return 'success'

if __name__ == '__main__':
    app.run()