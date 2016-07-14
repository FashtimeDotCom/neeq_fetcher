# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import datetime

BASE_URL = 'http://www.neeq.com.cn/'


# Trading tips SQL
RETRIVE_ID_NUMBER_SQL_TEMPLATE = 'SELECT COUNT(*) FROM {}\
                                    WHERE POST_DATE='


def read_data_str(target, values):
    try:
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # 转换 str 为 bytes
        req = urllib.request.Request(BASE_URL + target, data)
        with urllib.request.urlopen(req) as response:
            page = response.read().decode()
    except:
        print('ERROR')
    if page:
        return page


def get_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d'
    return time.strftime(ISOTIMEFORMAT, time.localtime())


def generate_date_list(s, e):
    date_list = []
    start = datetime.datetime.strptime(s, '%Y-%m-%d')
    end = datetime.datetime.strptime(e, '%Y-%m-%d')
    while start <= end:
        date_list.append(start.strftime('%Y-%m-%d'))
        start += datetime.timedelta(days=1)
    return date_list


def check_count(table, count, date, cursor):
    sql = RETRIVE_ID_NUMBER_SQL_TEMPLATE + '"' + date + '";'
    cursor.execute(sql.format(table))
    for ct in cursor:
        return int(ct[0]) == count


def check_log():
    pass
