from datetime import datetime
from enum import unique
from logging import debug
from flask import Flask, render_template, request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_session import Session



app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bkc.sqlite3'
db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class Dojos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sensei = db.Column(db.String(200), nullable=False)
    days = db.Column(db.String(200), nullable=False)
    time_1 = db.Column(db.String(200), nullable=False)
    time_2 = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    dojo_image = db.Column(db.String(200), nullable=False)

class league(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    dojo = db.Column(db.String(100), nullable=False)

class league_stats(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    members = db.Column(db.String(100), nullable=False)
    played = db.Column(db.String(100), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    draw = db.Column(db.Integer, nullable=False)
    loss = db.Column(db.Integer, nullable=False)
    dojo = db.Column(db.String(100))


# class dojo_members(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     member_id = db.Column(db.String(100), nullable=False)
#     fname = db.Column(db.String(100), nullable=False)
#     lname = db.Column(db.String(100), nullable=False)
#     rank = db.Column(db.String(100), nullable=False)


class bkcMember(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.String(100), nullable=False)
    dojo_id = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pnum = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    unique_id = db.Column(db.String(100), nullable=False,unique=True)


class credit_table(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Integer,nullable=False)


class point_table(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer,nullable=False)
class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    admin_uname = db.Column(db.String(100), nullable=False,unique=True)
    admin_pass = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)

class Attendence(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100),nullable=True)
    status = db.Column(db.String(100),nullable=True)

class Classdays(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(100),nullable=False)
    




@app.route("/")
def home():
    return render_template('home.html')


# Auth

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        creds = Admin.query.filter_by(admin_uname = request.form['uname'],admin_pass=request.form['pass']).first()
        print(creds)
        if creds == None:
            return redirect("/login")
        else:
            session["name"] = request.form['uname']
            return redirect("/admin")
        
    return render_template("authentication-signin.html")

@app.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect("/login")
# Admin

@app.route("/createUser")
def createUser():
    admin = Admin(admin_uname="admin",admin_pass="admin",email="admin@demo.com")
    db.session.add(admin)
    db.session.commit()
    return render_template("authentication-signin.html")

@app.route("/admin")
def admin():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    print(session["name"])
    return render_template('index.html')

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/addMember",methods=['GET','POST'])
def addMember():
    # if not session.get("name"):
    #     # if not there in the session then redirect to the login page
    #     return redirect("/login")
    if request.method == 'POST':
        addMem = bkcMember(member_id = request.form["member_id"],dojo_id = request.form["dojo_id"],fname = request.form["fname"],lname=request.form["lname"],rank=request.form["rank"],email= request.form["email"],address=request.form["address"],age=request.form["age"],pnum=request.form["pnum"],unique_id=request.form["unique_id"])
        creds = credit_table(member_id=request.form["member_id"],credit=0)
        attendence = Attendence(member_id = request.form["member_id"])
        points = point_table(member_id=request.form["member_id"],points=0)
        
        db.session.add(addMem)
        if int(request.form["age"]) > 17:
            db.session.add(creds)
        else:
            db.session.add(points)
        db.session.commit()
        print("Member Added")
    return render_template("addMember.html")


@app.route("/addDojo",methods=['GET','POST'])
def addDojo():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    if request.method == 'POST':
        dojo = Dojos(name = request.form['name'],sensei = request.form['sensei'],days =request.form['days'],time_1= request.form['time_1'],time_2=request.form['time_2'],venue=request.form['venue'], dojo_image=request.form['dojo_image'])
        db.session.add(dojo)
        db.session.commit()
        return render_template('add_dojo.html')
    return render_template('add_dojo.html')

@app.route('/deleteDojo/<int:id>')
def deleteDojo(id):
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    dojo = Dojos.query.filter_by(id=id).first()
    db.session.delete(dojo)
    db.session.commit()
    return render_template('home.html')

@app.route("/tournaments")
def tournaments():
    return render_template("tournaments.html")

@app.route('/qr')
def qr():
    return render_template('qrscan.html')

@app.route('/startClass')
def startClass():
    # todays_date = datetime.today().strftime('%d-%m-%Y')
    todays_date = "28-09-2021"
    classdays = Classdays(date = todays_date)
    db.session.add(classdays)
    db.session.commit()
    return redirect("/qr")



@app.route('/attendence/<memID>', methods=['GET','POST'])
def attendence(memID):
    memberDetails = bkcMember.query.all()
    credit = credit_table().query.all()
    points = point_table().query.all()
    # todays_date = datetime.today().strftime('%d-%m-%Y')
    todays_date = "28-09-2021"
    attendence = Attendence(member_id=memID,date=todays_date,status="P")
    db.session.add(attendence)
    db.session.commit()
    for member in memberDetails:
        if memID == member.member_id:
            if member.age < 18:
                print("kids")
                for p in points:
                        if member.member_id == p.member_id:
                            p.points = int(p.points)+10
                            db.session.commit()
            else:
                print("adults")
                if member.rank.lower().replace(" ","") in ['9kyu','8kyu','7kyu']:
                    for c in credit:
                        if member.member_id == c.member_id:
                            c.credit = int(c.credit)+4
                            db.session.commit()
                else:
                    for c in credit:
                        if member.member_id == c.member_id:
                            c.credit = int(c.credit)+2
                            db.session.commit()
                            print("ID : "+ c.member_id)
                            print("Credits : "+str(c.credit))
                # elif member.rank.lower().replace(" ","") in ['6kyu','5kyu','4kyu']:
                #     for c in credit:
                #         if member.member_id == c.member_id:
                #             c.credit +=2
    return render_template("home.html")

# User 

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/dojo")
def dojo():
    alldojos = Dojos.query.all()
    return render_template('dojos.html',alldojos = alldojos)

@app.route("/dojoDetails")
def dojoDetails():
    memberDetails = bkcMember.query.filter_by(dojo_id = "BKC01").all()
    credit = credit_table.query.all() 
    points = point_table().query.all()
    classdays = Classdays.query.with_entities(Classdays.date)
    attendence = Attendence.query.all()

    # classdays = classdays[::-1]
    cdays = []
    for c in classdays:
        cdays = cdays + list(c)
    print(cdays)
    # for member in memberDetails:
    #     for a in attendence:
    #         if a.member_id == member.member_id

    return render_template('dojo_details.html',credit = credit,memberDetails = memberDetails,classdays=cdays[:8],attendence=attendence,points=points)


@app.route("/deleteTable")
def deleteTable():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('dojo_details.html')


if __name__ == '__main__':
    app.run(debug=True)