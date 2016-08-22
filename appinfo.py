# _*_ coding: utf-8 _*_

"""
this model is aimed to save app info
"""

import logging
import pymysql
import time

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
ISOTIMEFORMAT='%Y-%m-%d %X'

# ----logging config----
logging.basicConfig(level=logging.DEBUG)


def save():
    """
    save app info
    :return: nothing
    """
    try:
        conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
        cur = conn.cursor()
        sql = "SELECT a_pkgname, a_name, a_description, a_classify, a_defaulttags, a_url, a_softgame " \
              "FROM t_apps_basic_united WHERE DATE(a_getdate) = '2016-08-06';"
        logging.debug("start to select from basic_united")
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        logging.debug("sucess to select from basic_united")
        conn.close()
        conn_l = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur_l = conn_l.cursor()
        sql_l_soft = "INSERT INTO t_tags_soft (t_pkgname, t_name, t_description, t_classify, " \
                     "t_defaulttags, t_url, t_softgame)  VALUES (%s, %s, %s, %s, %s, %s, %s);"
        sql_l_game = "INSERT INTO t_tags_game (t_pkgname, t_name, t_description, t_classify, " \
                     "t_defaulttags, t_url, t_softgame)  VALUES (%s, %s, %s, %s, %s, %s, %s);"
        logging.debug("start to insert")
        for app in apps:
            if app[6] == "soft":
                cur_l.execute(sql_l_soft, (app[0], app[1], app[2], app[3], app[4], app[5], app[6]))
            else:
                cur_l.execute(sql_l_game, (app[0], app[1], app[2], app[3], app[4], app[5], app[6]))
            conn_l.commit()
        logging.debug("success to insert")
        sql = "SELECT a_pkgname, a_picurl, a_softgame FROM t_apps_additional " \
              "WHERE a_getdate = '2016-08-12' AND a_source = 'yyb';"
        logging.debug("start to select pic")
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        sql_pic_soft = "UPDATE t_tags_soft SET t_picurl = %s WHERE t_pkgname = %s;"
        sql_pic_game = "UPDATE t_tags_game SET t_picurl = %s WHERE t_pkgname = %s;"
        for app in apps:
            if app[2] == "soft":
                logging.debug("%s update soft-%s", time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())), app[0])
                cur_l.execute(sql_pic_soft, (app[1], app[0]))
            else:
                logging.debug("%s update game-%s", time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())), app[0])
                cur_l.execute(sql_pic_game, (app[1], app[0]))
            conn_l.commit()
        logging.debug("success insert pic")
        return
    except Exception as excep:
        logging.error(Exception, ":", excep)
        return


def savepic():
    conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
    cur = conn.cursor()
    conn_l = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur_l = conn_l.cursor()
    sql = "SELECT a_pkgname, a_picurl, a_softgame FROM t_apps_additional " \
          "WHERE DATE(a_getdate) = '2016-08-12' AND a_source = 'yyb';"
    logging.debug("start to select from additional")
    cur.execute(sql)
    conn.commit()
    apps = cur.fetchall()
    sql_pic_soft = "UPDATE t_tags_soft SET t_picurl = %s WHERE t_pkgname = %s;"
    sql_pic_game = "UPDATE t_tags_game SET t_picurl = %s WHERE t_pkgname = %s;"
    logging.debug("start to update")
    for app in apps:
        if app[2] == "soft":
            logging.debug("%s update soft-%s",  time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())), app[0])
            cur_l.execute(sql_pic_soft, (app[1], app[0]))
        else:
            logging.debug("%s update game-%s", time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())), app[0])
            cur_l.execute(sql_pic_game, (app[1], app[0]))
        conn_l.commit()
    logging.debug("%s done", time.strftime(ISOTIMEFORMAT, time.gmtime(time.time())))
    return

if __name__ == "__main__":
    savepic()

