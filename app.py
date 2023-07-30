"""A simple website with pages for Home, About, List and Contact endpoints."""
import review
from os import environ

from flask import render_template, request, flash, redirect
from models import db, app, User, Order

app.secret_key = environ.get('secret_key')
app.config['SESSION_TYPE'] = 'filesystem'

# Links for the navigation bar
links = [
    {'name': 'Home', 'url': '/'},
    {'name': 'About', 'url': '/about'},
    {'name': 'Login', 'url': '/login'},
    {'name': 'Users', 'url': '/users'},
    {'name': 'Orders', 'url': '/orders'},
    {'name': 'Contact', 'url': '/contact'},
]


@app.route('/')
def index():
    return render_template('home.html', title='Home', navigation=links)


@app.route('/about')
def about():
    """A paragraph about the author/site."""
    return render_template('about.html', title='About', navigation=links)


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


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """
    a form with at least two form fields are used that creates a new entry
    in the table. Include data validation and error handling (e.g. for duplicate
    keys or invalid data types)
    """
    if request.method == 'GET':
        return render_template('adduser.html', title='Add User', navigation=links)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        errors = []
        try:
            user_id = User.query.last()['id'] + 1
        except IndexError:
            user_id = 1

        if not username:
            errors.append('Username is required!')
        if not email:
            errors.append('email is required!')
        if "@" not in email:
            errors.append('Please enter a valid email.')
        if errors:
            for error in errors:
                flash(error, 'error')

        else:
            new_user = User(
                id=user_id,
                username=username,
                email=email,
                phonenumber=request.form['phonenumber'],
                status=request.form['status'],
                is_admin=request.form.get('is_admin'),
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')

@app.route('/updateuser/<int:uid>', methods=['GET', 'POST'])
def updateuser(uid):
    """
    a form that displays a single record and allows change of at least two
    available fields.
    """
    existing_user = User.query.filter_by(id=uid).first()
    if request.method == 'GET':
        return render_template(
            'updateuser.html', title='Update User', user=existing_user, navigation=links
        )
    if request.method == 'POST':
        existing_user.username=request.form['username']
        existing_user.email=request.form['email']
        existing_user.phonenumber=request.form['phonenumber']
        db.session.commit()
        return redirect('/')

@app.route('/deleteuser/<int:uid>', methods=['GET','POST'])
def deleteuser(uid):
    """
    deletes a single row from the database, based on the primary key provided.
    Can use this endpoint from the `/updateuser` endpoint since deletion is
    another form of update.
    """
    existing_user = User.query.filter_by(id=uid).first()
    if request.method == 'POST':
        db.session.delete(existing_user)
        db.session.commit()
        return redirect('/')
    return render_template(
        'updateuser.html', title='Update User', user=existing_user, navigation=links
    )


@app.route('/users')
def users():
    """list all users in an HTML `<table>` structure."""
    user_objs = User.query.all()
    return render_template('users.html', title='Users', users=user_objs, navigation=links)


@app.route('/orders/<int:uid>')
def orders(uid):
    """list all orders in an HTML `<table>` structure."""
    user = User.query.filter(id=uid).first()
    order_objs = Order.query.filter(user_id=uid)
    return render_template('orders.html', title='Orders', orders=order_objs, user=user, navigation=links)


@app.route('/add_order/<int:uid>')
def add_order(uid):
    """Add an order for a specified user"""
    user = User.query.filter(id=uid).first()

    if request.method == 'GET':
        return render_template('add_order.html', title='Add Order',user=user, navigation=links)

    if request.method == 'POST':
        item_name = request.form['item_name']
        item_count = request.form['item_count']
        errors = []
        try:
            order_id = Order.query.last()['id'] + 1
        except IndexError:
            order_id = 1

        if not item_name:
            errors.append('item_name is required!')
        if not item_count:
            errors.append('item_count is required!')
        if errors:
            for error in errors:
                flash(error, 'error')

        else:
            new_order = Order(
                id=order_id,
                item_name=request.form['item_name'],
                item_count=request.form['item_count'],
                total=request.form['item_count'] * .99,
                user_id=uid,
            )
            db.session.add(new_order)
            db.session.commit()
            return redirect('/')
