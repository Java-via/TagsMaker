# _*_ coding: utf-8 _*_

"""
this model is aimed to route
"""
import logging
import pymysql
from flask import Flask, render_template
from flask import request, jsonify, make_response

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
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_APPDB, charset=DB_CHARSET)
        cur = conn.cursor()
        sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url FROM t_apps_basic_united " \
              "WHERE a_softgame = 'game' LIMIT 10;"
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        if len(apps) > 0:
            return jsonify({"msg": "has data", "apps": apps})
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
        sexual = request.args.get("sexual")
        age = request.args.get("age")
        marital = request.args.get("marital")
        degree = request.args.get("degree")
        logging.debug("useremail = %s, pkgname = %s, sexual = %s, age = %s, marital = %s", useremail, pkgname, sexual, age, marital)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            sql = "INSERT INTO t_user_tags (u_email, u_pkgname, u_gender, u_age, u_marital, u_degree) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            if sexual == "man":
                sexual = "男"
            elif sexual == "female":
                sexual = "女"
            else:
                sexual = "无偏向"
            if age == "teen":
                age = "18岁以下"
            elif age == "youth":
                age = "18-25岁"
            elif age == "old_youth":
                age = "26-35岁"
            elif age == "earth_mid":
                age = "36-45岁"
            elif age == "midlife":
                age = "45岁以上"
            else:
                age = "无偏向"
            if marital == "unmarried":
                marital = "未婚"
            elif marital == "married":
                marital = "已婚"
            else:
                marital = "无偏向"
            if degree == "middle":
                degree = "小学/初中"
            elif degree == "high":
                degree = "高中/中专"
            elif degree == "college":
                degree = "大专"
            elif degree == "university":
                degree = "本科及以上"
            else:
                degree = "无偏向"
            cur.execute(sql, (useremail, pkgname, sexual, age, marital, degree))
            logging.debug("save : %s, %s, %s, %s, %s, %s", useremail, pkgname, sexual, age, marital, degree)
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
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_APPDB, charset=DB_CHARSET)
        cur = conn.cursor()
        logging.debug("====1====")
        sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url FROM t_apps_basic_united " \
              "WHERE a_softgame = 'soft' LIMIT 10;"
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        if len(apps) > 0:
            return jsonify({"msg": "has data", "apps": apps})
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
        sexual = request.args.get("sexual")
        age = request.args.get("age")
        marital = request.args.get("marital")
        degree = request.args.get("degree")
        logging.debug("useremail = %s, pkgname = %s, sexual = %s, age = %s, marital = %s", useremail, pkgname, sexual, age, marital)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            sql = "INSERT INTO t_user_tags (u_email, u_pkgname, u_gender, u_age, u_marital, u_degree) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            if sexual == "man":
                sexual = "男"
            elif sexual == "female":
                sexual = "女"
            else:
                sexual = "无偏向"
            if age == "teen":
                age = "18岁以下"
            elif age == "youth":
                age = "18-25岁"
            elif age == "old_youth":
                age = "26-35岁"
            elif age == "earth_mid":
                age = "36-45岁"
            elif age == "midlife":
                age = "45岁以上"
            else:
                age = "无偏向"
            if marital == "unmarried":
                marital = "未婚"
            elif marital == "married":
                marital = "已婚"
            else:
                marital = "无偏向"
            if degree == "middle":
                degree = "小学/初中"
            elif degree == "high":
                degree = "高中/中专"
            elif degree == "college":
                degree = "大专"
            elif degree == "university":
                degree = "本科及以上"
            else:
                degree = "无偏向"
            cur.execute(sql, (useremail, pkgname, sexual, age, marital, degree))
            logging.debug("save : %s, %s, %s, %s, %s, %s", useremail, pkgname, sexual, age, marital, degree)
            conn.commit()
            return jsonify({"msg": "success"})
        except Exception as excep:
            logging.error(Exception, ":", excep)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans gametags with wrong request method: %s", request.method)
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
