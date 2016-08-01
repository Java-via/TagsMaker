# _*_ coding: utf-8 _*_

import logging
import pymysql
from flask import Flask, render_template
from flask import request, jsonify

logging.basicConfig(level=logging.DEBUG)
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
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123", db="my_db", charset="utf8")
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
        conn = pymysql.connect(host="localhost", user="root", password="123", db="app_db", charset="utf8")
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


if __name__ == "__main__":
    app.run(debug=True)
