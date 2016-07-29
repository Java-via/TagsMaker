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
    userpwd = request.form.get("userPwd", "")
    userlogin(useremail, userpwd)
    logging.debug(useremail, userpwd)
    return jsonify({"msg": "success"})


def userlogin(useremail, userpwd):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="123", db="my_db", charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT u_id FROM t_users WHERE u_email = %s AND u_pwd = %s;", useremail, userpwd)
        conn.commit()
    except Exception:
        logging.error("=======")
    return
