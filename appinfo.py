# _*_ coding: utf-8 _*_

import pymysql
import logging
from flask import jsonify

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

# ----local----
DB_HOST = "127.0.0.1"
DB_DB = "my_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"


def save():
    try:
        conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
        cur = conn.cursor()
        sql = "SELECT a_pkgname, a_name, a_description, a_classify, a_defaulttags, a_url, a_softgame " \
              "FROM t_apps_basic_united WHERE DATE(a_getdate) = '2016-07-30';"
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        conn.close()
        conn_l = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur_l = conn_l.cursor()
        sql_l = "INSERT INTO t_tags (t_pkgname, t_name, t_description, t_classify, " \
                "t_defaulttags, t_url, t_softgame)  VALUES (%s, %s, %s, %s, %s, %s, %s);"
        for app in apps:
            cur_l.execute(sql_l, (app[0], app[1], app[2], app[3], app[4], app[5], app[6]))
            conn_l.commit()
        return

    except Exception as e:
        logging.error(Exception, ":", e)
        return

if __name__ == "__main__":
    save()
