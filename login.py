# _*_ coding: utf-8 _*_

import logging
from datetime import datetime
import pymysql
from flask import Flask, render_template
from flask import request, jsonify

app = Flask(__name__)


@app.route('/login', methods=["POST", "GET"])
def register():
    useremail = request.form.get("userEmail", "")
    username = request.form.get("userName", "")
    userpwd = request.form.get("userPwd", "")
    userlogin(useremail, userpwd)
    logging.debug(useremail, username, userpwd)
    return jsonify({"msg": "success"})


def userlogin(useremail, userpwd):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="123", db="my_db", charset="utf8")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (userEmail, userName, userPwd) VALUES (%s, %s, %s)", (useremail, username, userpwd))
        conn.commit()
    except Exception:
        logging.error("=======")
    return