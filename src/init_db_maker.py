# -*- coding: utf-8 -*-
import time
import mysql.connector
from mysql.connector import errorcode


def build_db(DICT):
    for (table, sql) in DICT.items():
        try:
            print("Dropping table {}... ".format(table), end="")
            cursor.execute("DROP TABLE {};".format(table))
            print("OK")
        except:
            print("No table called {}...".format(table))
        try:
            print("Creating table {}... ".format(table), end="")
            cursor.execute(sql[0])
            print("OK")
            if len(sql) > 1:
                cursor.execute(sql[1])
                print("Indices for table {} have been created...".format(table))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    print("Tables created! Finish.")


ENTITIES = {}
RELATIONS = {}
ENTITIES["MAKER"] = [
    "CREATE TABLE MAKER(\
        NAME           VARCHAR(32) NOT NULL ,\
        M_CODE         INTEGER NOT NULL,\
        M_TYPE         VARCHAR(32),\
        RECNUM         INTEGER,\
        MAKENUM        INTEGER,\
        LAST_UPDATED   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(M_CODE)\
    );"
]

ENTITIES["STOCK"] = [
    "CREATE TABLE STOCK(\
        NAME            VARCHAR(32) NOT NULL ,\
        S_CODE          VARCHAR(32) NOT NULL,\
        LAST_UPDATED    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(S_CODE)\
    );"
]

ENTITIES["MAKERLOG"] = [
    "CREATE TABLE MAKERLOG(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        MISSION_TYPE  SMALLINT     NOT NULL,\
        LAST_UPDATED  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        STATUS        VARCHAR(16)  NOT NULL,\
        LOG_DATE      DATE         NOT NULL,\
        PRIMARY KEY (ID)\
    );"
]

RELATIONS["RECOMMEND"] = [
    "CREATE TABLE RECOMMEND(\
        S_CODE            VARCHAR(32) NOT NULL ,\
        M_CODE            VARCHAR(32) NOT NULL,\
        T_TYPE            VARCHAR(32),\
        GP_DATE           DATE,\
        LAST_UPDATED      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(S_CODE, M_CODE),\
        FOREIGN KEY(S_CODE) REFERENCES STOCK(S_CODE),\
        FOREIGN KEY(M_CODE) REFERENCES MAKER(M_CODE)\
     );"
]

RELATIONS["MAKE"] = [
    "CREATE TABLE MAKE(\
        S_CODE            VARCHAR(32) NOT NULL ,\
        M_CODE            VARCHAR(32) NOT NULL,\
        HOST              VARCHAR(32),\
        LAST_UPDATED      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        PRIMARY KEY(S_CODE, M_CODE),\
        FOREIGN KEY(S_CODE) REFERENCES STOCK(S_CODE),\
        FOREIGN KEY(M_CODE) REFERENCES MAKER(M_CODE)\
    );"
]


if __name__ == '__main__':
    cnx = mysql.connector.connect(user="stock", password="stock123",
                                  host="192.168.202.161",
                                  database="stockdb")
    cursor = cnx.cursor()
    build_db(ENTITIES)
    time.sleep(1)
    build_db(RELATIONS)
