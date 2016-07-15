# -*- coding: utf-8 -*-
import sys
import json
import helper
import mysql.connector
import fetch_config as conf
from mysql.connector import errorcode


def run_insert(inserted_data, template, cursor, table):
    sql = parse_template(template, inserted_data, table)
    try:
        cursor.execute(sql)
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
        return False


def parse_template(template, inserted_data, table):
    if table == "RECORD":
        template += '("' + inserted_data[0] + '","' + inserted_data[1] + '",' + str(inserted_data[
            2]) + ',"' + inserted_data[3] + '",' + str(inserted_data[4]) + ',"' + inserted_data[5] + '")'
    if table == "SYSLOG":
        template += '(' + inserted_data[0] + ',"' + \
            inserted_data[1] + '","' + inserted_data[2] + '");'
    return template


def main(argv):
    TARGET = 'tradingtipsController/tradingtips.do'
    POST_TIME = helper.get_current_time()
    INSERT_RECORD_TEMPLATE = '\
        INSERT INTO RECORD\
            (TYPE_CODE, TYPE_NAME, COMP_CODE, COMP_NAME, CLASS, POST_DATE)\
        VALUES '

    INSERT_SYSLOG_TEMPLATE = '\
        INSERT INTO SYSLOG\
            (MISSION_TYPE, STATUS, LOG_DATE)\
        VALUES '

    cnx = mysql.connector.connect(user=conf.DB_CONFIG['user'], password=conf.DB_CONFIG['password'],
                                  host=conf.DB_CONFIG['host'],
                                  database=conf.DB_CONFIG['database'])
    cursor = cnx.cursor()

    if argv and len(argv) == 3:
        date_list = helper.generate_date_list(argv[1], argv[2])
    else:
        date_list = [POST_TIME]

    for fetch_date in date_list:
        count = 0

        if not helper.check_log(fetch_date, cursor, 1):
            cnx.commit()
            # print("正在读读取 {} 的数据...".format(fetch_date))
            # xxfcbj解释：1对应创新层 0对应基础层
            values = [{'publishDate': fetch_date, 'xxfcbj': 0},
                      {'publishDate': fetch_date, 'xxfcbj': 1}, ]

            for param in values:
                class_code = param['xxfcbj']
                try:
                    data_str = helper.read_data_str(TARGET, param)
                except:
                    print('读取失败')
                data_json = json.loads(data_str[5:-1])
                for item in data_json:
                    type_code, type_name = item[
                        'typecode'], item['typename']
                    # print("\n\n=======================",
                    #   type_code, type_name)
                    trading_list = item['tradingtipsList']
                    if len(trading_list) > 0:
                        for trading_item in trading_list:
                            count += 1
                            comp_code = trading_item['companycode']
                            comp_name = trading_item['companyname']
                            # print("{} - {} 正在录入".format(comp_name,
                            # comp_code))
                            inserted_data = [type_code, type_name, comp_code, comp_name,
                                             class_code, fetch_date]
                            if run_insert(inserted_data, INSERT_RECORD_TEMPLATE, cursor, "RECORD"):
                                # print(
                                #     "{} - {} 录入成功".format(comp_name, comp_code))
                                pass
            is_success = helper.check_count(
                'RECORD', count, fetch_date, cursor)
            if is_success:
                print("{} 的数据已读取完毕 共{}条 \n".format(
                    fetch_date, count))
            inserted_data = ["1", str(is_success), fetch_date]
            run_insert(inserted_data, INSERT_SYSLOG_TEMPLATE,
                       cursor, 'SYSLOG')
            cnx.commit()

    # 关闭游标和连接
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main(sys.argv)
