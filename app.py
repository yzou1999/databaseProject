from __future__ import print_function # In python 2.7
from re import S
from flask import Flask, json, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from datetime import date
from datetime import datetime,timedelta
import sys
from random import randint
import random

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Wohenni123!'
app.config['MYSQL_DATABASE_DB'] = 'driver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# cursor.execute("SELECT * from User")
# data = cursor.fetchone()
app.secret_key = 'secret'

@app.route('/')
def hello():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
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
                    return redirect(url_for('login'))
                else:
                    return json.dumps({'error':str(data[0])})
            else:
                    return json.dumps({'html':'<span>Enter the required fields</span>'})
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()
    elif request.method == "GET":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM driver')
            data = cursor.fetchall()
            a = []
            for d in data:
                a.append(d)
            ##print(data,file=sys.stderr)
            print(a,file=sys.stderr)
            return render_template('index.html',user = session['firstname'], data = a), 201
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()
    else:
        return render_template('index.html')

@app.route('/getDriver',methods=['POST','GET'])
def getDriver():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST' and 'ssn' in request.form:
        _ssn = request.form['ssn']
        if(len(_ssn) != 9):
            msg = "the length of SSN has to be 9"
            return render_template('index.html', msg = msg)
        cursor.execute('SELECT * FROM driver WHERE SSN = %s',_ssn)
        account = cursor.fetchone()
        a = []
        a.append(account)
        print(a,file=sys.stderr)
        return render_template('index.html', user = session['firstname'], data = a), 201
    else:
        msg = 'Incorrect ssn !'
    return render_template('login.html', msg = msg)

@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST' and 'ssn' in request.form:
        _ssn = request.form['ssn']
        if(len(_ssn) != 9):
            msg = "the length of SSN has to be 9"
            return render_template('login.html', msg = msg)
        cursor.execute('SELECT * FROM driver WHERE SSN = %s',_ssn)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['ssn'] = account[0]
            session['firstname'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg, user = session['firstname'])
        else:
            msg = 'Incorrect ssn !'
    return render_template('login.html', msg = msg)

@app.route('/index',methods=['POST','GET'])
def index():
    if 'loggedin' in session: 
        return render_template("index.html", user = session['firstname'])
    return redirect(url_for('login'))

@app.route('/postGetID', methods = ['POST','GET'])
def postGetID():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST' and 'id' in request.form:
        _id = request.form['id']
        if (_id == "GIC"):
            idNum = "GI" + session['ssn']
            idClass = "A"
            today = date.today()
            exp = date.today() + timedelta(days=20)
            ssn = session['ssn']
            cursor.callproc('sp_createID',(idNum,idClass,today,exp,ssn))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return render_template("id.html", user = session['firstname'])
            else:
                msg = str(data[0])
                return render_template("id.html",msg = msg)
        elif (_id == "DL"):
            idNum = "DL" + session['ssn']
            idClass = "B"
            today = date.today()
            exp = date.today() + timedelta(days=20)
            ssn = session['ssn']
            cursor.callproc('sp_createID',(idNum,idClass,today,exp,ssn))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return render_template("id.html", user = session['firstname'])
            else:
                msg = str(data[0])
                return render_template("id.html",msg = msg)
        elif (_id == "LL"):
            idNum = "LL" + session['ssn']
            idClass = "C"
            today = date.today()
            exp = date.today() + timedelta(days=20)
            ssn = session['ssn']
            cursor.callproc('sp_createID',(idNum,idClass,today,exp,ssn))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return render_template("id.html", user = session['firstname'])
            else:
                msg = str(data[0])
                return render_template("id.html",msg = msg)
        cursor.close() 
        conn.close()
    elif request.method == "GET":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select i.ID_Number, i.Class, i.Date_Issued, i.Date_Expired from has h, id_card i, driver d where h.ID_Number = i.ID_Number and h.SSN = %s and h.SSN = d.SSN",session['ssn'])
            data = cursor.fetchall()
            a = []
            for d in data:
                a.append(d)
            return render_template('id.html',user = session['firstname'], data = a), 201
        except Exception as e:
            msg = str(e)
            return render_template("id.html", user = session['firstname'], msg = msg)
        finally:
            cursor.close() 
            conn.close()
    else:
        return render_template("id.html", user = session['firstname'])

