# -*- coding: utf-8 -*-
import datetime
import time
import urllib.error
import urllib.parse
import urllib.request

import mysql.connector
from mysql.connector import errorcode

from config import fetch_config as conf
from db import db_config as db_conf


def connect_db():
    cnx = mysql.connector.connect(user=db_conf.DB_CONFIG['user'], password=db_conf.DB_CONFIG['password'],
                                  host=db_conf.DB_CONFIG['host'],
                                  database=db_conf.DB_CONFIG['database'])
    cursor = cnx.cursor()
    return [cnx, cursor]


def build_db(tables, cursor):
    for (table, sql) in tables.items():
        try:
            print("删除 {} 表... ".format(table), end="")
            cursor.execute("DROP TABLE {};".format(table))
            print("完成")
        except mysql.connector.Error:
            print("{} 表不存在，继续其他操作...".format(table))
        try:
            print("创建 {} 表... ".format(table), end="")
            cursor.execute(sql[0])
            print("完成")
            if len(sql) > 1:
                print("{} 表的索引正在创建...".format(table))
                cursor.execute(sql[1])
                print("完成")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("已存在，不再重复创建")
            else:
                print(err.msg)
        else:
            print("OK")


def drop_prev_data(fetch_date, cursor, table):
    sql = conf.DROP_PREV_DATA_TEMPLATE.format(table, fetch_date)
    cursor.execute(sql)


def drop_log(fetch_date, mission_code, cursor):
    sql = conf.DROP_LOG_TEMPLATE.format(fetch_date, mission_code)
    cursor.execute(sql)


def check_log(fetch_date, cursor, mission_code):
    sql = conf.SELECT_LOG_TEMPLATE.format(fetch_date, mission_code)
    cursor.execute(sql)
    status = "False"
    for st in cursor:
        if st is not None:
            status = st[0]
    if status == 'True':
        print('{} 数据已存在...'.format(fetch_date))
        return True
    print("正在删除可能重复存在的数据...")
    drop_prev_data(fetch_date, cursor, "STAT")
    drop_log(fetch_date, mission_code, cursor)
    return False


def read_data_str(target, values):
    try:
        headers = {'Type': 'POST'}
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # 转换 str 为 bytes
        req = urllib.request.Request(conf.BASE_URL + target, data, headers)
        with urllib.request.urlopen(req) as response:
            page = response.read().decode()
            if page:
                return page
    except:
        print('ERROR')


def get_current_time():
    return time.strftime(conf.ISOTIMEFORMAT, time.localtime())


def get_yesterday():
    return str(datetime.date.today() - datetime.timedelta(days=1))


def get_plain(date):
    year = date[0:4]
    month = date[5:7]
    day = date[-2:]
    return year + month + day


def get_formatted(date):
    return date[0:4] + '-' + date[4:6] + '-' + date[6:]


def generate_date_list(s, e):
    date_list = []
    start = datetime.datetime.strptime(s, '%Y-%m-%d')
    end = datetime.datetime.strptime(e, '%Y-%m-%d')
    while start <= end:
        date_list.append(start.strftime('%Y-%m-%d'))
        start += datetime.timedelta(days=1)
    return date_list


def check_count(table, count, date, cursor):
    sql = conf.RETRIEVE_ID_NUMBER_SQL_TEMPLATE.format(table, date)
    cursor.execute(sql.format(table))
    for ct in cursor:
        return int(ct[0]) == count
