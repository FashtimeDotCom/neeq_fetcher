# -*- coding: utf-8 -*-
import sys
import json
import helper
import mysql.connector
from mysql.connector import errorcode


def run_insert(inserted_data, template, cursor, table):
    template = parse_template(template, inserted_data, table)
    try:
        cursor.execute(template)
        print("Inserted", table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


def parse_template(template, inserted_data, table):
    if table == "RECORD":
        template += '("' + inserted_data[0] + '","' + inserted_data[1] + '",' + str(inserted_data[
            2]) + ',"' + inserted_data[3] + '",' + str(inserted_data[4]) + ',"' +\
            inserted_data[5] + '","' + inserted_data[6] + '")'
    if table == "SYSLOG":
        template += '(' + inserted_data[0] + ',"' + \
            inserted_data[1] + '","' + inserted_data[2] + '");'

    return template


def main(argv):
    TARGET = 'tradingtipsController/tradingtips.do'
    POST_TIME = helper.get_current_time()
    INSERT_RECORD_TEMPLATE = '\
        INSERT INTO RECORD\
            (TYPE_CODE, TYPE_NAME, COMP_CODE, COMP_NAME, CLASS, COMMENT, POST_DATE)\
        VALUES '

    INSERT_SYSLOG_TEMPLATE = '\
        INSERT INTO SYSLOG\
            (MISSION_TYPE, STATUS, LOG_DATE)\
        VALUES '

    if argv:
        pass

    # xxfcbj解释：1对应创新层 0对应基础层
    values = [{'publishDate': POST_TIME, 'xxfcbj': 0},
              {'publishDate': POST_TIME, 'xxfcbj': 1}, ]

    cnx = mysql.connector.connect(user="stock", password="stock123",
                                  host="192.168.202.161",
                                  database="stockdb")
    cursor = cnx.cursor()
    count = 0
    for param in values:
        class_code = param['xxfcbj']
        try:
            data_str = helper.read_data_str(TARGET, param)
        except:
            print('failed')
        data_json = json.loads(data_str[5:-1])
        for item in data_json:
            type_code, type_name = item['typecode'], item['typename']
            # print("\n\n=======================", type_code, type_name)
            trading_list = item['tradingtipsList']
            if len(trading_list) > 0:
                for trading_item in trading_list:
                    count += 1
                    comp_code = trading_item['companycode']
                    comp_name = trading_item['companyname']
                    comment = trading_item['comments']
                    inserted_data = [type_code, type_name, comp_code, comp_name,
                                     class_code, comment, POST_TIME]
                    print(count, end='')
                    run_insert(inserted_data,
                               INSERT_RECORD_TEMPLATE, cursor, "RECORD")

    is_success = helper.check_count('RECORD', count, POST_TIME, cursor)
    # print(is_success)
    inserted_data = ["1", str(is_success), helper.get_current_time()]
    run_insert(inserted_data, INSERT_SYSLOG_TEMPLATE, cursor, 'SYSLOG')
    cnx.commit()

    # 关闭游标和连接
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main(sys.argv)
