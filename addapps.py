# _*_ coding: utf-8 _*_

import pymysql


DB_HOST = "127.0.0.1"
DB_DB = "my_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"


def addapps():
    conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, password=DB_PWD, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT t0.a_pkgname, t0.a_name, t0.a_description, t0.a_classify, t0.a_defaulttags, t0.a_url, t0.a_softgame " \
		  "FROM (SELECT a_pkgname, a_name, a_description, a_classify, a_defaulttags, a_url, a_softgame, a_getdate " \
		  "FROM t_apps_basic ) t0, (SELECT DATE_SUB(date_sub(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY),INTERVAL 2 DAY)" \
		  " AS sat) t1 WHERE DATE(t0.a_getdate) = t1.sat LIMIT 10;"

    return
