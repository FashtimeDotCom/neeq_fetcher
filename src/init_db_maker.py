# -*- coding: utf-8 -*-
import time
import helper
import mysql.connector
import fetch_config as conf
from mysql.connector import errorcode


ENTITIES = {}

ENTITIES["MAKER"] = [
    "CREATE TABLE MAKER(\
        M_NAME           VARCHAR(32) NOT NULL ,\
        M_CODE           VARCHAR(32) NOT NULL,\
        M_TYPE           VARCHAR(32),\
        RECNUM           INTEGER,\
        MAKERNUM          INTEGER,\
        LAST_UPDATED     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(M_CODE)\
    );"
]

ENTITIES["RECOMMEND"] = [
    "CREATE TABLE RECOMMEND(\
        ID                INTEGER     NOT NULL AUTO_INCREMENT,\
        M_NAME            VARCHAR(32) NOT NULL ,\
        M_CODE            VARCHAR(32) NOT NULL,\
        S_CODE            VARCHAR(32) NOT NULL ,\
        S_NAME            VARCHAR(32) NOT NULL ,\
        T_TYPE            VARCHAR(32),\
        GUAPAI_DATE       DATE,\
        LAST_UPDATED      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(ID)\
     );"
]

ENTITIES["MAKE"] = [
    "CREATE TABLE MAKE(\
        ID                INTEGER     NOT NULL AUTO_INCREMENT,\
        HOST            VARCHAR(32) NOT NULL ,\
        HOST_CODE            VARCHAR(32) NOT NULL,\
        S_CODE            VARCHAR(32) NOT NULL ,\
        S_NAME            VARCHAR(32) NOT NULL ,\
        T_TYPE            VARCHAR(32),\
        LAST_UPDATED      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(ID)\
    );"
]


if __name__ == '__main__':
    cnx = mysql.connector.connect(user=conf.DB_CONFIG['user'], password=conf.DB_CONFIG['password'],
                                  host=conf.DB_CONFIG['host'],
                                  database=conf.DB_CONFIG['database'])
    cursor = cnx.cursor()
    helper.build_db(ENTITIES, cursor, cnx)
    time.sleep(1)
    cursor.close()
    cnx.close()
