# -*- coding: utf-8 -*-
import sys
import json
import time
import math
import helper
import mysql.connector
import fetch_config as conf
from mysql.connector import errorcode


def run_insert(inserted_data, template, cursor, table):
    inserted_data.insert(0, table)
    try:
        if table is "MAKER" or table is "MAKE":
            cursor.execute(template.format(inserted_data[0],
                                           inserted_data[1],
                                           inserted_data[2],
                                           inserted_data[3],
                                           inserted_data[4],
                                           inserted_data[5]))
        elif table is "RECOMMEND":
            cursor.execute(template.format(inserted_data[0],
                                           inserted_data[1],
                                           inserted_data[2],
                                           inserted_data[3],
                                           inserted_data[4],
                                           inserted_data[5],
                                           inserted_data[6]))
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
        return False


def get_rec_info(maker_list, cursor, cnx):
    TARGET = '/makerInfoController/qryRecnumList.do'
    INSERT_RECOMMEND_TEMPLATE = '\
        INSERT INTO {}\
            (M_NAME, M_CODE, S_CODE, S_NAME, T_TYPE, GUAPAI_DATE)\
        VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'
    TYPE_DICT = {'T': '协议', 'M': '做市', 'C': '竞价'}

    cursor.execute('DELETE FROM RECOMMEND;')
    cnx.commit()

    for maker in maker_list:
        values = []
        count = 0
        data_str = helper.read_data_str(TARGET, {'makerName': maker[0]})
        data_json = json.loads(data_str[5:-1])
        total = data_json[0]['totalElements']
        total_page = data_json[0]['totalPages']
        for i in range(0, total_page):
            values.append({'page': i, 'makerName': maker[0]})
        for val in values:
            data_str = helper.read_data_str(TARGET, val)
            data_json = json.loads(data_str[5:-1])
            rec_list_content = data_json[0]['content']
            for rec in rec_list_content:
                m_name, m_code = maker
                s_code = rec['companyno']
                s_name = rec['companyName']
                t_type = TYPE_DICT[rec['zrlx']]
                gp = helper.get_formatted(rec['gprq'])
                inserted_data = [m_name, m_code, s_code, s_name, t_type, gp]
                run_insert(inserted_data, INSERT_RECOMMEND_TEMPLATE,
                           cursor, "RECOMMEND")
                count += 1
        if count == int(total):
            cnx.commit()
        else:
            print(maker[0], "的推荐数据读取失败")


def get_make_info(maker_list, cursor, cnx):
    TARGET = '/makerInfoController/qryMakenumList.do'
    INSERT_MAKE_TEMPLATE = '\
        INSERT INTO {}\
            (HOST, HOST_CODE,S_CODE,S_NAME, T_TYPE)\
        VALUES ("{}", "{}", "{}", "{}", "{}");'
    TYPE_DICT = {'T': '协议', 'M': '做市', 'C': '竞价'}

    cursor.execute('DELETE FROM MAKE;')
    cnx.commit()
    for maker in maker_list:
        values = []
        count = 0
        data_str = helper.read_data_str(TARGET, {'stkaccout': maker[0]})
        data_json = json.loads(data_str[5:-1])
        total = data_json[0]['totalElements']
        total_page = data_json[0]['totalPages']
        for i in range(0, total_page):
            values.append({'page': i, 'stkaccout': maker[0]})
        for val in values:
            data_str = helper.read_data_str(TARGET, val)
            data_json = json.loads(data_str[5:-1])
            make_list_content = data_json[0]['content']
            for make in make_list_content:
                m_name, m_code = maker
                s_code = make['companyno']
                s_name = make['companyName']
                gp = helper.get_formatted(make['gprq'])
                t_type = TYPE_DICT[make['zrlx']]
                inserted_data = [m_name, m_code, s_code, s_name, gp, t_type]
                run_insert(inserted_data, INSERT_MAKE_TEMPLATE,
                           cursor, "MAKE")
                count += 1
        if count == int(total):
            cnx.commit()
        else:
            print(maker[0], "的做市数据读取失败")


def main(cnx, cursor):
    TARGET = '/makerInfoController/listMakerInfo.do'
    INSERT_MAKER_TEMPLATE = '\
        INSERT INTO {}\
            (M_NAME, M_CODE, M_TYPE, RECNUM, MAKERNUM)\
        VALUES ("{}", "{}", "{}", {}, {});'

    cursor.execute('DELETE FROM MAKER;')
    cnx.commit()

    maker_list = []
    count = 0
    values = []
    data_str = helper.read_data_str(TARGET, {})
    data_json = json.loads(data_str[5:-1])
    total = data_json[0]['totalElements']
    total_page = math.ceil(total / 20)

    for i in range(0, total_page):
        values.append({'page': i})

    for param in values:
        try:
            data_str = helper.read_data_str(TARGET, param)
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
            inserted_data = [m_name, m_code, m_type, recnum, makernum]
            maker_list.append([m_name, m_code])
            run_insert(inserted_data, INSERT_MAKER_TEMPLATE,
                       cursor, "MAKER")
    if count == int(total):
        cnx.commit()
        get_rec_info(maker_list, cursor, cnx)
        get_make_info(maker_list, cursor, cnx)
    else:
        print("做市商信息读取出错...")


if __name__ == '__main__':
    start_time = time.time()
    cnx = mysql.connector.connect(user="stock", password="stock123",
                                  host="192.168.202.161",
                                  database="stockdb")
    cursor = cnx.cursor()
    main(cnx, cursor)
    cursor.close()
    cnx.close()
    end_time = time.time()
    print("Total time:", end_time - start_time)
