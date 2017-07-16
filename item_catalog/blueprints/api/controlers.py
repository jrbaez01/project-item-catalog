from flask import Blueprint, jsonify, make_response
import json


from item_catalog.db import DBSession
from item_catalog.blueprints.catalog.models import Category, Item

# Define the blueprint: 'api', set its url prefix: app.url/api/v1
# version v1, in the future I could create a v2 api blueprint version
# and keep support for version v1
bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Get all categories to be used later.
categories = DBSession.query(Category).all()


# ============================================================================
# Controlers
# ============================================================================


@bp.route('/catalog')
def catalog_json():
    output = []
    for category in categories:
        items = DBSession.query(Item).filter_by(category_id=category.id).all()
        serialized_category = category.serialize
        serialized_category['items'] = [i.serialize for i in items]
        output.append(serialized_category)
    return jsonify(categories=output)


@bp.route('/catalog/item/<int:item_id>')
def item_json(item_id):
    item = DBSession.query(Item).filter_by(id=item_id).one_or_none()
    if item:
        return jsonify(item=item.serialize)

    response = make_response(json.dumps('Item not found'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response


@bp.route('/')
@bp.route('/<path:endpoint>')
def endpoint_not_valid(endpoint=None):
    response = make_response(json.dumps('Api endpoint is not valid.'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response
