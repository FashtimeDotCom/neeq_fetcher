DB_CONFIG = {
    'user': 'stock',
    'password': 'stock123',
    'host': '192.168.202.161',
    'database': 'stockdb'
}

INSERT_TEMPLATE = {
    'recommend': '\
        INSERT INTO {}\
            (M_NAME, M_CODE, S_CODE, S_NAME, T_TYPE, GUAPAI_DATE)\
        VALUES ("{}", "{}", "{}", "{}", "{}", "{}");',
    'make': '\
        INSERT INTO {}\
            (HOST, HOST_CODE,S_CODE,S_NAME, T_TYPE)\
        VALUES ("{}", "{}", "{}", "{}", "{}");',
    'maker': '\
        INSERT INTO {}\
            (M_NAME, M_CODE, M_TYPE, RECNUM, MAKERNUM)\
        VALUES ("{}", "{}", "{}", {}, {});',
    'stat': '\
        INSERT INTO {}\
            (TYPE_NAME, GUAPAI, XINZENG, Z_GUBEN, LT_GUBEN, CJ_ZHISHU, CJ_JINE, CJ_SHULIANG, POST_DATE)\
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

DROP_LOG_TEMPLATE = 'DELETE FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={}'
SELECT_LOG_TEMPLATE = 'SELECT STATUS FROM SYSLOG WHERE LOG_DATE="{}" AND MISSION_TYPE={}'
DROP_PREV_DATA_TEMPLATE = 'DELETE FROM {} WHERE POST_DATE="{}"'

TYPE_DICT = {'T': '协议', 'M': '做市', 'C': '竞价', '1': '创新层', '0': '基础层'}

TARGET = {
    'recommend': '/makerInfoController/qryRecnumList.do',
    'maker': '/makerInfoController/listMakerInfo.do',
    'make': '/makerInfoController/qryMakenumList.do',
    'tradingtips': '/tradingtipsController/tradingtips.do',
    'stat': '/marketStatController/dailyReport.do'
}
