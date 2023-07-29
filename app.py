"""A simple website with pages for Home, About, List and Contact endpoints."""

import json
from flask import render_template, request, url_for, flash, redirect
from models import db, app, User

# Links for the navigation bar
links = [
    {'name': 'Home', 'url': '/'},
    {'name': 'About', 'url': '/about'},
    {'name': 'Login', 'url': '/login'},
    {'name': 'List', 'url': '/list'},
    {'name': 'Contact', 'url': '/contact'},
    {'name': 'Users', 'url': '/users'}
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


@app.route('/adduser')
def adduser():
    """
    a form with at least two form fields are used that creates a new entry
    in the table. Include data validation and error handling (e.g. for duplicate
    keys or invalid data types)
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        status = request.form['status']
        is_admin = request.form['is_admin']

        if not username:
            flash('Username is required!')
        elif not email:
            flash('email is required!')
        else:
            new_user = User(
                username=username,
                email=email,
                phonenumber=phonenumber,
                status=status,
                is_admin=is_admin,
            )
            db.session.add(new_user)
            db.session.commit()

    return render_template('adduser.html', title='Add User', navigation=links)

@app.route('/updateuser')
def updateuser():
    """
    a form that displays a single record and allows change of at least two
    available fields.
    """
    return render_template('updateuser.html', title='Update User', navigation=links)

@app.route('/deleteuser')
def deleteuser():
    """
    deletes a single row from the database, based on the primary key provided.
    Can use this endpoint from the `/updateuser` endpoint since deletion is
    another form of update.
    """
    return render_template('deleteuser.html', title='Delete User', navigation=links)

@app.route('/users')
def users():
    """list all the users from the table, in an HTML `<table>` structure."""
    user_objs = User.query.all()
    return render_template('users.html', title='Users', users=user_objs, navigation=links)
