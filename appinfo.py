# _*_ coding: utf-8 _*_

import pymysql
import functools
import operator
import logging

"""
different is url and picurl first choose yyb
"""

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

logging.basicConfig(level=logging.WARNING)


def insert_data(date):
    s_conn = pymysql.connect(host=SDB_HOST, db=SDB_DB, user=SDB_USER, passwd=SDB_PWD, charset=SDB_CHARSET)
    l_conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
    s_cur = s_conn.cursor()
    l_cur = l_conn.cursor()

    # get pkgname in t_tags_apps
    l_sql_pkg = "SELECT a_pkgname FROM t_tags_apps_test"
    l_cur.execute(l_sql_pkg)
    tag_pkg_list = (item[0] for item in l_cur.fetchall())

    # get install_sum TOP 20000
    s_sql_addi = "SELECT a_pkgname, a_pkgname_list, a_install_sum FROM t_apps_addi_united " \
                 "WHERE DATE(a_getdate) = %s ORDER BY a_install_sum DESC LIMIT 20000;"
    s_cur.execute(s_sql_addi, date)
    logging.debug("Addi select order by install_sum is over")

    for app in s_cur.fetchall():
        # get apps where pkgname is in pkgname_list of TOP 20000
        s_sql_basic = "SELECT a_pkgname, a_pkgname_list, a_name, a_url_list, a_picurl_list, a_description, " \
                      "a_classify, a_defaulttags, a_softgame FROM t_apps_basic_united WHERE a_pkgname IN (%s);"
        pkglist = get_string_split(app[1], split_chars=(' ', '\n'), is_remove_empty=True)
        in_p = ', '.join(list(map(lambda x: '%s', pkglist)))
        s_sql_basic = s_sql_basic % in_p
        s_cur.execute(s_sql_basic, pkglist)
        apps_basic = s_cur.fetchall()

        # format result
        if len(apps_basic) > 0:
            logging.debug("Basic select result example: %s", apps_basic[0])
        pkg = list()
        # length of app_basic equals 1 if select is right and then insert
        if len(apps_basic) == 1:
            item = list(apps_basic[0])
            url_list = get_string_split(item[3], split_chars=(" ", "\n"), is_remove_empty=True)
            url = url_list[0]
            for item_url in url_list[1:]:
                if "sj.qq.com" in item_url:
                    url = item_url

            picurl_list = get_string_split(item[4], split_chars=(" ", "\n"), is_remove_empty=True)
            picurl = picurl_list[0]
            for item_pic in picurl_list[1:]:
                if "pp.myapp.com" in item_pic:
                    picurl = item_pic
            item[3] = url
            item[4] = picurl
            for iapp in item:
                pkg.append(iapp)
            logging.debug("%s install is: %s", pkg[0], app[2])
            pkg.append(app[2])

            # check pkgname if already exist
            if pkg[0] not in tag_pkg_list:
                l_sql_tags = "INSERT INTO t_tags_apps_test (a_pkgname, a_pkgname_list, a_name, a_url, a_picurl, " \
                         "a_description, a_classify, a_defaulttags, a_softgame, a_install_sum) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                l_cur.execute(l_sql_tags, pkg)
                l_conn.commit()
                logging.debug("INSERT SUCCESS, row number=%s", l_cur.rowcount)
            else:
                logging.warning("%s is already exist", pkg[0])
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
