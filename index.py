# _*_ coding: utf-8 _*_

"""
this model is aimed to route
"""
import logging
import pymysql
from flask import Flask, render_template
from flask import request, jsonify, make_response
from tagsconf import *
from db_config import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/iframe")
def iframe():
    return render_template("iframe.html")


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

    make_response("X-Frame-Options", "SAMEORIGIN")
    try:
        useremail = request.cookies.get("useremail")
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql_user = "SELECT u_game_end FROM t_users WHERE u_email = %s;"
        cur.execute(sql_user, useremail)
        game_end = cur.fetchall()[0][0]

        sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url, a_picurl, a_id " \
              "FROM t_tags_apps_test WHERE a_softgame = 'game' AND a_id > %s ORDER BY a_id LIMIT 10;"
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
        appid = request.args.get("appid")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        game_index = request.args.get("index")
        logging.debug("useremail = %s, pkgname = %s, appid = %s, tagsname = %s, tagsvalue = %s, index = %s",
                      useremail, pkgname, appid, tagsname, tagsvalue, game_index)
        if game_index == "10":
            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
                cur = conn.cursor()
                # save tags of this user
                sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                      "VALUES (%s, %s, %s, %s)"
                for idx in range(0, len(tagsname)):
                    cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                    logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                    conn.commit()

                # update endid of this user
                sql_end = "UPDATE t_users t1, (SELECT u_game_end AS game_end FROM t_users WHERE u_email = %s)t0 " \
                          "SET t1.u_game_end = %s WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, appid, useremail))
                conn.commit()

                # select another 10 data
                sql_user = "SELECT u_game_end FROM t_users WHERE u_email = %s"
                cur.execute(sql_user, useremail)
                game_end = cur.fetchall()[0][0]

                sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url, a_picurl, a_id " \
                      "FROM t_tags_apps_test WHERE a_softgame = 'game' AND a_id > %s ORDER BY a_id LIMIT 10;"
                cur.execute(sql, game_end)
                conn.commit()
                apps = cur.fetchall()
                if len(apps) > 0:
                    return jsonify({"msg": "another ten", "apps": apps})
                else:
                    return jsonify({"msg": "no data"})
            except Exception as excep:
                logging.error(Exception, ":", excep)
                return jsonify({"msg": "sql error"})
        else:
            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
                cur = conn.cursor()
                # save game tags of this user
                sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                      "VALUES (%s, %s, %s, %s)"
                for idx in range(0, len(tagsname)):
                    cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                    logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                    conn.commit()

                # update end of this user
                sql_end = "UPDATE t_users t1, (SELECT u_game_end AS game_end FROM t_users WHERE u_email = %s)t0 " \
                          "SET t1.u_game_end = %s WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, appid, useremail))
                conn.commit()
                return jsonify({"msg": "success"})
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

    make_response("X-Frame-Options", "SAMEORIGIN")

    try:
        useremail = request.cookies.get("useremail")
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql_user = "SELECT u_soft_end FROM t_users WHERE u_email = %s"
        cur.execute(sql_user, useremail)
        soft_end = cur.fetchall()[0][0]

        sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url, a_picurl, a_id " \
              "FROM t_tags_apps_test WHERE a_softgame = 'soft' AND a_id > %s ORDER BY a_id LIMIT 10;"
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
        appid = request.args.get("appid")
        tagsname = request.args.get("tagsname").split(",")
        tagsvalue = request.args.get("tagsvalue").split(",")
        soft_index = request.args.get("index")
        logging.debug("useremail = %s, pkgname = %s, pkgname = %s, tagsname = %s, tagsvalue = %s, index = %s",
                      useremail, pkgname, appid, tagsname, tagsvalue, soft_index)
        if soft_index == "10":
            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
                cur = conn.cursor()
                # save soft tags of this user
                sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                      "VALUES (%s, %s, %s, %s)"
                for idx in range(0, len(tagsname)):
                    cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                    logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                    conn.commit()

                # update soft end of this user
                sql_end = "UPDATE t_users t1, (SELECT u_soft_end AS soft_end FROM t_users WHERE u_email = %s)t0 " \
                          "SET t1.u_soft_end = %s WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, appid, useremail))
                conn.commit()

                # select another ten soft
                sql_user = "SELECT u_soft_end FROM t_users WHERE u_email = %s"
                cur.execute(sql_user, useremail)
                game_end = cur.fetchall()[0][0]
                sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url, a_picurl, a_id " \
                      "FROM t_tags_apps_test WHERE a_softgame = 'soft' AND a_id > %s ORDER BY a_id LIMIT 10;"
                cur.execute(sql, game_end)
                conn.commit()
                apps = cur.fetchall()
                if len(apps) > 0:
                    logging.debug("another ten")
                    return jsonify({"msg": "another ten", "apps": apps})
                else:
                    return jsonify({"msg": "no data"})
            except Exception as excep:
                logging.error(Exception, ":", excep)
                return jsonify({"msg": "sql error"})
        else:
            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
                cur = conn.cursor()
                # save soft tags of this user
                sql = "INSERT INTO t_user_tags (u_useremail, u_pkgname, u_tagname, u_tagvalue) " \
                      "VALUES (%s, %s, %s, %s)"
                for idx in range(0, len(tagsname)):
                    cur.execute(sql, (useremail, pkgname, tagsname[idx], tagsvalue[idx]))
                    logging.debug("save : %s, %s, %s, %s", useremail, pkgname, tagsname[idx], tagsvalue[idx])
                    conn.commit()

                # update soft end of this user
                sql_end = "UPDATE t_users t1, (SELECT u_soft_end AS soft_end FROM t_users WHERE u_email = %s)t0 " \
                          "SET t1.u_soft_end = %s WHERE u_email = %s;"
                cur.execute(sql_end, (useremail, appid, useremail))
                conn.commit()
                logging.debug("success")
                return jsonify({"msg": "success"})
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
    app.run(debug=True, host="0.0.0.0")
