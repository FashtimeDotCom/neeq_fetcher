# -*- coding: utf-8 -*-
import time
import helper
import mysql.connector
from mysql.connector import errorcode


TABLES = {}

TABLES["RECORD"] = [
    "CREATE TABLE RECORD(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        TYPE_CODE     VARCHAR(8)   NOT NULL,\
        TYPE_NAME     VARCHAR(32)  NOT NULL,\
        COMP_CODE     INTEGER      NOT NULL,\
        COMP_NAME     VARCHAR(16)  NOT NULL,\
        CLASS         SMALLINT     NOT NULL,\
        POST_DATE     DATE,\
        LAST_UPDATED  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY (ID)\
    );",
    "CREATE INDEX record_date_index ON RECORD (POST_DATE);CREATE INDEX company_class_index ON RECORD (CLASS);"
]

TABLES["STAT"] = [
    "CREATE TABLE STAT(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        TYPE_NAME     VARCHAR(32)  NOT NULL,\
        GUAPAI        INTEGER,\
        XINZENG       INTEGER,\
        Z_GUBEN       INTEGER,\
        LT_GUBEN      INTEGER,\
        CJ_ZHISHU     INTEGER,\
        CJ_JINE       INTEGER,\
        CJ_SHULIANG   INTEGER,\
        POST_DATE     DATE,\
        LAST_UPDATED  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY (ID)\
    );",
    "CREATE INDEX stat_date_index ON RECORD (POST_DATE);"
]

TABLES["SYSLOG"] = [
    "CREATE TABLE SYSLOG(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        MISSION_TYPE  SMALLINT     NOT NULL,\
        LAST_UPDATED  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        STATUS        VARCHAR(16)  NOT NULL,\
        LOG_DATE      DATE         NOT NULL,\
        PRIMARY KEY (ID)\
    );",
    "CREATE INDEX mission_type_index ON SYSLOG (MISSION_TYPE);"
]


if __name__ == '__main__':
    cnx = mysql.connector.connect(user="stock", password="stock123",
                                  host="192.168.202.161",
                                  database="stockdb")
    cursor = cnx.cursor()
    helper.build_db(TABLES, cursor, cnx)
    time.sleep(1)
    cursor.close()
    cnx.close()
