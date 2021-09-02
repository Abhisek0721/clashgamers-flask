from os import error, name
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from instamojo_wrapper import Instamojo
import requests, json, random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clashGamers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret'
db = SQLAlchemy(app)

# Api_key = "test_38fe23ddde8c9e3c77abeb98718"
# Auth_token = "test_3af2934f39906237f43104d177e"
# api = Instamojo(api_key=Api_key, auth_token=Auth_token, endpoint="https://test.instamojo.com/api/1.1/")


class Accounts(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(30), unique=True)
    CountryCode = db.Column(db.String(5))
    PhoneNo = db.Column(db.String(20),unique=True)
    FreeFireID = db.Column(db.String(20))
    UPI = db.Column(db.String(20), nullable=False)
    Gender = db.Column(db.String(6))
    Password = db.Column(db.String(20))
    Datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Id} - {self.Username}"

class Contacts(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(30), nullable=True)
    Title = db.Column(db.String(60))
    Email = db.Column(db.String(30))
    Message = db.Column(db.String(600))
    Datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Id} - {self.Email}"

class Userjoin(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Orderid = db.Column(db.String(30))
    Username = db.Column(db.String(30))
    Name = db.Column(db.String(30))
    CountryCode = db.Column(db.String(5))
    PhoneNo = db.Column(db.String(20))
    Email = db.Column(db.String(40))
    Datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Id} - {self.Username}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if session.get('joinMsg') != "You have already join this plan.":
        session.pop("joinMsg",None)
    if 'signupMSG' in session:
        session.pop('signupMSG',None)
    if session.get("auth"):
        name = session.get("name")
        auth = session.get("auth")
        return render_template('./index.html',auth=auth,name=name,joinMsg=session.get("joinMsg"))
    else:
        auth = False
        return render_template('./index.html',auth=auth,joinMsg=session.get("joinMsg"))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(request.method == "POST"):
        if(session.get("auth") and session.get("name")):
            username = session.get("name")
        else:
            username = None
        title = request.form["title"]
        email = request.form["email"]
        message = request.form.get("contact_msg")
        contact = Contacts(Username = username, Title=title, Email=email, Message=message)
        db.session.add(contact)
        db.session.commit()
        return redirect("./")


@app.route('/signup', methods=['GET', 'POST'])
def signup():  
    if 'msg' in session:
        session.pop('msg',None)

    if request.method == "POST":
        name = request.form['name']
        country_code = request.form['country_code']
        phone_number = request.form['phoneNo']
        ff_id = request.form['ff_id']
        upi = request.form['upi']
        gender = request.form['gender']
        password = request.form['RetypePassword']

        check_username = Accounts.query.filter_by(Username=name).first()
        check_phone = Accounts.query.filter_by(PhoneNo=phone_number).first()

        if(check_phone or check_username):
            session['signupMSG'] = "Username or Phone Number has already been registered!"
            return redirect(url_for("signup"))
        else:
            if 'signupMSG' in session:
                session.pop('signupMSG',None)
            signup = Accounts(Username = name,CountryCode=country_code,PhoneNo=phone_number,FreeFireID=ff_id,UPI=upi,Gender=gender,Password=password)
            db.session.add(signup)
            db.session.commit()
            session['msg'] = "Account has been created successfully !"
            return redirect(url_for("login"))

    return render_template('./signup.html',msg=session.get("signupMSG"))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'signupMSG' in session:
        session.pop('signupMSG',None)
    if "msg" in session:
        pass

    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')
        session['auth'] = False
        user = Accounts.query.filter_by(Username=name).first()
        if user:
            if(password==user.Password):
                session['name'] = name
                session['password'] = password
                session['auth'] = True
                if "msg" in session:
                    session.pop("msg",None)
                return redirect('./')
            else:
                session["msg"] = "Wrong Password !"
        else:
            session["msg"] = "This Username doesn't exist."

    return render_template('./login.html',msg = session.get('msg'))

@app.route('/logout')
def logout():
    store = ['auth','name','phone_number','country_code','ff_id','upi','gender','password','otp','signupMSG','joinMsg']
    for i in store:
        if i in session:
            session.pop(i,None)
    return redirect(url_for('login'))

@app.route('/forgotten', methods=['GET', 'POST'])
def forgotten():
    if request.method == "POST":
        otp = request.form['otp']
        phoneNo = request.form["phoneNo"]
        session.pop('otp',None)
        session["phoneNo"] = phoneNo
        return redirect("./changePassword")
            
    return render_template("./forgotten.html")

@app.route("/changePassword", methods=['GET', 'POST'])
def changePassword():
    phoneNo = session.get('phoneNo')
    user = Accounts.query.filter_by(PhoneNo=phoneNo).first()
    session["reminderUsername"] = user.Username
    if request.method == "POST":
        changePassword = request.form['confirmPassword']
        user.Password = changePassword
        db.session.add(user)
        db.session.commit()
        if 'msg' in session:
            session.pop('msg',None)
            session['msg'] = "Your password has been changed!"
            return redirect("./login")
        else:
            session['msg'] = "Your password has been changed!"
            return redirect("./login")

    return render_template("changePassword.html", username=session.get("reminderUsername"))


@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == "POST":
        user = Accounts.query.filter_by(Username=session["name"]).first()
        name = request.form["name"]
        email = request.form["email"]
        countryCode = user.CountryCode
        phoneNo = user.PhoneNo

        def createOrderId():
            return "order_"+str(random.randrange(1000000,9000000))

        url = "https://test.cashfree.com/api/v1/order/create"

        payload={'appId': '939176d02f6d7c3b283979a3c71939',
        'secretKey': '83d34fd586b0bb2ffe206cf22cd7d65449b7d6f7',
        'orderId': createOrderId(),
        'orderAmount': '29',
        'orderCurrency': 'INR',
        'orderNote': 'Entry fee in Clash Gamer',
        'customerEmail': email,
        'customerName': name,
        'customerPhone': countryCode+phoneNo,
        'returnUrl': 'https://github.com/Abhisek0721',
        'returnUrl': 'https://github.com/Abhisek0721',
        'notifyUrl': 'https://github.com/Abhisek0721'}
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.text)
        return redirect(eval(response.text)["paymentLink"])
    else:
        return render_template("pay.html")

@app.route('/admin', methods=["GET", "POST"])
def admin():
    if session.get('name') == "clashgamer" and session.get("password") == "clashgamer1":
        accounts = Accounts.query.all()
        return render_template("adminAccounts.html", accounts=accounts)
    else:
        return redirect("./")

@app.route('/adminContacts', methods=["GET","POST"])
def adminContacts():
    if session.get('name') == "clashgamer" and session.get("password") == "clashgamer1":
        contacts = Contacts.query.all()
        return render_template("adminContacts.html", contacts=contacts)

@app.route('/adminUserjoin', methods=["GET","POST"])
def adminUserjoin():
    if session.get('name') == "clashgamer" and session.get("password") == "clashgamer1":
        contacts = Contacts.query.all()
        return render_template("adminUserjoin.html", contacts=contacts)


if __name__ == "__main__":
    app.run(debug=False)