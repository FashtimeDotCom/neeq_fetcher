import mysql.connector
from mysql.connector import errorcode


TABLES = {}

TABLES["RECORD"] = "\
    CREATE TABLE RECORD(\
       TYPE_CODE    SMALLINT     NOT NULL,\
       TYPE_NAME    VARCHAR(64)  NOT NULL,\
       COMP_CODE    VARCHAR(12)  NOT NULL,\
       COMP_NAME    VARCHAR(32)  NOT NULL,\
       CLASS        VARCHAR(12)  NOT NULL,\
       COMMENT      VARCHAR(128),\
       RECORD_DATE  DATE,\
       GET_DATE     TIMESTAMP,\
       PRIMARY KEY(COMP_CODE)\
    );"


cnx = mysql.connector.connect(user="stock", password="stock123",
                              host="192.168.202.161",
                              database="stockdb")
cursor = cnx.cursor()

for (table, sql) in TABLES.items():
    try:
        print("Dropping table {}... ".format(table), end="")
        cursor.execute("DROP TABLE {};".format(table))
        print("OK")
        print("Creating table {}... ".format(table), end="")
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

print("Tables created! Finish.")
