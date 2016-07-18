# -*- coding: utf-8 -*-
import sys
import json
import time
import helper
import mysql.connector
import fetch_config as conf
from mysql.connector import errorcode


def run_insert(inserted_data, template, cursor, table):
    inserted_data.insert(0, table)
    try:
        if table is "SYSLOG":
            cursor.execute(template.format(inserted_data[0],
                                           inserted_data[1],
                                           inserted_data[2],
                                           inserted_data[3]))
        elif table is "RECORD":
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
            print("已存在，不再重复读取")
        else:
            print(err.msg)
        return False


def get_tradingtips_info(argv, cnx, cursor):
    POST_TIME = helper.get_current_time()

    if argv and len(argv) == 3:
        date_list = helper.generate_date_list(argv[1], argv[2])
    else:
        date_list = [POST_TIME]

    for fetch_date in date_list:
        count = 0
        if not helper.check_log(fetch_date, cursor, 1):
            cnx.commit()
            values = [{'publishDate': fetch_date, 'xxfcbj': 0},
                      {'publishDate': fetch_date, 'xxfcbj': 1}, ]
            for param in values:
                class_code = param['xxfcbj']
                try:
                    data_str = helper.read_data_str(
                        conf.TARGET['tradingtips'], param)
                except:
                    print('读取失败')
                data_json = json.loads(data_str[5:-1])
                for item in data_json:
                    type_code, type_name = item[
                        'typecode'], item['typename']
                    trading_list = item['tradingtipsList']
                    if len(trading_list) > 0:
                        for trading_item in trading_list:
                            count += 1
                            comp_code = trading_item['companycode']
                            comp_name = trading_item['companyname']
                            inserted_data = [type_code, type_name, comp_code,
                                             comp_name, class_code, fetch_date]
                            run_insert(inserted_data, conf.INSERT_TEMPLATE[
                                       'record'], cursor, "RECORD")
            is_success = helper.check_count(
                'RECORD', count, fetch_date, cursor)
            if is_success:
                print("{} 的数据已读取完毕 共{}条 \n".format(
                    fetch_date, count))
            inserted_data = ["1", str(is_success), fetch_date]
            run_insert(inserted_data, conf.INSERT_TEMPLATE['syslog'],
                       cursor, 'SYSLOG')
            cnx.commit()


if __name__ == '__main__':
    start_time = time.time()
    cnx, cursor = helper.connect_db()
    get_tradingtips_info(sys.argv, cnx, cursor)
    cnx.commit()
    cursor.close()
    cnx.close()
    end_time = time.time()
    print("获取交易提示数据总用时:", end_time - start_time)
