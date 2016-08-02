# _*_ coding: utf-8 _*_

import logging
import pymysql
from flask import Flask, render_template
from flask import request, jsonify

logging.basicConfig(level=logging.DEBUG)

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

# ----local----
DB_HOST = "127.0.0.1"
DB_DB = "my_db"
DB_APPDB = "app_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sig")
def sig():
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user_email = request.form.get("userEmail")
        user_pwd = request.form.get("userPwd")
        logging.debug("user_email = %s, user_pwd = %s", user_email, user_pwd)

    logging.debug("userlogin = %s", userlogin(user_email, user_pwd))
    if userlogin(user_email, user_pwd) == "exit":
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "fail"})


@app.route("/tagsbegin", methods=["POST", "GET"])
def tagsbegin():
    return render_template("tagsbegin.html")


@app.route("/tagssoft", methods=["POST", "GET"])
def tagssoft():
    return render_template("tagssoft.html")


@app.route("/tagsgame", methods=["POST", "GET"])
def tagsgame():
    return render_template("tagsgame.html")


def userlogin(useremail, userpwd):
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
        cur = conn.cursor()
        cur.execute("SELECT u_id FROM t_users WHERE u_email = %s AND u_pwd = %s", (useremail, userpwd))
        conn.commit()
        num = len(cur.fetchall())
        if num > 0:
            return "exit"
        else:
            return "not_exit"
    except Exception as e:
        logging.error(Exception, ":", e)
        return


@app.route("/gameinfo", methods=["POST", "GET"])
def gameinfo():
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_APPDB, charset=DB_CHARSET)
        cur = conn.cursor()
        logging.debug("====1====")
        sql = "SELECT a_pkgname, a_name, a_description, a_defaulttags, a_classify, a_url FROM t_apps_basic_united " \
              "WHERE a_softgame = 'game' LIMIT 10;"
        cur.execute(sql)
        conn.commit()
        apps = cur.fetchall()
        if len(apps) > 0:
            return jsonify({"msg": "has data", "apps": apps})
        else:
            return jsonify({"msg": "no data"})

    except Exception as e:
        logging.error(Exception, ":", e)
        return jsonify({"msg": "no data"})


@app.route("/gametags", methods=["POST", "GET"])
def gametags():
    if request.method == "GET":
        pkgname = request.args.get("pkgname")
        sexual = request.args.get("sexual")
        age = request.args.get("age")
        marital = request.args.get("marital")
        logging.debug("pkgname = %s, sexual = %s, age = %s, marital = %s", pkgname, sexual, age, marital)
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
            cur = conn.cursor()
            sql = "INSERT INTO t_tags (t_sexual, t_age, t_marital, t_degree) VALUES (%s, %s, %s, %s) " \
                  "WHERE t_pkgname = %s"
            cur.execute(sql, (sexual, age, marital, "学士", pkgname))
            conn.commit()
            return jsonify({"msg": "success"})
        except Exception as e:
            logging.error(Exception, ":", e)
            return jsonify({"msg": "sql error"})
    else:
        logging.error("trans gametags with wrong request method: %s", request.method)
        return jsonify({"msg": "fail"})


def savegametags():
    return


@app.route("/userinfo", methods=["POST", "GET"])
def userinfo():
    if request.method == "GET":
        conn = pymysql.connect(host=DB_DB, user=DB_USER, password=DB_PWD, charset=DB_CHARSET)
        cur = conn.cursor()
        sql = "SELECT u_email, u_name, u_pwd, u_manager FROM t_users"
        cur.execute(sql)
        user = cur.fetchall()
        if len(user) < 0:
            logging.error("selece users error")

if __name__ == "__main__":
    app.run(debug=True)
