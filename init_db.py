# -*- coding: utf-8 -*-
from db import db_config as db_conf
from helper import helper

if __name__ == '__main__':
    cnx, cursor = helper.connect_db()
    helper.build_db(db_conf.TABLES, cursor)
    cursor.close()
    cnx.close()
