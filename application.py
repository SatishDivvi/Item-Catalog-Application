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
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('categories.html', categories=categories, items=items)


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
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        editCategory.name = request.form['editName']
        session.add(editCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category = editCategory)


@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteCategory = session.query(Category).filter_by(id=category_id).first()
    try:
        deleteCategoryItems = session.query(Item).filter_by(catalog_id = category_id).all()
    except Exception:
        pass
    if request.method == 'POST':
        session.delete(deleteCategory)
        session.commit()
        try:
            session.delete(deleteCategoryItems)
            session.commit()
        except Exception:
            pass
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category = deleteCategory)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id = category_id).one()
    if len(items) == 0:
        items = None
    return render_template('showItems.html', category = category, items = items)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def showItemDescription(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('showDescription.html', item=item, category_id=category_id)


@app.route('/catalog/<int:category_id>/items/new/', methods=['GET', 'POST'])
def addItems(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(name=request.form['addTitle'], description=request.form['addDescription'], category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category.id))
    else:
        return render_template('addItem.html', category=category)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItems(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
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
        return redirect(url_for('showItems', category_id=item.category_id))
    else:
        return render_template('edititem.html', item=item, category=category)
     

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItems(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
