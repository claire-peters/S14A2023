"""A simple website with pages for Home, About, List and Contact endpoints."""

import json
from os import environ
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('postgres_connection_string')
# initialize the app with the extension
db.init_app(app)

# Links for the navigation bar
links = [
    {'name': 'Home', 'url': '/'},
    {'name': 'About', 'url': '/about'},
    {'name': 'Login', 'url': '/login'},
    {'name': 'List', 'url': '/list'},
    {'name': 'Contact', 'url': '/contact'}
]

@app.route('/')
def index():
    return render_template('home.html', title='Home', navigation=links)

@app.route('/about')
def about():
    """A paragraph about the author/site."""
    return render_template('about.html', title='About', navigation=links)

@app.route('/list')
def list():
    """
    Specs:
        displays a <table> with multiple rows. Data should come
        from a list of dictionaries from the Flask application. Use Jinja
        inheritance to construct a base template and the subsequent templates
        to extend the basetemplate.

    """
    # read in json for table Data
    with open('data.json', 'r') as f:
        table_data = json.load(f)
    return render_template('list.html', title='List', navigation=links, table_data=table_data)

@app.route('/registration')
def registration():
    """
    Specs:
        an HTML form with fields for first name, last name, e-mail,
        password and a button. The form should be submitted to the same
        URL using the POST method. The form should be validated using
        Flask-WTF. If the form is valid, the user should be redirected
        to the /l
    """
    return render_template('registration.html', title='Registration', navigation=links)

@app.route('/login')
def login():
    """
    Specs:
        an HTML form with fields for e-mail, password and a button.
        The form should be submitted to the same URL using the POST method.
        The form should be validated using Flask-WTF. If the form is valid,
        the user should be redirected to the /list endpoint.
    """
    return render_template('login.html', title='Login', navigation=links)

@app.route('/contact')
def contact():
    """
    Specs:
        an HTML form with fields for sender's e-mail and a message
        in a <textarea> textbox, with a button.
    """
    return render_template('contact.html', title='Contact', navigation=links)
