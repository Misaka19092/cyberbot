import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from cyberbot.wxcloudrun.model import History

# 初始化日志
logger = logging.getLogger('log')


def query_historybyid(id):
    """
    根据ID查询history实体
    :param id: history的ID
    :return: history实体
    """
    try:
        return History.query.filter(History.id == id).first()
    except OperationalError as e:
        logger.info("query_historybyid errorMsg= {} ".format(e))
        return None


def delete_historybyid(id):
    """
    根据ID删除history实体
    :param id: history的ID
    """
    try:
        history = History.query.get(id)
        if history is None:
            return
        db.session.delete(history)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_historybyid errorMsg= {} ".format(e))


def insert_history(history):
    """
    插入一个history实体
    :param history: History实体
    """
    try:
        db.session.add(history)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_history errorMsg= {} ".format(e))


def update_historybyid(history):
    """
    根据ID更新history的值
    :param history实体
    """
    try:
        history = query_historybyid(history.id)
        if history is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_historybyid errorMsg= {} ".format(e))
