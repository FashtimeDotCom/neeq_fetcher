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
        if table is 'SYSLOG':
            cur.execute(template.format(inserted_data[0],
                                        inserted_data[1],
                                        inserted_data[2],
                                        inserted_data[3]))
        elif table is 'RECORD':
            cur.execute(template.format(inserted_data[0],
                                        inserted_data[1],
                                        inserted_data[2],
                                        inserted_data[3],
                                        inserted_data[4],
                                        inserted_data[5],
                                        inserted_data[6]))
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('已存在，不再重复读取')
        else:
            print(err.msg)
        return False


def run_update(updated_data, template, cur):
    try:
        cur.execute(template.format(updated_data[0],
                                    updated_data[1],
                                    updated_data[2],
                                    updated_data[3]))
        return True
    except mysql.connector.Error as err:
        print(err.msg)
    return False


def get_trading_tips_info(argv, conn, cur):
    cur_date = helper.get_current_time()
    if argv and len(argv) == 3:
        date_list = helper.generate_date_list(argv[1], argv[2])
    else:
        date_list = [cur_date]

    for fetch_date in date_list:
        count = 0
        if not helper.check_log(fetch_date, cur, 1):
            param = {'publishDate': fetch_date}
            try:
                data_str = helper.read_data_str(
                    conf.TARGET['tradingtips'], param)
            except SyntaxError:
                print('读取失败')
                continue
            data_json = json.loads(data_str[5:-1])
            for item in data_json:
                type_code, type_name = item['typecode'], item['typename']
                trading_list = item['tradingtipsList']
                if len(trading_list) > 0:
                    for trading_item in trading_list:
                        count += 1
                        comp_code = trading_item['companycode']
                        comp_name = trading_item['companyname']
                        inserted_data = [type_code, type_name, comp_code,
                                         comp_name, 9, fetch_date]
                        run_insert(inserted_data,
                                   conf.INSERT_TEMPLATE['record'],
                                   cur, "RECORD")
            conn.commit
            update_class(fetch_date, cur, conn)
            is_success = helper.check_count(
                'RECORD', count, fetch_date, cur)
            if is_success:
                print('{} 的数据已读取完毕 共{}条 \n'.format(
                    fetch_date, count))
            inserted_data = ['1', str(is_success), fetch_date]
            run_insert(inserted_data, conf.INSERT_TEMPLATE['syslog'],
                       cur, 'SYSLOG')
            conn.commit()


def update_class(f_date, cur, conn):
    values = [{'publishDate': f_date, 'xxfcbj': 0},
              {'publishDate': f_date, 'xxfcbj': 1}, ]
    for param in values:
        try:
            data_str = helper.read_data_str(
                conf.TARGET['tradingtips'], param)
        except:
            print('读取失败')
            continue
        data_json = json.loads(data_str[5:-1])
        for item in data_json:
            type_code = item['typecode']
            trading_list = item['tradingtipsList']
            if len(trading_list) > 0:
                for trading_item in trading_list:
                    comp_code = trading_item['companycode']
                    updated_data = [param['xxfcbj'], comp_code, type_code, f_date]
                    run_update(updated_data, conf.UPDATE_RECORD_TEMPLATE, cur)
                    conn.commit()


if __name__ == '__main__':
    start_time = time.time()
    cnx, cursor = helper.connect_db()
    get_trading_tips_info(sys.argv, cnx, cursor)
    cnx.commit()
    cursor.close()
    cnx.close()
    end_time = time.time()
    print('获取交易提示数据总用时:', end_time - start_time)
