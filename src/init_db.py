# -*- coding: utf-8 -*-
import time
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

TABLES["SYSLOG"] = [
    "CREATE TABLE SYSLOG(\
        ID            INTEGER      NOT NULL AUTO_INCREMENT,\
        MISSION_TYPE  SMALLINT     NOT NULL,\
        LAST_UPDATED  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        STATUS        VARCHAR(16)  NOT NULL,\
        LOG_DATE      DATE         NOT NULL,\
        PRIMARY KEY (ID)\
    );"
]

cnx = mysql.connector.connect(user="stock", password="stock123",
                              host="192.168.202.161",
                              database="stockdb")
cursor = cnx.cursor()

for (table, sql) in TABLES.items():
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
