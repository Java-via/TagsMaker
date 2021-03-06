# _*_ coding: utf-8 _*_

import pymysql
import functools
import operator
import logging

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

logging.basicConfig(level=logging.DEBUG)


def insert_data(date):
    s_conn = pymysql.connect(host=SDB_HOST, db=SDB_DB, user=SDB_USER, passwd=SDB_PWD, charset=SDB_CHARSET)
    l_conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
    s_cur = s_conn.cursor()
    l_cur = l_conn.cursor()
    l_sql_exit = "SELECT a_pkgname FROM t_tags_apps"
    l_cur.execute(l_sql_exit)
    tags_pkgname_list = (item[0] for item in l_cur.fetchall())
    logging.debug("TAGS_PKGNAME_LIST: %s", tags_pkgname_list)
    s_sql_addi = "SELECT a_pkgname, a_pkgname_list, a_install_sum FROM t_apps_addi_united " \
                 "WHERE DATE(a_getdate) = %s ORDER BY a_install_sum DESC;"

    s_cur.execute(s_sql_addi, date)
    # logging.debug("Addi select order by install_sum is over")
    for app in s_cur.fetchall():
        s_sql_basic = "SELECT a_pkgname, a_pkgname_list, a_name, a_url, a_picurl, a_description, a_classify, " \
                      "a_defaulttags, a_softgame FROM t_apps_basic_united WHERE a_pkgname IN (%s);"
        pkglist = get_string_split(app[1], split_chars=(' ', '\n'), is_remove_empty=True)
        # logging.debug("Here app is: %s", pkglist[1])
        # logging.debug("Pkglist is that: %s", pkglist)
        in_p = ', '.join(list(map(lambda x: '%s', pkglist)))
        s_sql_basic = s_sql_basic % in_p
        s_cur.execute(s_sql_basic, pkglist)
        # logging.debug("Basic select a_pkgname_list is over")
        apps_basic = s_cur.fetchall()
        # logging.debug("Basic select result example: %s", apps_basic[0])
        pkg = list()
        if len(apps_basic) == 1:
            # logging.debug("Basic select is right")
            for item in apps_basic[0]:
                pkg.append(item)
            # logging.debug("%s install is: %s", pkg[0], app[2])
            pkg.append(app[2])
            # logging.debug("PKG IS len()=%d, :%s", len(pkg), pkg)
            if pkg[0] in tags_pkgname_list:
                logging.warning("%s is already exist in t_tags_apps", pkg[0])
            else:
                l_sql_tags = "INSERT INTO t_tags_apps (a_pkgname, a_pkgname_list, a_name, a_url, a_picurl, " \
                             "a_description, a_classify, a_defaulttags, a_softgame, a_install_sum) " \
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                l_cur.execute(l_sql_tags, pkg)
                l_conn.commit()
                # logging.debug("CHECK error: %s", l_cur.insertSql)
                logging.debug("INSERT SUCCESS, row number=%s", l_cur.rowcount)
        else:
            logging.error("Basic select error in: %s", pkglist)


def get_string_split(string, split_chars=(" ", "\t", ","), is_remove_empty=False):
    """
    get string list by splitting string from split_chars
    """
    assert len(split_chars) >= 2, "get_string_split: len(split_chars) must >= 2"
    string_list = []
    for char in split_chars:
        if string_list:
            string_list = functools.reduce(operator.add, [item.split(char) for item in string_list], [])
        else:
            string_list = string.split(char)
    return string_list if not is_remove_empty else [item.strip() for item in string_list if item.strip()]


if __name__ == "__main__":
    insert_data("2016-08-18")
