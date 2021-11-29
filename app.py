from re import S
from flask import Flask, json, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import sys

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Wohenni123!'
app.config['MYSQL_DATABASE_DB'] = 'driver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# cursor.execute("SELECT * from User")
# data = cursor.fetchone()

@app.route('/')
def hello():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # read the posted values from the UI
        _First_Name = request.form['firstName']
        _Last_Name = request.form['lastName']
        _SSN = request.form['ssn']
        _Address = request.form['address']
        _Birthday = request.form['birthdate']
        _Height = request.form['height']
        _Eye = request.form['eye']
        _Sex = request.form['sex']

        if (len(_SSN) != 9):
            return json.dumps({'error':'The SSN has to be 9 digit'})

        # validate the received values
        if _First_Name and _Last_Name and _SSN and _Address and _Birthday and _Height and _Eye and _Sex:
            cursor.callproc('sp_createDriver',(_SSN,_First_Name,_Last_Name,_Address,_Birthday,_Height,_Eye,_Sex))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()