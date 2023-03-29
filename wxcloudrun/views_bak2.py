from flask import Flask, request
import requests,json,os
from run import app

#app = Flask(__name__)

@app.route('/', methods=['POST'])

def wx():
    # 接收微信发来的消息
    rec_data = request.get_json()
    # print(rec_data)
    openid = request.headers.get('x-wx-openid')
    msg='['+rec_data['message']+']'
    message = json.loads(msg)
    code=rec_data['code']
    # wxurl = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?from_appid=wx8bfa8275fb71767f"

    # 转发给机器人并获得回复
    # os.environ["OPENAI_API_KEY"] = "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"
    os.environ["OPENAI_API_KEY"] = code
    chaturl='https://service-5eae8k92-1315204370.sg.apigw.tencentcs.com/v1/chat/completions'
    chatheaders={
        'Content-Type':'application/json',
        'Authorization': 'Bearer {}'.format(os.environ["OPENAI_API_KEY"])
    }
    chatdata=json.dumps(
    {
    'model':'gpt-3.5-turbo',
    # 'messages':[{'role':'user','content':message}]
    'messages':message
    }
    )
    chatresponse = requests.request("POST",chaturl,headers=chatheaders,data=chatdata)
    # print(chatresponse)
    # 解析回复内容，获得机器人答复
    if 'choices' in chatresponse.json():
        answer=chatresponse.json()['choices'][0]['message']['content']
    else:
        answer=chatresponse.json()['error']['code']
    response = {
        "content": answer
        }
    return response
