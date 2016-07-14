# -*- coding: utf-8 -*-
import time
import mysql.connector
from mysql.connector import errorcode


TABLES = {}

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