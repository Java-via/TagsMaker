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
    s_sql_addi = "SELECT a_pkgname, a_pkgname_list, a_install_sum FROM t_apps_addi_united " \
                 "WHERE DATE(a_getdate) = %s ORDER BY a_install_sum DESC LIMIT 20000;"
    s_cur.execute(s_sql_addi, date)
    logging.debug("Addi select order by install_sum is over")
    for app in s_cur.fetchall():
        s_sql_basic = "SELECT a_pkgname, a_pkgname_list, a_name, a_url, a_picurl, a_description, a_classify, " \
                      "a_defaulttags, a_softgame FROM t_apps_basic_united WHERE a_pkgname IN (%s);"
        pkglist = get_string_split(app[1], split_chars=(' ', '\n'), is_remove_empty=True)
        logging.debug("Here app is: %s", pkglist[0])
        logging.debug("Pkglist is that: %s", pkglist)
        in_p = ', '.join(list(map(lambda x: '%s', pkglist)))
        s_sql_basic = s_sql_basic % in_p
        s_cur.execute(s_sql_basic, pkglist)
        logging.debug("Basic select a_pkgname_list is over")
        apps_basic = s_cur.fetchall()
        if len(apps_basic) > 0:
            logging.debug("Basic select result example: %s", apps_basic[0])
        pkg = list()
        if len(apps_basic) == 1:
            logging.debug("Basic select is right")
            for item in apps_basic[0]:
                pkg.append(item)
            logging.debug("%s install is: %s", pkg[0], app[2])
            pkg.append(app[2])
            logging.debug("PKG IS len()=%d, :%s", len(pkg), pkg)
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
    # l_conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
    # cur = l_conn.cursor()
    # l_sql_tags = "INSERT INTO t_tags_apps (a_pkgname, a_pkgname_list, a_name, a_url, a_picurl, " \
    #              "a_description, a_classify, a_defaulttags, a_softgame, a_install_sum) " \
    #              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # print("===1===")
    # cur.execute(l_sql_tags, ('com.baidu.searchbox', 'com.baidu.searchbox\ncom.baidu.searchbox\ncom.baidu.searchbox\ncom.baidu.searchbox', '手机百度', 'http://www.wandoujia.com/apps/com.baidu.searchbox', 'http://img.wdjimg.com/mms/icon/v1/8/1f/6d89947d237fbcf80fc0c35ae3b1c1f8_256_256.png', '【软件介绍】手机百度日活过亿，是目前国内活跃用户TOP3的App，依托百度家族特有资源及优势技术，随时随地为用户找到所求，解决所需。【搜索功能】手机百度根据用户行为特征，基于情景建模，大数据分析，智能语义匹配等优势技术 ，为用户提供精确，智能检索结果及相关内容。用户还可以通过语音、图像、扫码等多维输入方式，更便捷的获取优质内容。【兴趣订阅】基于Profile挖掘与个性订制的信息服务，我们的用户可以随时随地获取自己感兴趣的内容。从天气预报到时事要闻，从明星话题到体坛赛事，以丰富内容和精准视角，为用户呈现所喜欢的内容。【视频小说】搜罗全网资源，影音娱乐这里最全，更能一键下载到本地，体验本地化的极致享受。【生活服务】手机百度不仅提供美食、娱乐等常规线下服务，更为用户提供快修、回收、洗衣、早教及租车等丰富的上门服务内容，不仅为用户找到所求，更为用户解决所需，践行“链接人与服务”的产品使命。【我】登录、管理百度帐号，好友畅聊，安全畅享百度服务；下载管理和书签历史，重要内容贴心收藏；我的钱包，安全安心管理生活消费；订单、卡券包、积分，尽享各种优惠。', '系统工具 搜索·下载\n系统工具\n工具\n系统工具', '常用工具 生活 新闻资讯 语音 必备软件 热门应用 网络工具 搜索\n\n\n', 'soft', 3962567969))
    # print("===2===")
    insert_data("2016-08-18")
