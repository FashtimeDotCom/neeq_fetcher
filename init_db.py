# -*- coding: utf-8 -*-
from helper import helper
from db import db_config as db_conf

if __name__ == '__main__':
    cnx, cursor = helper.connect_db()
    helper.build_db(db_conf.TABLES, cursor, cnx)
    cursor.close()
    cnx.close()
