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
import os
from datetime import datetime
#sudo pip3 install dnspython

# -- Initialization section --
app = Flask(__name__)
app.secret_key = os.getenv('KEY')
app.config['URL'] = os.getenv("URL")
URL = app.config['URL']


client = pymongo.MongoClient(URL)

#get the database name
db = client.get_database('project')
#get the particular collection that contains the data
records = db.users
transactions = db.data

#The home page, maybe with slide that will show features and stuffs.
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', time = datetime.now())

@app.route('/h0me')
def index1():
    return render_template('h0me.html', time = datetime.now())

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
            message1 = "User Created Successfully! Please login!"
            user_input = {'name': user, 'email': email, 'password': password2, 'total_saving':0, 'total_spending':0, 'account':0}
            # storage = {'email': email, 'holder':{}}
            #insert it in the record collection
            records.insert_one(user_input)

            # transactions.insert_one(storage)
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            # return redirect(url_for("logged_in"), email=new_email, message=message)
            # redirect(url_for("logged_in")
            return render_template('home.html', email=new_email,message1=message1)

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
        # message = "You have successfully logged in!"        
        email = session["email"]
        datas = list(transactions.find({'email':email}))
        user2 = list(records.find({'email':email}))

        return render_template('logged_in.html', email=email, datas=datas, user2=user2)
    else:
        return redirect(url_for("login"))

# @app.route('/profile')
# def profile():
#     if "email" in session:
#         email = session["email"]
#         datas = list(transactions.find({'email':email}))
#         user2 = list(records.find({'email':email}))

#         return render_template('logged_in.html', email=email, datas=datas, user2=user2)
#     else:
#         return redirect(url_for("login"))


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
            event_type = request.form['event_type']

            if event_type == 'Saving':
                user = records.find_one({'email':email})
                user["account"] += int(event_amount)
                user["total_saving"] += int(event_amount)
                records.save(user)

            if event_type == 'Spending':
                user = records.find_one({'email':email})
                user["account"] -= int(event_amount)
                user["total_spending"] += int(event_amount)
                records.save(user)

            #Combine all the input

            user_input = {'date': event_date, 'amount': event_amount, 'description': event_description, 'type': event_type}
            # name_stored = "TXN on " + str(event_date)
            # section = {name_stored: user_input}
            storage = {'email': email, 'holder': user_input}
            transactions.insert_one(storage)

            # transactions.update_one({"email": email}, {"$set": {"1" : user_input}})
            # what.insert(section)
            datas = list(transactions.find({'email':email}))
            user2 = list(records.find({'email':email}))

        return render_template('logged_in.html', datas=datas, user2=user2)
    else:
        return redirect(url_for("home"))



# @app.route('/update')
# def update():
# #    if event_type == 'saving':
#     # total_saving = list(records.find({'email':email}, {'total_saving'}))
#     # total_saving += event_amount
#     # records.update({'email': email}, { "$inc": { "total_saving": event_amount } })
#     event_amount = 32
#     email = session["email"]
#     user = records.find_one({'email':email})
#     user["total_saving"] += event_amount
#     records.save(user)
#     # records.update_one({"email": email}, {"$set": {"total_saving" : total_saving}})
    
#     return f'<h1>Success</h1>'


# @app.route('/find')
# def find():
#     print(records.find({'email':{"$in":['d'],"$exists":"true"}}))
#     user = records.find_one({'name':'a'})
#     return f'<h1>Cant find it</h1>'

@app.route('/pagenotfound')
def pagenotfound():
    return render_template('404.html')

@app.route('/search')
def search():
    if "email" in session:
        email = session["email"]
        user = transactions.find_one({'email':email})
        email = session["email"]
       
        return render_template('search.html', email=email, user=user)
    else:
        return redirect(url_for("login"))

# @app.route('/update')
# def update():
#     email = session["email"]
#     user = records.find_one({'name':email})
#     user["test"] = "test"
#     records.save(user)
#     return '<h1>Updated user!</h>'

# @app.route('/push')
# def push():
#     email = session['email']
#     user = records.find_one({'email':email})
#     user_input = {'date': 'event_date', 'amount': 'event_amount', 'description': 'event_description'}
#     records.update_one({"email": email}, {"$push": {user_input : user_input}})
#     return '<h1>Pushed</h>'

# @app.route('/update_general')
# def update_general():
#     event_date = request.form['event_date']

#     return

#Logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        message1 = "You have successfully logged out!"
        return render_template("home.html", message1=message1)
    else:
        return render_template('home.html')

