# -*- coding: utf-8 -*-
INSERT_TEMPLATE = {
    'recommend': '\
        INSERT INTO {}\
            (MAKER_NAME, MAKER_CODE, STOCK_CODE, STOCK_NAME, T_TYPE, QUOTED_DATE)\
        VALUES ("{}", "{}", "{}", "{}", "{}", "{}");',
    'make': '\
        INSERT INTO {}\
            (HOST, HOST_CODE,STOCK_CODE,STOCK_NAME, T_TYPE)\
        VALUES ("{}", "{}", "{}", "{}", "{}");',
    'maker': '\
        INSERT INTO {}\
            (MAKER_NAME, MAKER_CODE, MAKER_TYPE, RECNUM, MAKERNUM)\
        VALUES ("{}", "{}", "{}", {}, {});',
    'stat': '\
        INSERT INTO {}\
            (TYPE_NAME, QUOTED_COMP, DAILY_INCREASED, TOTAL_EQUITY, FLOW_EQUITY, STOCK_COUNT, AMOUNT, VOLUME, POST_DATE)\
        VALUES ("{}", {}, {}, {}, {}, {}, {}, {}, "{}");',
    'syslog': '\
        INSERT INTO {}\
            (MISSION_TYPE, STATUS, LOG_DATE)\
        VALUES ({}, "{}", "{}");',
    'record': '\
        INSERT INTO {}\
            (TYPE_CODE, TYPE_NAME, COMP_CODE, COMP_NAME, CLASS, POST_DATE)\
        VALUES ("{}", "{}", {}, "{}", {}, "{}");',
}

DROP_LOG_TEMPLATE = 'DELETE FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={};'
SELECT_LOG_TEMPLATE = 'SELECT STATUS FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={};'
DROP_PREV_DATA_TEMPLATE = 'DELETE FROM {} WHERE POST_DATE="{}";'

TYPE_DICT = {'T': '协议', 'M': '做市', 'C': '竞价', '1': '创新层', '0': '基础层'}

TARGET = {
    'recommend': '/makerInfoController/qryRecnumList.do',
    'maker': '/makerInfoController/listMakerInfo.do',
    'make': '/makerInfoController/qryMakenumList.do',
    'tradingtips': '/tradingtipsController/tradingtips.do',
    'stat': '/marketStatController/dailyReport.do'
}

BASE_URL = 'http://www.neeq.com.cn/'

RETRIEVE_ID_NUMBER_SQL_TEMPLATE = 'SELECT COUNT(*) FROM {} WHERE POST_DATE="{}";'
UPDATE_RECORD_TEMPLATE = 'UPDATE RECORD SET CLASS={} WHERE COMP_CODE="{}" AND TYPE_CODE="{}" AND POST_DATE="{}";'
ISOTIMEFORMAT = '%Y-%m-%d'
