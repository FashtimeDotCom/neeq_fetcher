DB_CONFIG = {
    'user': 'stock',
    'password': 'stock123456',
    'host': '192.168.202.166',
    'database': 'stockdb'
}

TABLES = dict()

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
        QUOTED_COMP       INTEGER,\
        DAILY_INCREASED       INTEGER,\
        TOTAL_EQUITY       INTEGER,\
        FLOW_EQUITY      INTEGER,\
        STOCK_COUNT     INTEGER,\
        AMOUNT       INTEGER,\
        VOLUME   INTEGER,\
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

TABLES["MAKER"] = [
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

TABLES["RECOMMEND"] = [
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

TABLES["MAKE"] = [
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
