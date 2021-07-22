# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]

# name of database
app.config['MONGO_DBNAME'] = 'project'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://project_user:password@cluster0.qf94p.mongodb.net/data?retryWrites=true&w=majority'

print("YESS")

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""

@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    elif request.method == "POST":
#This is storing data from your form
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']
#This is connecting to mongo and inserting data in your "Events" collection
        collection = mongo.db.data
        collection.insert({'event': event_name, 'date': event_date, 'user': user_name})
        events = list(collection.find({}))
        return render_template('index.html', events = events)

