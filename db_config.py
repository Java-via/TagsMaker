# _*_ coding: utf-8 _*_

# ----server----
# SDB_HOST = "101.200.174.172"
# SDB_DB = "data_apps"
# SDB_USER = "dba_apps"
# SDB_PWD = "mimadba_apps"
# SDB_CHARSET = "utf8"

import pymysql

# ----local----
DB_HOST = "192.168.2.43"
DB_APPDB = "app_db"
DB_DB = "my_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"


def conn_db():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur
