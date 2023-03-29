from datetime import datetime

from wxcloudrun import db


# 计数表
class History(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'chathistory'

    # 设定结构体对应表格的字段
    id = db.Column(db.Text,primary_key=True)
    chatjson = db.Column(db.Text)
