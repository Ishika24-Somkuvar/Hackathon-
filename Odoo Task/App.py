from flask import Flask, flash, request, redirect, jsonify, render_template
from flask_session import Session
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import MySQLdb.cursors
from random import randint
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import requests


app = Flask(_name_)
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
dataKey = 'dkl9DOws21hJAmbAu07790JqYjGSSpWB'
# app.config['SECURITY_PASSWORD_HASH'] = 'dkl9DOws21hJAmbAu07790JqYjGSSpWB'

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'karishma.wani0112@gmail.com'
app.config['MAIL_PASSWORD'] = 'dieg sbqc rrmb kswc'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
mail = Mail(app)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'Hackathon'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return jsonify({'status':200, 'message':'API Test hey Success'})


@app.route('/auth/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
                  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tbl_user WHERE email = % s', (email, ))
        account = cursor.fetchone()

        if account:
            if account and check_password_hash(account['password'], pwd):
                if account['isverify'] == "1" or account['isverify'] == True:
                    payload = {
                        'id': account['id'],
                        'email': account['email'],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}

                    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
                    cursor.execute(
                        "update tbl_user set token = % s,isflag = %s where email = %s", (token, email,))
                    mysql.connection.commit()

                    msg = 'Logged in successfully !'
                    data = {
                        'token': token,
                        'id': account['id'],
                        'username':account['username']
                    }
                    cursor.close()
                    return render_template({'data': data, 'message': msg, 'status': 200})
                else:
                    generate_otp = randint(1111, 9999)
                    msg = Message('Verify Your Registration',
                                sender='karishma.wani0112@gmail.com', recipients=[email])
                    msg.body = "Your verification code is" + str(generate_otp)
                    mail.send(msg)
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(
                        'SELECT * FROM tbl_user WHERE email = % s', (email,))
                    account = cursor.fetchone()
                    if account:
                        payload = {
                            'id': account['id'],
                            'email': account['email'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
                        }
                        token = jwt.encode(
                            payload, app.secret_key, algorithm='HS256')
                        cursor.execute(
                            'update tbl_user set token= %s, otp = %s where email = %s', (token, generate_otp, email,))
                        mysql.connection.commit()

                        if account['isverify'] == '0' or account['isverify'] == False:
                            isEmailVerified = 'false'

                        data = {
                            'token': token,
                            'isEmailVerified': isEmailVerified,
                            'id': account['id'],
                            'username':account['username']
                        }
                        msg = 'Please verify your email'
                        cursor.close()
                        return jsonify({'data': data, 'otp':generate_otp,'message': msg, 'status': 400})
            else:
                msg = 'Please enter correct email and password'
                cursor.close()
                return jsonify({'message': msg, 'status': 400})
        else:
            msg = 'Your Email Doesn\'t Exist'
            cursor.close()
            return jsonify({'message': msg, 'status': 400})



@app.route('/auth/signup', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tbl_user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Email Already Exits!'
            cursor.close()
            return jsonify({'message': msg, 'status': 400})
        else:
            sql = "INSERT INTO tbl_user (username, email,password,isflag,isverify) VALUES (%s, %s, %s,%s,%s)"
            val = (username, email, generate_password_hash(pwd), 'false', False)
            cursor.execute(sql, val)
            mysql.connection.commit()
            msg = 'You have successfully registered!'

            generate_otp = randint(1111, 9999)
            msg = Message('Verify Your Registration',
                          sender='karishma.wani0112@gmail.com', recipients=[email])
            msg.body = "Your verification code is: " + str(generate_otp)
            mail.send(msg)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM tbl_user WHERE email = % s', (email,))
            account = cursor.fetchone()
            if account:
                payload = {
                    'id': account['id'],
                    'email': account['email'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
                }
                token = jwt.encode(payload, app.secret_key, algorithm='HS256')
                cursor.execute(
                    'update tbl_user set token= %s, otp = %s where email = %s', (token, generate_otp, email,))
                mysql.connection.commit()

                sql = "INSERT INTO tbl_userSubscriptionUsed (totalDuration, unusedDuration,usedDuration,isActiveflag,user_id) VALUES (%s, %s, %s,%s,%s)"
                val = ('10:00:00', '10:00:00','00:00:00', True,account['id'])
                cursor.execute(sql, val)
                mysql.connection.commit()

                msg = "Successfully email submit!"
                data = {
                    'token': token,
                    'username':account['username'],
                    'id': account['id']
                }
                cursor.close()

                # Send the HTTP request to create the collection
                return jsonify({'data': data, 'otp':generate_otp,'message': msg, 'status': 200})
        cursor.close()
    # else:
    #     return "Please select valid method"


@app.route('/auth/forgotPassword', methods=['POST', 'GET'])
def forgotPasswordV4():
    if request.method == 'POST':
        email = request.form['email']
        generate_otp = randint(1111, 9999)
        msg = Message('Forgot Password',
                      sender='karishma.wani0112@gmail.com', recipients=[email])
        msg.body = "Your verification code is: " + str(generate_otp)
        mail.send(msg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'update tbl_user set otp = %s where email = %s', (generate_otp, email,))
            mysql.connection.commit()
            msg = "Successfully email submit!"
            cursor.close()
            return jsonify({'otp':generate_otp,'message': msg, 'status': 200})
        msg = "Email Don't Exits!"
        cursor.close()
        return jsonify({'message': msg, 'status': 400})


@app.route('/auth/verifyOtp', methods=['POST', 'GET'])
def verifyOTPV4():
    if request.method == 'POST':
        email = request.form['email']
        otp = request.form['otp']
        # token =  request.headers.get('token')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            generate_otp = account['otp']
            if generate_otp == otp:
                cursor.execute(
                    'update tbl_user set isverify = %s where email = %s', (True, email,))
                mysql.connection.commit()
                msg = 'your OTP is match'
                cursor.close()
                return jsonify({'message': msg, 'status': 200})
            msg = "Your OTP is not match"
            return jsonify({'message': msg, 'status': 400})
        msg = "Email Don't Exits"
        cursor.close()
        return jsonify({'message': msg, 'status': 400})


@app.route('/auth/resetPassword', methods=['POST', 'GET'])
def resetPasswordV4():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'update tbl_user set password = %s where email = % s', (generate_password_hash(pwd), email,))
            mysql.connection.commit()
            msg = "Successfully update your password"
            cursor.close()
            return jsonify({'message': msg, 'status': 200})
        else:
            cursor.close()


@app.route('/auth/logout', methods=['POST', 'GET'])
def logoutV4():
    if request.method == 'POST':
        headers = request.headers
        bearer = headers.get('Authorization')
        token = bearer.split()[1]
    
        try:
            payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            email = payload['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM tbl_user WHERE email = % s', (email,))
            account = cursor.fetchone()
            if account:
                cursor.execute(
                    'update tbl_user set token = %s where email = % s', ('', email,))
                mysql.connection.commit()
                cursor.close()

                msg = "Successfully logout"
                return jsonify({'message': msg, 'status': 200})
            else:
                cursor.close()
        except:
            msg = 'Session timed out!'
            return jsonify({'message': msg, 'status': 203})


if _name_ == '_main_':
    app.run(host='0.0.0.0',port='5000',debug=True)
