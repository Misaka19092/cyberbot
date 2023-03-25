from flask import Flask, request
import requests
from run import app

#app = Flask(__name__)

@app.route('/', methods=['POST'])

def wx():
    rec_data = request.get_json()
    openid = request.headers.get('x-wx-openid')
    message = rec_data['message']
    data = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            # "content": "Hello World,{}".format(message)
        "content": "Hello World"
        }
    }
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?from_appid=wx8bfa8275fb71767f"
    r = requests.post(url, json=data)
    return data

@app.route('/test')
def test():
    """
    :return: 返回index页面
    """
    return "data"
# if __name__ == '__main__':
#     app.run()