# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import datetime

BASE_URL = 'http://www.neeq.com.cn/'


# Trading tips SQL
RETRIVE_ID_NUMBER_SQL_TEMPLATE = 'SELECT COUNT(*) FROM {}\
                                    WHERE POST_DATE='


def drop_prev_data(fetch_date, cursor, table):
    DROP_PREV_DATA_TEMPLATE = 'DELETE FROM {} WHERE POST_DATE="{}"'
    sql = DROP_PREV_DATA_TEMPLATE.format(table, fetch_date)
    cursor.execute(sql)


def drop_log(fetch_date, mission_code, cursor):
    DROP_LOG_TEMPLATE = 'DELETE FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={}'
    sql = DROP_LOG_TEMPLATE.format(fetch_date, mission_code)
    cursor.execute(sql)


def check_log(fetch_date, cursor, mission_code):
    SELECT_LOG_TEMPLATE = 'SELECT STATUS FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={}'
    sql = SELECT_LOG_TEMPLATE.format(fetch_date, mission_code)
    cursor.execute(sql)
    status = "False"
    for st in cursor:
        if st is not None:
            status = st[0]
    if status == 'True':
        print('{} data already exists...'.format(fetch_date))
        return True
    print("Dropping possibly duplicate data...")
    drop_prev_data(fetch_date, cursor, "STAT")
    drop_log(fetch_date, mission_code, cursor)
    return False


def read_data_str(target, values):
    try:
        headers = {'Type': 'POST'}
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # 转换 str 为 bytes
        req = urllib.request.Request(BASE_URL + target, data, headers)
        with urllib.request.urlopen(req) as response:
            page = response.read().decode()
    except:
        print('ERROR')
    if page:
        return page


def get_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d'
    return time.strftime(ISOTIMEFORMAT, time.localtime())


def get_yesterday():
    return str(datetime.date.today() - datetime.timedelta(days=1))


def get_plain(date):
    year = date[0:4]
    month = date[5:7]
    day = date[-2:]
    return year + month + day


def generate_date_list(s, e):
    date_list = []
    start = datetime.datetime.strptime(s, '%Y-%m-%d')
    end = datetime.datetime.strptime(e, '%Y-%m-%d')
    while start <= end:
        date_list.append(start.strftime('%Y-%m-%d'))
        start += datetime.timedelta(days=1)
    return date_list


def generate_nonweekend_date_list(s, e):
    weekday_list = []
    date_list = generate_date_list(s, e)
    for item in date_list:
        date = datetime.datetime.strptime(item, '%Y-%m-%d')
        if date.isoweekday() > 0 and date.isoweekday() < 6:
            weekday_list.append(item)
    return weekday_list


def check_count(table, count, date, cursor):
    sql = RETRIVE_ID_NUMBER_SQL_TEMPLATE + '"' + date + '";'
    cursor.execute(sql.format(table))
    for ct in cursor:
        return int(ct[0]) == count
