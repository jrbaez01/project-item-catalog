from flask import render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import Blueprint
from functools import wraps

from item_catalog.db import DBSession
from .models import User, Category, Item

# Define the blueprint: 'catalog', set its url prefix: app.url/catalog
bp = Blueprint('catalog', __name__, url_prefix='/catalog')

# ============================================================================
# Helpers
# ============================================================================


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


# Get all categories to be used later.
categories = DBSession.query(Category).all()


# ============================================================================
# Controlers
# ============================================================================


@bp.route('/')
def index():
    items = DBSession.query(Item, Category)\
                     .join(Category)\
                     .order_by(Item.id.desc())[0:10]
    return render_template('catalog/index.html',
                           cat_name='Latest',
                           categories=categories,
                           items=items)


@bp.route('/<cat_name>/')
def category(cat_name):

    items = DBSession.query(Item, Category)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .order_by(Item.id.desc()).all()
    return render_template('catalog/index.html',
                           cat_name=cat_name,
                           categories=categories,
                           items=items)


@bp.route('/<cat_name>/<item_name>')
def item(cat_name, item_name):
    item = DBSession.query(Item)\
                           .join(Category)\
                           .filter(Category.name == cat_name)\
                           .filter(Item.name == item_name).one_or_none()
    if item is None:
        return render_template('404.html'), 404

    return render_template('catalog/item.html',
                           cat_name=cat_name,
                           categories=categories,
                           item=item)


@bp.route('/<cat_name>/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def item_edit(cat_name, item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()

    if login_session['user_id'] != item.user_id:
        flash(
            "Hey!, if you are not the owner of a item you CANNOT EDIT it.",
            "warning"
        )
        return redirect(url_for('catalog.item',
                                cat_name=cat_name,
                                item_name=item_name))

    if request.method == 'POST':
        item_name = request.form['item_name']
        cat_id, cat_name = request.form['cat'].split('|')
        item_desc = request.form['item_desc']

        if item_name == '' or item_desc == '':
            flash(
                "All fields need to be filled with text.",
                "warning"
            )
            return render_template('catalog/item_edit.html',
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
            return render_template('catalog/item_edit.html',
                                   cat_name=cat_name,
                                   categories=categories,
                                   item={'name': item_name,
                                         'desc': item_desc})
        else:
            flash(
                "The ITEM WAS EDITED successfully.",
                "success"
            )
            return redirect(url_for('catalog.item',
                                    cat_name=cat_name,
                                    item_name=item_name))

    else:
        return render_template('catalog/item_edit.html',
                               cat_name=cat_name,
                               categories=categories,
                               item=item)


@bp.route('/new', methods=['GET', 'POST'])
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
            return render_template('catalog/item_new.html',
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
            return render_template('catalog/item_new.html',
                                   cat_name=cat_name,
                                   categories=categories,
                                   item=item)
        else:
            flash(
                "The ITEM WAS CREATED successfully.",
                "success"
            )
            return redirect(url_for('catalog.item',
                                    cat_name=cat_name,
                                    item_name=item_name))
    else:
        return render_template('catalog/item_new.html',
                               cat_name=request.args.get('cat_name', ''),
                               categories=categories,
                               item=item)


@bp.route('/<cat_name>/<item_name>/remove', methods=['GET', 'POST'])
@login_required
def item_remove(cat_name, item_name):
    item = DBSession.query(Item)\
                            .join(Category)\
                            .filter(Category.name == cat_name)\
                            .filter(Item.name == item_name).one()

    if login_session['user_id'] != item.user_id:
        flash(
            "Hey!, if you are not the owner of a item you CANNOT REMOVE it.",
            "warning"
        )
        return redirect(url_for('catalog.item',
                                cat_name=cat_name,
                                item_name=item_name))

    if request.method == 'POST':
        DBSession.delete(item)
        DBSession.commit()
        flash(
            "The ITEM WAS REMOVED successfully.",
            "success"
        )
        return redirect(url_for('catalog.category', cat_name=cat_name))
    else:
        return render_template('catalog/item_remove.html',
                               cat_name=cat_name,
                               categories=categories,
                               item=item)
