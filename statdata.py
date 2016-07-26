# -*- coding: utf-8 -*-
import json
import sys
import time

import mysql.connector
from mysql.connector import errorcode

from config import fetch_config as conf
from helper import helper


def run_insert(inserted_data, template, cur, table):
    inserted_data.insert(0, table)
    try:
        if table is "STAT":
            cur.execute(template.format(inserted_data[0],
                                        inserted_data[1],
                                        inserted_data[2],
                                        inserted_data[3],
                                        inserted_data[4],
                                        inserted_data[5],
                                        inserted_data[6],
                                        inserted_data[7],
                                        inserted_data[8],
                                        inserted_data[9]))
        elif table is "SYSLOG":
            cur.execute(template.format(inserted_data[0],
                                        inserted_data[1],
                                        inserted_data[2],
                                        inserted_data[3]))
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("已存在，不再重复读取")
        else:
            print(err.msg)
        return False


def get_stat_info(argv):
    yesterday = helper.get_yesterday()

    if argv and len(argv) == 3:
        date_list = helper.generate_date_list(argv[1], argv[2])
    else:
        date_list = [yesterday]

    for fetch_date in date_list:
        param_date = helper.get_plain(fetch_date)
        param = {'HQJSRQ': param_date}
        count = 0
        if not helper.check_log(fetch_date, cursor, 2):
            cnx.commit()
            data_str = helper.read_data_str(conf.TARGET['stat'], param)
            data_json = json.loads(data_str[5:-1])
            for item in data_json:
                type_name = conf.TYPE_DICT[item['xxzrlx']]
                gpgsjs = item['gpgsjs']
                drxzjs = item['drxzjs']
                xxzgb = round(float(item['xxzgb']) / 100000000, 2)
                xxfxsgb = round(float(item['xxfxsgb']) / 100000000, 2)
                hqcjzs = item['hqcjzs']
                hqcjje = round(float(item['hqcjje']) / 10000, 2)
                hqcjsl = round(float(item['hqcjsl']) / 10000, 2)
                inserted_data = [type_name, gpgsjs, drxzjs,
                                 xxzgb, xxfxsgb, hqcjzs, hqcjje, hqcjsl, fetch_date]
                run_insert(inserted_data, conf.INSERT_TEMPLATE['stat'],
                           cursor, 'STAT')
                count += 1
            is_success = helper.check_count(
                'STAT', count, fetch_date, cursor)
            if is_success:
                print("{} 的数据已读取完毕 共{}条 \n".format(
                    fetch_date, count))
            inserted_data = ["2", str(is_success), fetch_date]
            run_insert(inserted_data, conf.INSERT_TEMPLATE['syslog'],
                       cursor, 'SYSLOG')
            cnx.commit()
        cnx.commit()


if __name__ == '__main__':
    start_time = time.time()
    cnx, cursor = helper.connect_db()
    get_stat_info(sys.argv)
    cursor.close()
    cnx.close()
    end_time = time.time()
    print("获取日报统计数据总用时:", end_time - start_time)
