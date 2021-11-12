import datetime, json

from models import db_session
from models.logs import Logs

db_session.global_init('database.db')

def get_log(url, password):
    session = db_session.create_session()
    log = session.query(Logs).filter(Logs.url==url).first()

    if password == log.password:
        log_as_dict = {
            "id": log.id,
            "url": log.url,
            "data": json.loads(log.data)
        }
        return log_as_dict
    return "Forgot password!"

def create_logs(url, password):
    session = db_session.create_session()
    log = Logs(
        url=url,
        data='[]',
        password=password,
    )
    session.add(log)
    session.commit()
    return True

def append_logs(url, data):
    session = db_session.create_session()
    log = session.query(Logs).filter(Logs.url==url).first()
    loge = log.data
    loge = json.loads(loge)
    loge.append(data)
    log.data = json.dumps(loge)

    session.commit()
    return True