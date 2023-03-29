from flask import Flask, request,g
import requests,json,os
from run import app

#app = Flask(__name__)

@app.route('/', methods=['POST'])

def wx():
    # 接收微信发来的消息
    rec_data = request.get_json()
    g.openid = request.headers.get('x-wx-openid')
    g.sessionid=rec_data['sessionid']
    message0=rec_data['message']
    message1='['+message0+']'
    message = json.loads(message1)
    code=rec_data['code']
    os.environ["OPENAI_API_KEY"] = code
    #只有通过前段回传的方式key才不会失效
    chaturl='https://service-5eae8k92-1315204370.sg.apigw.tencentcs.com/v1/chat/completions'
    chatheaders={
        'Content-Type':'application/json',
        'Authorization': 'Bearer {}'.format(os.environ["OPENAI_API_KEY"])
    }
    chatdata=json.dumps(
    {
    'model':'gpt-3.5-turbo',
    'messages':message
    }
    )
    chatresponse = requests.request("POST",chaturl,headers=chatheaders,data=chatdata)
    # 解析回复内容，获得机器人答复
    if 'choices' in chatresponse.json():
        answer=chatresponse.json()['choices'][0]['message']['content']
        g.message2='['+message0+',{"role":"assistant","content":"'+answer+'"}'+']'
    else:
        answer=chatresponse.json()['error']['code']
    response = {
        "content": answer
        }
    return response

@app.after_request
def after(response):
    app_root = os.path.dirname(os.path.abspath(__file__))
    file_dir=app_root+'\\'+g.openid
    file_path=file_dir+'\\'+g.sessionid+'.txt'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(file_path, "w",encoding='utf-8') as file:
        file.write(g.message2)
    return response