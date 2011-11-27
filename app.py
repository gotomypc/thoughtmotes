import os, datetime, logging, re
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from pymongo import Connection, GEO2D

# configuration

DEBUG = True
SECRET_KEY = 'This should be better'
MONGODB_CONNSTRING = 'mongodb://localhost:27017'
MONGODB_DB = 'thoughtmotes'

        
# application
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config.from_object(__name__)


# routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mote', methods=['POST'])
def addMote():
    mote =  {   'loc': { 
                    'lat' : request.form['lat'], 
                    'long' : request.form['long'] 
                },
                'content' : request.form['content'],
                'date' : datetime.datetime.utcnow(),
                'readcount' : 0,
                'likecount' : 0,
                'flagcount' : 0
            }
    g.db.motes.insert(mote)
    flash('Your thoughts have been set free.')
    return redirect(url_for('index'))

@app.route('/motes-nearby')
def motesNearby():
    return render_template('nearby.html')


# lifecycle functions

@app.before_request
def beforeRequest():
    g.conn = connectDB()
    g.db = g.conn[app.config['MONGODB_DB']]
    initDB()

@app.teardown_request
def afterRequest(exception):
    g.conn.end_request()


# functions

def connectDB():
    return Connection(app.config['MONGODB_CONNSTRING'])

def initDB():
    g.db.motes.create_index("handle")
    g.db.motes.create_index([("loc", GEO2D)])

def parseMongoURI(uri):
    """Parse the MongoHQ connection string and grab the DB name"""
    [[user, pw, host, port, db]] = re.findall("^.*://(.*?):(.*?)@(.*?):(\d+)/(.*)$", uri)
    logging.debug(user + " " + pw + " " + host + " " + port + " " + db)
    app.config['MONGODB_DB'] = db

# launch application

if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    dbConnString = os.environ.get("MONGOHQ_URL", "")
    logging.debug("Connection string: " + dbConnString)
    if dbConnString != "":
        app.config['MONGODB_CONNSTRING'] = dbConnString
        logging.debug("Switching to Heroku's mongodb")
        parseMongoURI(dbConnString)
    app.run(host='0.0.0.0', port=port)
    
