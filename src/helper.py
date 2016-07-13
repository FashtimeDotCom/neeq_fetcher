# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time

BASE_URL = 'http://www.neeq.com.cn/'


# Trading tips SQL
RETRIVE_ID_NUMBER_SQL_TEMPLATE = 'SELECT COUNT(ID) FROM {}\
                                      WHERE POST_DATE='


def read_data_str(target, values):
    try:
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # 转换 str 为 bytes
        req = urllib.request.Request(BASE_URL + target, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read().decode()
    except:
        print("ERROR")
    if the_page:
        return the_page


def get_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d'
    return time.strftime(ISOTIMEFORMAT, time.localtime())


def check_count(table, count, date, cursor):
    sql = RETRIVE_ID_NUMBER_SQL_TEMPLATE + '"' + date + '"'
    cursor.execute(sql.format(table))
    for ct in cursor:
        print(ct[0])
    return int(ct[0]) == count


def check_log():
    pass