@app.route('/id',methods=['POST','GET'])
def id():
    if 'loggedin' in session: 
        return render_template("id.html", user = session['firstname'])
    return redirect(url_for('login'))

@app.route('/insurance',methods=['POST','GET'])
def insurance():
    if 'loggedin' in session: 
        return render_template("insurance.html", user = session['firstname'])
    return redirect(url_for('login'))

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@app.route('/postGetInsurance', methods = ['POST','GET'])
def postGetInsurance():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST' and 'company' and 'plan' and 'premium' and 'coverage' and 'vehicle' in request.form:
        _policyID = random_with_N_digits(10)
        _company = request.form['company']
        _plan = request.form['plan']
        _premium = request.form['premium']
        _coverage = request.form['coverage']
        exp = date.today() + timedelta(days=20)
        point = 50
        ssn = session['ssn']
        _vehicle = request.form['vehicle']
        cursor.callproc('sp_createInsurance',(_policyID, _company,_plan,_premium,_coverage, exp, point, ssn, _vehicle))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            cursor.close() 
            conn.close()
            return render_template("insurance.html", user = session['firstname'],msg="success")
        else:
            msg = str(data[0])
            return render_template("insurance.html",msg = msg)
    elif request.method == "GET":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select distinct i.Policy_ID, i.Company, i.Plan, i.Premium, i.Coverage, i.Expiration_Date, c.VIN from drives d, covers c, insures h, car_insurance i where h.Policy_ID = i.Policy_ID and h.SSN = %s and d.VIN = c.VIN",session['ssn'])
            data = cursor.fetchall()
            a = []
            for d in data:
                a.append(d)
            return render_template('insurance.html',user = session['firstname'], data = a), 201
        except Exception as e:
            msg = str(e)
            return render_template("insurance.html", user = session['firstname'], msg = msg)
        finally:
            cursor.close() 
            conn.close()
    else:
        return render_template("insurance.html", user = session['firstname'])

@app.route('/vehicle',methods=['POST','GET'])
def vehicle():
    if 'loggedin' in session: 
        return render_template("vehicle.html", user = session['firstname'])
    return redirect(url_for('login'))

@app.route('/postGetVehicle', methods = ['POST','GET'])
def postGetVehicle():
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            # read the posted values from the UI
            _vin = request.form['vin']
            _model = request.form['model']
            _year = request.form['year']
            _manufacturer = request.form['manufacturer']
            _color = request.form['color']
            _license = request.form['license']

            # validate the received values
            if _vin and _model and _year and _manufacturer and _color and _license:
                cursor.callproc('sp_createVehicle',(_vin,_model,_year,_manufacturer,_color,_license,session['ssn']))
                data = cursor.fetchall()
                if len(data) == 0:
                    conn.commit()
                    return render_template("vehicle.html", user = session['firstname'],msg="success")
                else:
                    msg = str(data[0])
                    return render_template("vehicle.html",msg = msg)
            else:
                    return render_template("vehicle.html",msg = "Enter the required fields")
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()
    elif request.method == "GET":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select v.VIN, v.Model, v.Year, v.Manufacturer, v.Color, v.License_Plate from drives h, vehicle v, driver d where h.VIN = v.VIN and h.SSN = %s and h.SSN = d.SSN",session['ssn'])
            data = cursor.fetchall()
            a = []
            for d in data:
                a.append(d)
            return render_template('vehicle.html',user = session['firstname'], data = a), 201
        except Exception as e:
            msg = str(e)
            return render_template("vehicle.html", user = session['firstname'], msg = msg)
        finally:
            cursor.close() 
            conn.close()
    else:
        return render_template("id.html", user = session['firstname'])

@app.route('/driverRecord',methods=['POST','GET'])
def driverRecord():
    if 'loggedin' in session: 
        return render_template("driverRecord.html", user = session['firstname'])
    return redirect(url_for('login'))