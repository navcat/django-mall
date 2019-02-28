import random
from datetime import datetime


def generate_trans_id(date=None):
    """ 生成交易流水"""
    if date is None:
        date = datetime.now()
    str_date = date.strftime('%Y%m%d')
    str_time = date.strftime('%H%M%S%f')
    return str_date + str_time + str(random.randint(1000, 9999))