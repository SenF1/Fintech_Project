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

#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.config['app.secret_key'] = os.getenv("app.secret_key")
app.secret_key = app.config["app.secret_key"]

#connect to your Mongo DB database
client = pymongo.MongoClient('mongodb+srv://project_user:@cluster0.qf94p.mongodb.net/project?retryWrites=true&w=majority')

#get the database name
db = client.get_database('project')
#get the particular collection that contains the data
records = db.users


#This should be a home page, maybe with slide that will show features and stuffs.
# Need to create another html page and make sure all pages include nav bar
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')



#assign URLs to have a particular route 
@app.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        elif user == "":
            message = 'Please enter a username'
            return render_template('index.html', message=message)
        elif email == "":
            message = 'Please enter a email'
            return render_template('index.html', message=message)
        elif password1 == "":
            message = 'Please enter a password'
            return render_template('index.html', message=message)
        elif password2 == "":
            message = 'Please enter re-enter password'
            return render_template('index.html', message=message)
        elif email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        elif password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            message = "User Created Successfully!"
            user_input = {'name': user, 'email': email, 'password': password2}
            #insert it in the record collection
            records.insert_one(user_input)
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email, message=message)
    return render_template('index.html')



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
            return render_template('login.html', message=message)
        # elif password == "":
        #     bad_message = "Please enter your password!"
        #     return render_template('login.html', bad_message=bad_message)
        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            # if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            # if passwordcheck:
            #     session["email"] = email_val
            if password == passwordcheck:
                session['email'] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        message = "You have successfully logged in!"        
        email = session["email"]
        return render_template('logged_in.html', email=email, message=message)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        message = "You have successfully logged out!"
        return render_template("signout.html", message=message)
    else:
        return render_template('home.html')



















# # # A - Individual Post Pages
# from bson.objectid import ObjectId

# # # B - Accounts and Sessions
# from flask import session, url_for


# # -- Initialization section --
# app = Flask(__name__)

# # name of database
# app.config['MONGO_DBNAME'] = 'database'

# # URI of database
# app.config['MONGO_URI'] = 'mongodb+srv://project_user:61WAQwDQJZPYFjmF@cluster0.qf94p.mongodb.net/project?retryWrites=true&w=majority'

# # # B - Accounts and Sessions
# app.secret_key = 'wbdekjdewjkwn'
# session['username'] = "My Name"

# mongo = PyMongo(app)

# # -- Routes section --
# # INDEX

# @app.route('/')
# @app.route('/index')
# def index():
#     # connect to db
#     collection = mongo.db.data

#     # find all data
#     events = collection.find({})

#     # return message to user
#     return render_template('index.html', events = events)
# # CONNECT TO DB, ADD DATA

# @app.route('/add')
# def add():
#     # connect to the database
#     events = mongo.db.data

#     # insert new data
#     events.insert({'event': "Homecoming", 'date': "2019-05-21"})

#     # return a message to the user
#     return "event added"


# @app.route('/events/new', methods=['GET', 'POST'])
# def new_event():
#     if request.method == "GET":
#         return render_template('new_event.html')
#     else:
#         event_name = request.form['event_name']
#         event_date = request.form['event_date']
#         user_name = request.form['user_name']

#         events = mongo.db.events
#         events.insert({'event': event_name, 'date': event_date, 'user': user_name})
#         return redirect('/')


# #### ADVANCED CONCEPTS ####
# # A - Individual Post Pages
# @app.route('/events/<eventID>')
# def event(eventID):
#     collection = mongo.db.data
#     event = collection.find_one({'_id' : ObjectId(eventID)})

#     return render_template('event.html', event = event)

# # C - New User Sign Up
# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
#     if request.method == 'POST':
#         users = mongo.db.users
#         existing_user = users.find_one({'name' : request.form['username']})

#         if existing_user is None:
#             users.insert({'name' : request.form['username'], 'password' : request.form['password']})
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))

#         return 'That username already exists! Try logging in.'

#     return render_template('signup.html')

# # D - Logging In
# @app.route('/login', methods=['POST'])
# def login():
#     users = mongo.db.users
#     login_user = users.find_one({'name' : request.form['username']})

#     if login_user:
#         if request.form['password'] == login_user['password']:
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))

#     return 'Invalid username/password combination'

# # E - Log Out
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

# # F - Gated Pages
# @app.route('/events/myevents')
# def myevents():
#     collection = mongo.db.events
#     username = session['username']
#     events = collection.find({'user' : username})

#     return render_template('my_events.html', events = events)