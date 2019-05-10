#!/usr/bin/env python2

from flask import Flask, render_template, request, url_for, redirect
from database_setup import Category, Item, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


@app.route('/')
@app.route('/catalog/')
def showCategories():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def addCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newCategory = Category(name=request.form['addCategory'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('addCategory.html')


@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    return None

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
