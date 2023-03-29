from flask import Flask, request,g
import requests,json,os,time
from run import app
from datetime import datetime
from wxcloudrun.dao import delete_historybyid, query_historybyid, insert_history, update_historybyid
from wxcloudrun.model import History
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
#app = Flask(__name__)

@app.route('/chat', methods=['POST'])
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

@app.route('/recall', methods=['POST'])
def re():
    sessionid=request.get_json()['sessionid']
    openid= request.headers.get('x-wx-openid')
    recallid=openid+'-'+sessionid
    recall = query_historybyid(recallid)
    while recall is None:
        time.sleep(2)
        recall = query_historybyid(recallid)
    answer0=recall.chatjson
    answer=answer0.json()[-1]['content']
    response = {
        "content": answer
        }
    return response


@app.after_request
def after(response):
    if request.endpoint == 'chat':
        his_id=g.openid+'-'+g.sessionid
        history = query_historybyid(his_id)
        if history is None:
            history = History()
            history.id = his_id
            history.chatjson = g.message2
            insert_history(history)
        else:
            history.id = his_id
            history.chatjson = g.message2
            update_historybyid(history)

    return response

@app.after_request
def after(response):
    if request.endpoint == 'chat':
        his_id = g.openid + '-' + g.sessionid
        history = query_historybyid(his_id)
        if history is None:
            history = History()
            history.id = his_id
            history.chatjson = g.message2
            insert_history(history)
        else:
            history.id = his_id
            history.chatjson = g.message2
            update_historybyid(history)
    return response