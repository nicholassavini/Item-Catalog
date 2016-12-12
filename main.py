from flask import Flask, render_template, request, redirect, abort, url_for
from flask import make_response, flash, jsonify
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, User, Category, Item

import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def category_by_id(id):
    return session.query(Category).filter_by(id=id).one()


def item_by_cat(category_id):
    return session.query(Item).filter_by(category_id=category_id).all()


def item_by_id(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.category_id != category_id:
        return abort(404)
    else:
        return item


def get_names():
    names = session.query(Item.name).all()
    return [n[0].encode("utf-8") for n in names]


def check_price(price):
    try:
        float(price)
        return True
    except ValueError:
        return False


@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, session=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect("/")
    else:
        response = make_response(json.dumps('Failed to revoke token for user.',
                                            400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
def show_catalog():
    items = session.query(Item).order_by(Item.created_date.desc()).limit(6)
    return render_template('catalog.html', items=items)


@app.route('/new/', methods=['GET', 'POST'])
def create_item():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        item_names = get_names()

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category']

        params = dict(name=name, price=price, description=description,
                      category_id=category_id,
                      created_by=login_session['user_id'])

        has_error = False
        if not name:
            has_error = True
            flash("We need a name!")
        if name in item_names:
            has_error = True
            flash("Name already exists!")
        if not price or not check_price(price):
            has_error = True
            flash("We need a valid price!")
        if not description:
            has_error = True
            flash("We need a description!")

        if has_error:
            return render_template("new_item.html", **params)
        else:
            new_item = Item(**params)
            session.add(new_item)
            session.commit()
            return redirect(url_for('show_category', category_id=category_id))
    else:
        return render_template("new_item.html")


@app.route('/<int:category_id>/')
def show_category(category_id):
    items = item_by_cat(category_id)
    return render_template('category.html', items=items,
                           category=category_by_id(category_id))


@app.route('/<int:category_id>/<int:item_id>/')
def show_item(category_id, item_id):
    item = item_by_id(category_id, item_id)
    return render_template('item.html', i=item)


@app.route('/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item_names = get_names()
    item = item_by_id(category_id, item_id)

    if login_session['user_id'] != item.created_by:
        return render_template('error.html')

    if request.method == 'POST':
        old_name = item.name
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category']

        has_error = False
        if not name:
            has_error = True
            flash("We need a name!")
        if name in item_names and name != old_name:
            has_error = True
            flash("Name already exists!")
        if not price or not check_price(price):
            has_error = True
            flash("We need a valid price!")
        if not description:
            has_error = True
            flash("We need a description!")

        if has_error:
            return render_template("edit.html", i=item)
        else:
            item.name = name
            item.price = price
            item.description = description
            item.category_id = category_id

            session.add(item)
            session.commit()

            return redirect(url_for('show_item', category_id=category_id,
                            item_id=item_id))
    else:
        return render_template("edit.html", i=item)


@app.route('/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item = item_by_id(category_id, item_id)
    if login_session['user_id'] != item.created_by:
        return render_template('error.html')
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('show_category', category_id=category_id))
    else:
        return render_template("delete.html", i=item)


# JSON routes
@app.route('/catalog/json/')
def catalog_json():
    return jsonify(Keyboards=[k.serialize for k in item_by_cat(1)],
                   Keysets=[k.serialize for k in item_by_cat(2)],
                   Switches=[s.serialize for s in item_by_cat(3)],
                   Accessories=[a.serialize for a in item_by_cat(4)])


@app.route('/<int:category_id>/json/')
def category_json(category_id):
    return jsonify(Items=[i.serialize for i in item_by_cat(category_id)])


@app.route('/<int:category_id>/<int:item_id>/json/')
def item_json(category_id, item_id):
    item = item_by_id(category_id, item_id)
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
