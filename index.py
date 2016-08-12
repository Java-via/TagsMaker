# _*_ coding: utf-8 _*_

"""
this model is aimed to route
"""
import logging
import pymysql
from flask import Flask, render_template
from flask import request, jsonify, make_response
from tagsconf import *

logging.basicConfig(level=logging.DEBUG)

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

# ----local----
DB_HOST = "127.0.0.1"
DB_APPDB = "app_db"
DB_DB = "my_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"

app = Flask(__name__)


@app.route("/")
def index():
    """
    index html
    :return:
    """
    return render_template("index.html")


@app.route("/sig")
def sig():
    """
    login html
    :return:
    """
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    login this system
    :return:
    """
    if request.method == 'POST':
        user_email = request.form.get("userEmail")
        user_pwd = request.form.get("userPwd")
        logging.debug("user_email = %s, user_pwd = %s", user_email, user_pwd)

    logging.debug("userlogin = %s", userlogin(user_email, user_pwd))
    if userlogin(user_email, user_pwd) == "manager":
        return jsonify({"msg": "manager"})
    elif userlogin(user_email, user_pwd) == "exit":
        resp = make_response(jsonify({"msg": "success"}))
        resp.set_cookie("useremail", user_email)
        return resp
    else:
        return jsonify({"msg": "fail"})


@app.route("/tagsbegin", methods=["POST", "GET"])
def tagsbegin():
    """
    tags begin html
    :return:
    """
    return render_template("tagsbegin.html")


@app.route("/manager", methods=["POST", "GET"])
def manager():
    """
    manager html
    :return:
    """
    return render_template("manager.html")


@app.route("/tagssoft", methods=["POST", "GET"])
def tagssoft():
    """
    begin with soft
    :return:
    """
    return render_template("tagssoft.html")


@app.route("/tagsgame", methods=["POST", "GET"])
def tagsgame():
    """
    begin with game
    :return:
    """
    return render_template("tagsgame.html")


def userlogin(useremail, userpwd):
    """
    check manager or not and return if is exist or not
    :param useremail: email of user
    :param userpwd: password for this user
    :return: manager or exist or not
    """
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        cur.execute("SELECT * FROM t_users WHERE u_email = %s AND u_pwd = %s", (useremail, userpwd))
        conn.commit()
        user = cur.fetchall()
        if user[0][4] == 1:
            return "manager"
        elif len(user) > 0:
            return "exit"
        else:
            return "not_exit"
    except Exception as excep:
        logging.error(Exception, ":", excep)
        return


@app.route("/gameinfo", methods=["POST", "GET"])
def gameinfo():
    """
    get game info limit 10
    :return:
    """
    try:
        useremail = request.cookies.get("useremail")
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql_user = "SELECT u_game_end FROM t_users WHERE u_email = %s"
        cur.execute(sql_user, useremail)
        game_end = cur.fetchall()[0][0]
        sql = "SELECT t_pkgname, t_name, t_description, t_defaulttags, t_classify, t_url, t_picurl FROM t_tags_game " \
              "WHERE t_softgame = 'game' AND t_id > %s ORDER BY t_id LIMIT 10;"
        cur.execute(sql, game_end)
        conn.commit()
        apps = cur.fetchall()
        if len(apps) > 0:
            return jsonify({"msg": "has data", "apps": apps, "tags": config_tags_game})
        else:
            return jsonify({"msg": "no data"})

    except Exception as excep:
        logging.error(Exception, ":", excep)
        return jsonify({"msg": "no data"})


@app.route("/gametags", methods=["POST", "GET"])
def gametags():
    """
    get tags for game that user given and save it
    :return:
    """
    if request.method == "GET":
        useremail = request.cookies.get("useremail")
        pkgname = request.args.get("pkgname")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        logging.debug("useremail = %s, pkgname = %s, tagsname = %s, tagsvalue = %s", useremail, pkgname, tagsname, tagsvalue)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                  "VALUES (%s, %s, %s, %s)"
            for idx in range(0, len(tagsname)):
                cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                conn.commit()
            return jsonify({"msg": "success"})
        except Exception as excep:
            logging.error(Exception, ":", excep)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans gametags with wrong request method: %s", request.method)
        return jsonify({"msg": "fail"})


@app.route("/moregame", methods=["POST", "GET"])
def moregame():
    """
    get another 10 game apps
    :return:
    """
    if request.method == "GET":
        index = request.args.get("index")
        useremail = request.cookies.get("useremail")
        pkgname = request.args.get("pkgname")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        logging.debug("useremail = %s, pkgname = %s, tagsname = %s, tagsvalue = %s", useremail, pkgname, tagsname, tagsvalue)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            if int(index) == 10:
                sql_end = "UPDATE t_users t1, (SELECT u_game_end AS game_end FROM t_users WHERE u_email = %s)t0 " \
                           "SET t1.u_game_end = (t0.game_end + 10) WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, useremail))
                conn.commit()
            sql_search_end = "SELECT u_game_end FROM t_users WHERE u_email = %s;"
            cur.execute(sql_search_end, useremail)
            num = cur.fetchall()[0][0]
            sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                  "VALUES (%s, %s, %s, %s)"
            for idx in range(0, len(tagsname)):
                cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                conn.commit()
            sql_apps = "SELECT t_pkgname, t_name, t_description, t_defaulttags, t_classify, t_url, t_picurl " \
                       "FROM t_tags_game WHERE t_softgame = 'game' AND t_id > %s ORDER BY t_id LIMIT 10;"
            cur.execute(sql_apps, num)
            conn.commit()
            apps = cur.fetchall()
            return jsonify({"msg": "success", "apps": apps})
        except Exception as excep:
            logging.error(Exception, ":", excep)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans gametags with wrong request method: %s", request.method)
        return jsonify({"msg": "fail"})


@app.route("/softinfo", methods=["POST", "GET"])
def softinfo():
    """
    get soft info limit 10
    :return:
    """
    try:
        useremail = request.cookies.get("useremail")
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql_user = "SELECT u_soft_end FROM t_users WHERE u_email = %s"
        cur.execute(sql_user, useremail)
        soft_end = cur.fetchall()[0][0]
        sql = "SELECT t_pkgname, t_name, t_description, t_defaulttags, t_classify, t_url, t_picurl FROM t_tags_soft " \
              "WHERE t_softgame = 'soft' AND t_id > %s ORDER BY t_id LIMIT 10;"
        cur.execute(sql, soft_end)
        conn.commit()
        apps = cur.fetchall()
        if len(apps) > 0:
            return jsonify({"msg": "has data", "apps": apps, "tags": config_tags_soft})
        else:
            return jsonify({"msg": "no data"})

    except Exception as excep:
        logging.error(Exception, ":", excep)
        return jsonify({"msg": "no data"})


@app.route("/softtags", methods=["POST", "GET"])
def softtags():
    """
    get tags for soft that user given and save it
    :return:
    """
    if request.method == "GET":
        useremail = request.cookies.get("useremail")
        pkgname = request.args.get("pkgname")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        logging.debug("useremail = %s, pkgname = %s, tagsname = %s, tagsvalue = %s", useremail, pkgname, tagsname,
                      tagsvalue)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                  "VALUES (%s, %s, %s, %s)"
            for idx in range(0, len(tagsname)):
                cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                conn.commit()
            return jsonify({"msg": "success"})
        except Exception as excep:
            logging.error(Exception, ":", excep)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans softtags with wrong request method: %s", request.method)
        return jsonify({"msg": "fail"})


@app.route("/moresoft", methods=["POST", "GET"])
def moresoft():
    """
    get another 10 soft apps
    :return:
    """
    if request.method == "GET":
        index = request.args.get("index")
        useremail = request.cookies.get("useremail")
        pkgname = request.args.get("pkgname")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        logging.debug("useremail = %s, pkgname = %s, tagsname = %s, tagsvalue = %s", useremail, pkgname, tagsname,
                      tagsvalue)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            if int(index) == 10:
                sql_end = "UPDATE t_users t1, (SELECT u_soft_end AS soft_end FROM t_users WHERE u_email = %s)t0 " \
                          "SET t1.u_soft_end = (t0.soft_end + 10) WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, useremail))
                conn.commit()
            sql_search_end = "SELECT u_soft_end FROM t_users WHERE u_email = %s;"
            cur.execute(sql_search_end, useremail)
            num = cur.fetchall()[0][0]
            sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                  "VALUES (%s, %s, %s, %s)"
            for idx in range(0, len(tagsname)):
                cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                conn.commit()
            sql_apps = "SELECT t_pkgname, t_name, t_description, t_defaulttags, t_classify, t_url, t_picurl " \
                       "FROM t_tags_soft WHERE t_softgame = 'soft' AND t_id > %s ORDER BY t_id LIMIT 10;"
            cur.execute(sql_apps, num)
            conn.commit()
            apps = cur.fetchall()
            return jsonify({"msg": "success", "apps": apps})
        except Exception as excep:
            logging.error(Exception, ":", excep)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans softtags with wrong request method: %s", request.method)
        return jsonify({"msg": "fail"})


@app.route("/userinfo", methods=["POST", "GET"])
def userinfo():
    """
    search for user info
    :return: user info if exist
    """
    if request.method == "GET":
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql = "SELECT u_email, u_name, u_pwd, u_manager FROM t_users"
        cur.execute(sql)
        user = cur.fetchall()
        if len(user) < 0:
            logging.error("selece users error")
            return jsonify({"msg": "no data"})
        else:
            return jsonify({"msg": "have users", "users": user})

if __name__ == "__main__":
    app.run(debug=True)
