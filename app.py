# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import session, url_for
import pymongo
# import os
from datetime import datetime
#sudo pip3 install dnspython

#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run

#hiding the secret key is not working 
# app.config['app.secret_key'] = os.getenv("app.secret_key")
# app.secret_key = app.config["app.secret_key"]
app.secret_key = "L9K0m3KPfAQA"

#connect to your Mongo DB database
client = pymongo.MongoClient('mongodb+srv://project_user:61WAQwDQJZPYFjmF@cluster0.qf94p.mongodb.net/project?retryWrites=true&w=majority')

#get the database name
db = client.get_database('project')
#get the particular collection that contains the data
records = db.users
what = db.data
# transactions = db.data

#The home page, maybe with slide that will show features and stuffs.
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', time = datetime.now())




#This is for the sign up system
@app.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        #Get all the input info
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('home.html', message=message)
        elif email_found:
            message = 'This email already exists in database'
            return render_template('home.html', message=message)
        elif password1 != password2:
            message = 'Passwords should match!'
            return render_template('home.html', message=message)
        else:
            message = "User Created Successfully!"
            user_input = {'name': user, 'email': email, 'password': password2, 'section':{'date': "", 'amount': "", 'description': ""}}
            #insert it in the record collection
            records.insert_one(user_input)
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email, message=message)
    return render_template('home.html')



#The login system
@app.route("/login", methods=["POST", "GET"])
def login():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #Check if the input is empty
        if email == "":
            message = "Please enter your email!"
            return render_template('home.html', message=message)
        #check if email exists in database
        email_found = records.find_one({"email": email})
        #If email is found and password is verified, then it will direct to logged-in page
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            if password == passwordcheck:
                session['email'] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('home.html', message=message)
        else:
            message = 'Email not found'
            return render_template('home.html', message=message)
    return render_template('home.html', message=message)



#Logged-in 
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        message = "You have successfully logged in!"        
        email = session["email"]
        datas = list(records.find({'email':email}))
        return render_template('logged_in.html', email=email, message=message, datas=datas)
    else:
        return redirect(url_for("login"))



@app.route('/logged_in/add', methods=['GET', 'POST'])
def add():
    if "email" in session:
        if request.method == "GET":
            return redirect(url_for("logged_in"))
        if request.method == "POST":
            #Only email works, this line won't work with name or email
            email = session["email"]
            #Initialize the input datas
            event_date = request.form['event_date']
            event_amount = request.form['event_amount']
            event_description = request.form['event_description']
            #Combine all the input
            user_input = {'date': event_date, 'amount': event_amount, 'description': event_description}
            name_stored = "TXN on " + str(event_date)
            # section = {name_stored: user_input}

            # section_num = 1
            # section_name = 'section ' + str(section_num)
            # while {section_name: {"$exists": True}}:
            #     section_num+=1
            #     section_name = 'section ' + str(section_num)
            # else:
            #     section_name = 'section' + str(section_num)
            # section_name = 'section1'
            # if {'section1': {"$exists": True}}:
            #     section_name = 'section2'
            # elif {'section2': {"$exists": True}}:
            #     section_name = 'section3'
            # elif {'section3': {"$exists": True}}:
            #     section_name = 'section4'
            # else:
            #     section_name = 'section5'
            # print(section_name)
           
            
            datas = user_input
            records.update_one({"email": email}, {"$set": {name_stored : user_input}})
            # what.insert(section)
            datas = list(records.find({'email':email}))
        return render_template('logged_in.html', datas=datas)
    else:
        return redirect(url_for("home"))


# @app.route('/logged_in/add', methods=['GET', 'POST'])
# def add():
#     if "email" in session:
#         if request.method == "GET":
#             return redirect(url_for("logged_in"))
#         if request.method == "POST":
#             #Only email works, this line won't work with name or email
#             email = session["email"]
#             #Initialize the input datas
#             event_date = request.form['event_date']
#             event_amount = request.form['event_amount']
#             event_description = request.form['event_description']
#             #Find the email in the data 
#             # user = records.find_one({'email':email})
#             #Combine all the input
#             user_input = {'date': event_date, 'amount': event_amount, 'description': event_description}
            
#             # user["event"] = user_input
            
#             # records.save(user) 
#             # records.update_one({"email": email}, {"$set": {"geolocCountry": event_amount}})
#             name_stored = "TXN on " + str(event_date)
#             records.update_one({"email": email}, {"$set": {name_stored : user_input}})

#             datas = list(records.find({'email':email}))
#         return render_template('logged_in.html', datas=datas)
#     else:
#         return redirect(url_for("login"))


# @app.route('/find')
# def find():
#     user = records.find_one({'name':'a'})
#     return f'<h1>User: {user["email"]} password: {user["password"]} </h1>'

# @app.route('/update')
# def update():
#     email = session["email"]
#     user = records.find_one({'name':email})
#     user["test"] = "test"
#     records.save(user)
#     return '<h1>Updated user!</h>'


#Logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        message1 = "You have successfully logged out!"
        return render_template("home.html", message1=message1)
    else:
        return render_template('home.html')

