# -*- coding: utf-8 -*-
import sys
import json
import math
import helper
import mysql.connector
from mysql.connector import errorcode


def run_insert(inserted_data, template, cursor, table):
    inserted_data.insert(0, table)
    try:
        if table is "MAKER":
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
    pass


def get_make_info(maker_list, cursor, cnx):
    pass


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
        print("Makers information loaded successfully...")
        cnx.commit()
    else:
        print("Possibly something is wrong with loading makers information...")
    # get_rec_info(maker_list, cursor, cnx)
    # get_make_info(maker_list, cursor, cnx)


if __name__ == '__main__':
    cnx = mysql.connector.connect(user="stock", password="stock123",
                                  host="192.168.202.161",
                                  database="stockdb")
    cursor = cnx.cursor()
    main(cnx, cursor)
    cursor.close()
    cnx.close()
