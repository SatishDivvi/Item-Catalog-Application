#!/usr/bin/env python2

from flask import Flask, render_template, request, url_for, redirect, flash
from flask import jsonify
from database_setup import Category, Item, Base, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
                        open('client_secrets.json', 'r').
                        read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


# Route for Specific Category Item API Endpoint
@app.route('/catalog/<int:category_id>/items/<int:item_id>/itemjson')
def getCategorySpecificItemJSON(category_id, item_id):
    '''Returns specific Category Item in JSON format'''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(
                                        id=item_id,
                                        category_id=category_id).one()
    return jsonify(Item=[item.serialize])


# Route for logging into the application
@app.route('/login')
def showLogin():
    '''Creates state variable and assigns to login_session variable
    and returns login.html'''
    if 'username' in login_session:
        return redirect('/catalog')
    state = (
            ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32)))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/googleconnect', methods=['POST'])
def googleconnect():
    """Connects with Google OAuth for Authentication
    and creates login session"""
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
    url = (
            'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
            .format(access_token))
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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("""Current user is already
         connected."""), 200)
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

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> """
    flash("you are now logged in as {}".format(login_session['username']))
    return output


@app.route('/facebookconnect', methods=['POST'])
def facebookconnect():
    """Connects with Facebook OAuth for Authentication
    and creates login session"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(
                        open('fb_client_secrets.json', 'r').
                        read())['web']['app_id']
    app_secret = json.loads(
                            open('fb_client_secrets.json', 'r').
                            read())['web']['app_secret']
    url = """https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s""" % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = """https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email""" % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    url = """https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200""" % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ style = "width: 300px; height: 300px;border-radius:
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> """
    flash("you are now logged in as {}".format(login_session['username']))
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Delete the login session and disconnect using Google OAuth"""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps("""Current user
        not connected."""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = (
            'https://accounts.google.com/o/oauth2/revoke?token=%s' %
            login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash('You are disconnected successfully')
        return redirect(url_for('showLogin'))
    else:
        response = make_response(json.dumps("""Failed to revoke token for
        given user.""", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbdisconnect')
def fbdisconnect():
    """Delete the login session and disconnect using Facebook OAuth"""
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = (
            'https://graph.facebook.com/%s/permissions?access_token=%s' %
            (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['provider']
    del login_session['picture']
    del login_session['facebook_id']
    del login_session['user_id']
    flash('You are disconnected successfully')
    return redirect(url_for('showLogin'))


@app.route('/disconnect')
def disconnect():
    '''Base disconnect Module for routing to appropriate
    social disconnect'''
    if login_session['provider'] == 'google':
        return redirect(url_for('gdisconnect'))
    elif login_session['provider'] == 'facebook':
        return redirect(url_for('fbdisconnect'))


@app.route('/')
@app.route('/catalog/')
def showCategories():
    '''Display's categories and last 10 added items'''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    if len(categories) == 0:
        categories = None
    if 'username' not in login_session:
        return render_template(
                                'publicCategories.html',
                                categories=categories,
                                items=items)
    return render_template(
                            'categories.html',
                            categories=categories,
                            items=items)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def addCategory():
    '''Add's new category to the Category Table and
    redirects to /catalog route.'''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
                                name=request.form['addCategory'],
                                user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("Added New Category")
        return redirect(url_for('showCategories'))
    else:
        return render_template('addCategory.html')


@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    '''Edit existing category and
    redirects to /catalog route.'''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editCategory = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(editCategory.user_id)
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        editCategory.name = request.form['editName']
        session.add(editCategory)
        session.commit()
        flash("Edited Category")
        return redirect(url_for('showCategories'))
    else:
        if creator.id != login_session['user_id']:
            flash('Sorry, you are not the owner of the category to edit.')
            return redirect('/catalog')
        return render_template('editCategory.html', category=editCategory)


@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteCategory = session.query(Category).filter_by(id=category_id).first()
    creator = getUserInfo(deleteCategory.user_id)
    try:
        deleteCategoryItems = (
                                session.query(Item).
                                filter_by(category_id=category_id).all())
    except Exception:
        pass
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(deleteCategory)
        session.commit()
        try:
            for deleteCategoryItem in deleteCategoryItems:
                session.delete(deleteCategoryItem)
                session.commit()
        except Exception:
            pass
        flash("Deleted Category")
        return redirect(url_for('showCategories'))
    else:
        if creator.id != login_session['user_id']:
            flash('Sorry, you are not the owner of the category to delete.')
            return redirect('/catalog')
        return render_template('deleteCategory.html', category=deleteCategory)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if len(items) == 0:
        items = None
    if 'username' not in login_session:
        return render_template(
                                'showPublicItems.html',
                                category=category,
                                items=items)
    return render_template('showItems.html', category=category, items=items)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def showItemDescription(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template(
                            'showDescription.html',
                            item=item,
                            category_id=category_id)


@app.route('/catalog/<int:category_id>/items/new/', methods=['GET', 'POST'])
def addItems(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(
                        name=request.form['addTitle'],
                        description=request.form['addDescription'],
                        category_id=category_id,
                        user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('Added New Item')
        return redirect(url_for('showItems', category_id=category.id))
    else:
        if creator.id != login_session['user_id']:
            flash("""You are not the owner of the category,
             Hence you are not allowed to add items to it.""")
            return redirect(url_for('showItems', category_id=category_id))
        return render_template('addItem.html', category=category)


@app.route(
            '/catalog/<int:category_id>/items/<int:item_id>/edit',
            methods=['GET', 'POST'])
def editItems(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    distinctCategories = session.query(Category).distinct()
    item = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        select = request.form['category']
        newCategory = session.query(Category).filter_by(name=select).one()
        if newCategory.id != category.id:
            item.category_id = newCategory.id
            session.commit()
        if request.form['editTitle']:
            item.name = request.form['editTitle']
            session.commit()
        if request.form['editDescription']:
            item.description = request.form['editDescription']
            session.commit()
        flash('Updated Requested Item')
        return redirect(url_for('showItems', category_id=item.category_id))
    else:
        if creator.id != login_session['user_id']:
            flash("""You are not the owner of the category,
            Hence you are not allowed to edit the item.""")
            return redirect(url_for('showItems', category_id=category_id))
        return render_template(
                                'edititem.html',
                                item=item,
                                category=category,
                                distinctCategories=distinctCategories)


@app.route(
            '/catalog/<int:category_id>/items/<int:item_id>/delete',
            methods=['GET', 'POST'])
def deleteItems(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(
                                        id=item_id,
                                        category_id=category_id).one()
    creator = getUserInfo(item.user_id)
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Deleted Requested Item')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        if creator.id != login_session['user_id']:
            flash("""You are not the owner of the category,
            Hence you are not allowed to delete the item.""")
            return redirect(url_for('showItems', category_id=category_id))
        return render_template(
                                'deleteItem.html',
                                category_id=category_id,
                                item=item)


# Create User in Database
def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = Users(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


# Get User Info
def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one()
    return user


# Get User ID
def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
