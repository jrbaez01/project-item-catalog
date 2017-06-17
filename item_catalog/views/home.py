from flask import render_template, request, redirect, jsonify, url_for, flash
from item_catalog.flask_app import app
from item_catalog.db import DBSession
from item_catalog.models import User, Category, Item

categories = Category.query.all()

@app.route('/')
@app.route('/catalog')
def catalog():
    items = DBSession.query(Item, Category).join(Category)[0:10]
    return  render_template('index.html',
                             cat_name='Latest',
                             categories=categories,
                             items=items)


@app.route('/catalog/<cat_name>')
def category(cat_name):
    items = DBSession.query(Item, Category)\
                            .join(Category)\
                            .filter(Category.name == cat_name).all()
    return  render_template('index.html',
                             cat_name=cat_name,
                             categories=categories,
                             items=items)


@app.route('/catalog/<cat_name>/<item_name>')
def item(cat_name , item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()
    return  render_template('item.html',
                             cat_name=cat_name,
                             categories=categories,
                             item=item)

@app.route('/catalog/<cat_name>/new', methods=['GET', 'POST'])
def item_new(cat_name):

    if request.method == 'POST':
        item_name = request.form['item_name']
        cat_id, cat_name = request.form['cat'].split('|')
        item = Item()
        item.category_id = cat_id
        item.name = item_name
        item.desc = request.form['item_desc']
        DBSession.add(item)
        DBSession.commit()
        return redirect(url_for('item', cat_name=cat_name, item_name=item_name))
    else:
        return  render_template('item_new.html',
                                 cat_name=cat_name,
                                 categories=categories)

@app.route('/catalog/<cat_name>/<item_name>/edit', methods=['GET', 'POST'])
def item_edit(cat_name , item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()
    if request.method == 'POST':
        item_name = request.form['item_name']
        cat_id, cat_name = request.form['cat'].split('|')
        item.category_id = cat_id
        item.name = item_name
        item.desc = request.form['item_desc']

        DBSession.commit()
        return redirect(url_for('item', cat_name=cat_name, item_name=item_name))
    else:
        return  render_template('item_edit.html',
                                 cat_name=cat_name,
                                 categories=categories,
                                 item=item)


@app.route('/catalog/<cat_name>/<item_name>/remove', methods=['GET', 'POST'])
def item_remove(cat_name , item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()
    if request.method == 'POST':
        DBSession.delete(item)
        DBSession.commit()
        return redirect(url_for('category', cat_name=cat_name))
    else:
        return  render_template('item_remove.html',
                                 cat_name=cat_name,
                                 categories=categories,
                                 item=item)
