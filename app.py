"""
A simple Flask app consisting of:
- a landing page 
- a page "datetime" showing the current datetime in the server's timezone and another datetime in the UTC timezone
- a page "pacifictime" showing the current datetime in pacific time.
"""

from flask import Flask
from datetime import datetime as dt
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World! Welcome to CSCI S-14a.<br><a href=/datetime>datetime</a><br><a href="/pacifictime">pacific</a>'

@app.route('/datetime')
def datetime():
    now = dt.now()
    utc = dt.utcnow()
    return f'Current server timezone date time {now}. Current UTC datetime is {utc}'

@app.route('/pacifictime')
def pacifictime():
    return (f'Current Pacific timezone date time {dt.now(tz=pytz.timezone("US/Pacific"))}')
if __name__ == '__main__':
    app.run(debug=True)
