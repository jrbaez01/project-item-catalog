from flask import render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from functools import wraps
from item_catalog.flask_app import app
from item_catalog.db import DBSession
from item_catalog.models import User, Category, Item

categories = Category.query.all()

# Helper functions

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash(
                "You need to be logged in order to create/edit/remove items.",
                "warning"
            )
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# views functions

@app.route('/')
@app.route('/catalog')
def catalog():
    items = DBSession.query(Item, Category).join(Category)[0:10]
    return  render_template('index.html',
                             cat_name='Latest',
                             categories=categories,
                             items=items)


@app.route('/catalog.json')
def catalog_json():
    output = []
    for category in categories:
        items = DBSession.query(Item).filter_by(category_id=category.id).all()
        serialized_category = category.serialize
        serialized_category['items'] = [i.serialize for i in items]
        output.append(serialized_category)
    return jsonify(categories=output)


@app.route('/catalog/<cat_name>/')
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


@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def item_new():
    item = Item()
    if request.method == 'POST':
        item_name = request.form['item_name']
        cat_id, cat_name = request.form['cat'].split('|')
        item_desc = request.form['item_desc']

        if item_name == '' or item_desc == '':
            flash(
                "All fields need to be filled with text.",
                "warning"
            )
            return  render_template('item_new.html',
                                    cat_name=cat_name,
                                    categories=categories,
                                    item={'name': item_name,
                                          'desc': item_desc})

        try:
            item.user_id = login_session['user_id']
            item.category_id = cat_id
            item.name = item_name
            item.desc = item_desc
            DBSession.add(item)
            DBSession.commit()
        except Exception as e:
            flash(
                e.message,
                "danger"
            )
            DBSession.rollback()
            return  render_template('item_new.html',
                                    cat_name=cat_name,
                                    categories=categories,
                                    item=item)
        else:
            flash(
                "The ITEM WAS CREATED successfully.",
                "success"
            )
            return redirect(url_for('item',
                                    cat_name=cat_name,
                                    item_name=item_name))
    else:
        return  render_template('item_new.html',
                                cat_name=request.args.get('cat_name', ''),
                                categories=categories,
                                item=item)


@app.route('/catalog/<cat_name>/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def item_edit(cat_name , item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()

    if login_session['user_id'] != item.user_id:
        flash(
            "Hey!, if you are not the owner of a item you CANNOT EDIT it.",
            "warning"
        )
        return redirect(url_for('item', cat_name=cat_name, item_name=item_name))

    if request.method == 'POST':
        item_name = request.form['item_name']
        cat_id, cat_name = request.form['cat'].split('|')
        item_desc = request.form['item_desc']

        if item_name == '' or item_desc == '':
            flash(
                "All fields need to be filled with text.",
                "warning"
            )
            return  render_template('item_edit.html',
                                    cat_name=cat_name,
                                    categories=categories,
                                    item={'name': item_name,
                                          'desc': item_desc})

        try:
            item.category_id = cat_id
            item.name = item_name
            item.desc = item_desc
            DBSession.commit()
        except Exception as e:
            DBSession.rollback()
            flash(
                e.message,
                "danger"
            )
            return  render_template('item_edit.html',
                                    cat_name=cat_name,
                                    categories=categories,
                                    item={'name': item_name,
                                          'desc': item_desc})
        else:
            flash(
                "The ITEM WAS EDITED successfully.",
                "success"
            )
            return redirect(url_for('item',
                                    cat_name=cat_name,
                                    item_name=item_name))
        
    else:
        return  render_template('item_edit.html',
                                cat_name=cat_name,
                                categories=categories,
                                item=item)


@app.route('/catalog/<cat_name>/<item_name>/remove', methods=['GET', 'POST'])
@login_required
def item_remove(cat_name , item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()

    if login_session['user_id'] != item.user_id:
        flash(
            "Hey!, if you are not the owner of a item you CANNOT REMOVE it.",
            "warning"
        )
        return redirect(url_for('item', cat_name=cat_name, item_name=item_name))

    if request.method == 'POST':
        DBSession.delete(item)
        DBSession.commit()
        flash(
            "The ITEM WAS REMOVED successfully.",
            "success"
        )
        return redirect(url_for('category', cat_name=cat_name))
    else:
        return  render_template('item_remove.html',
                                 cat_name=cat_name,
                                 categories=categories,
                                 item=item)

