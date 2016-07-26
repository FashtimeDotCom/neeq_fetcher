# -*- coding: utf-8 -*-
import time
import helper
import mysql.connector
import fetch_config as conf
from mysql.connector import errorcode


ENTITIES = {}

ENTITIES["MAKER"] = [
    "CREATE TABLE MAKER(\
        MAKER_NAME           VARCHAR(32) NOT NULL ,\
        MAKER_CODE           VARCHAR(32) NOT NULL,\
        MAKER_TYPE           VARCHAR(32),\
        RECNUM           INTEGER,\
        MAKERNUM          INTEGER,\
        FETCH_DATE      DATE,\
        LAST_UPDATED     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(MAKER_CODE, FETCH_DATE)\
    );"
]

ENTITIES["RECOMMEND"] = [
    "CREATE TABLE RECOMMEND(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        MAKER_NAME            VARCHAR(32) NOT NULL ,\
        MAKER_CODE            VARCHAR(32) NOT NULL,\
        STOCK_CODE            VARCHAR(32) NOT NULL ,\
        STOCK_NAME            VARCHAR(32) NOT NULL ,\
        T_TYPE            VARCHAR(32),\
        QUOTED_DATE       DATE,\
        FETCH_DATE      DATE,\
        LAST_UPDATED      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(ID)\
     );"
]

ENTITIES["MAKE"] = [
    "CREATE TABLE MAKE(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        HOST            VARCHAR(32) NOT NULL ,\
        HOST_CODE            VARCHAR(32) NOT NULL,\
        STOCK_CODE            VARCHAR(32) NOT NULL ,\
        STOCK_NAME            VARCHAR(32) NOT NULL ,\
        T_TYPE            VARCHAR(32),\
        FETCH_DATE      DATE,\
        LAST_UPDATED      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(ID)\
    );"
]


if __name__ == '__main__':
    cnx, cursor = helper.connect_db()
    helper.build_db(ENTITIES, cursor, cnx)
    time.sleep(1)
    cursor.close()
    cnx.close()
