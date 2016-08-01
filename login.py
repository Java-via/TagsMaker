# _*_ coding: utf-8 _*_

import logging
from datetime import datetime
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


@app.route('/login', methods=["POST", "GET"])
def login():
    useremail = request.args.get("user", "")
    userpwd = request.args.get("userPwd", "")
    logging.debug("useremail = %s, userpwd = %s", useremail, userpwd)
    print(userlogin(useremail, userpwd))
    if userlogin(useremail, userpwd) == "exit":
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "fail"})


def userlogin(useremail, userpwd):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="123", db="my_db", charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT u_id FROM t_users WHERE u_email = %s AND u_pwd = %s;", useremail, userpwd)
        conn.commit()
        logging.error("fetchall = %s, size = %s", cur.fetchall(), cur.arraysize)
        if cur.arraysize > 0:
            return "exit"
        else:
            return "not_exit"
    except Exception:
        logging.error("=======")


if __name__ == "__main__":
    app.run(debug=True)
