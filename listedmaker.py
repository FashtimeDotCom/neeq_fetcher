# -*- coding: utf-8 -*-
import json
import math
import time

import mysql.connector
from mysql.connector import errorcode

from config import fetch_config as conf
from helper import helper


def run_insert(inserted_data, template, cursor, table):
    inserted_data.insert(0, table)
    try:
        if table is "MAKER" or table is "MAKE":
            cursor.execute(template.format(inserted_data[0],
                                           inserted_data[1],
                                           inserted_data[2],
                                           inserted_data[3],
                                           inserted_data[4],
                                           inserted_data[5],
                                           inserted_data[6]))
        elif table is "RECOMMEND":
            cursor.execute(template.format(inserted_data[0],
                                           inserted_data[1],
                                           inserted_data[2],
                                           inserted_data[3],
                                           inserted_data[4],
                                           inserted_data[5],
                                           inserted_data[6],
                                           inserted_data[7]))
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("已存在，不再重复读取")
        else:
            print(err.msg)
        return False


def get_rec_info(maker_list, cursor, cnx):
    for maker in maker_list:
        print('*', end="")
        values = []
        count = 0
        data_str = helper.read_data_str(
            conf.TARGET['recommend'], {'makerName': maker[0]})
        data_json = json.loads(data_str[5:-1])
        total = data_json[0]['totalElements']
        total_page = data_json[0]['totalPages']
        for i in range(0, total_page):
            values.append({'page': i, 'makerName': maker[0]})
        for val in values:
            data_str = helper.read_data_str(conf.TARGET['recommend'], val)
            data_json = json.loads(data_str[5:-1])
            rec_list_content = data_json[0]['content']
            for rec in rec_list_content:
                m_name, m_code = maker
                s_code = rec['companyno']
                s_name = rec['companyName']
                t_type = conf.TYPE_DICT[rec['zrlx']]
                gp = helper.get_formatted(rec['gprq'])
                inserted_data = [m_name, m_code, s_code,
                                 s_name, t_type, gp, helper.get_current_time()]
                run_insert(inserted_data, conf.INSERT_TEMPLATE['recommend'],
                           cursor, "RECOMMEND")
                count += 1
        if count == int(total):
            cnx.commit()
        else:
            print(maker[0], "的推荐数据读取失败")


def get_make_info(maker_list, cursor, cnx):
    cursor.execute('DELETE FROM MAKE;')
    cnx.commit()

    for maker in maker_list:
        print('*', end="")
        values = []
        count = 0
        data_str = helper.read_data_str(
            conf.TARGET['make'], {'stkaccout': maker[0]})
        data_json = json.loads(data_str[5:-1])
        total = data_json[0]['totalElements']
        total_page = data_json[0]['totalPages']
        for i in range(0, total_page):
            values.append({'page': i, 'stkaccout': maker[0]})
        for val in values:
            data_str = helper.read_data_str(conf.TARGET['make'], val)
            data_json = json.loads(data_str[5:-1])
            make_list_content = data_json[0]['content']
            for make in make_list_content:
                m_name, m_code = maker
                s_code = make['companyno']
                s_name = make['companyName']
                gp = helper.get_formatted(make['gprq'])
                t_type = conf.TYPE_DICT[make['zrlx']]
                inserted_data = [m_name, m_code, s_code,
                                 s_name, gp, t_type, helper.get_current_time()]
                run_insert(inserted_data, conf.INSERT_TEMPLATE['make'],
                           cursor, "MAKE")
                count += 1
        if count == int(total):
            cnx.commit()
        else:
            print(maker[0], "的做市数据读取失败")


def get_maker_info(cnx, cursor):
    cursor.execute('DELETE FROM MAKER;')
    cnx.commit()

    maker_list = []
    count = 0
    values = []
    data_str = helper.read_data_str(conf.TARGET['maker'], {})
    data_json = json.loads(data_str[5:-1])
    total = data_json[0]['totalElements']
    total_page = math.ceil(total / 20)

    for i in range(0, total_page):
        values.append({'page': i})

    for param in values:
        try:
            data_str = helper.read_data_str(conf.TARGET['maker'], param)
        except:
            print('读取失败')
            continue
        data_json = json.loads(data_str[5:-1])
        maker_list_content = data_json[0]['content']
        for maker in maker_list_content:
            count += 1
            m_name = maker['makername']
            m_code = maker['stkaccout']
            m_type = maker['makertype']
            recnum = maker['recnum']
            makernum = maker['makernum']
            inserted_data = [m_name, m_code, m_type,
                             recnum, makernum, helper.get_current_time()]
            maker_list.append([m_name, m_code])
            run_insert(inserted_data, conf.INSERT_TEMPLATE['maker'],
                       cursor, "MAKER")
        print('*', end="")
    if count == int(total):
        cnx.commit()
        get_rec_info(maker_list, cursor, cnx)
        get_make_info(maker_list, cursor, cnx)
    else:
        print("做市商信息读取出错...")


if __name__ == '__main__':
    start_time = time.time()
    cnx, cursor = helper.connect_db()
    get_maker_info(cnx, cursor)
    cursor.close()
    cnx.close()
    end_time = time.time()
    print("获取做市商数据总用时:", end_time - start_time)
