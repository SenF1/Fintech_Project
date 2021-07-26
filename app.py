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

# transactions = db.data

#The home page, maybe with slide that will show features and stuffs.
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')



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
            user_input = {'name': user, 'email': email, 'password': password2, 'data':{'event': "", 'date': "", 'user': ""}}
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
        return render_template('logged_in.html', email=email, message=message)
    else:
        return redirect(url_for("login"))



@app.route('/logged_in/add', methods=['GET', 'POST'])
def add():
    if "email" in session:
        if request.method == "GET":
            return render_template('logged_in.html')
        elif request.method == "POST":
            # name = session["name"]
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            user_name = request.form['user_name']
            user_input = {'event': event_name, 'date': event_date, 'user': user_name}
            records.insert(user_input)  
            # db.record.update({user_input})
            # db.records.update.many({'event': ""}, {'event': event_name})
            # records.save({'_id':{"$oid":"60ff095966b4e9d5f18303b7"}, 'name':"David"})
            # db.records.update({'event':""}, {$set: {'name':"new name"}})
            # db.records.update({"name":name}, {"$set":{'data':user_input}})

            # myquery = { "name": name }
            # newvalues = { "$set": { "address": "Canyon 123" } }
            # col.update_one(myquery, newvalues)

            datas = list(records.find({}))


            # for i in datas:
            #     if i['email'] == 'email':  
        return render_template('logged_in.html', datas=datas)
    else:
        return redirect(url_for("login"))



#Logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        message1 = "You have successfully logged out!"
        return render_template("home.html", message1=message1)
    else:
        return render_template('home.html')

