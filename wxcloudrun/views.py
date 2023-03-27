from flask import Flask, request
import requests,json
from run import app

#app = Flask(__name__)

@app.route('/', methods=['POST'])

def wx():
    # 接收微信发来的消息
    rec_data = request.get_json()
    openid = request.headers.get('x-wx-openid')
    message = rec_data['message']
    # 转发给机器人并获得回复
    wxurl = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?from_appid=wx8bfa8275fb71767f"
    chaturl='https://service-5eae8k92-1315204370.sg.apigw.tencentcs.com/v1/chat/completions'
    chatheaders={
        'Content-Type':'application/json',
        'Authorization': 'Bearer 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'
    }
    chatdata=json.dumps(
    {
    'model':'gpt-3.5-turbo',
    'messages':[{'role':'user','content':message}]
    }
    )
    chatresponse = requests.request("POST",chaturl,headers=chatheaders,data=chatdata)

    # 解析回复内容，获得机器人答复
    answer=chatresponse.json()['choices'][0]['message']['content']
    response = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            # "content": "Hello World,{}".format(message)
        "content": answer
        }
    }
    r = requests.post(wxurl, json=response)
    return response