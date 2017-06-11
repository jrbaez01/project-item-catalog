from flask import render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy.orm import sessionmaker
from item_catalog.flask_app import app
from item_catalog.db import DBSession
from item_catalog.models import User

@app.route('/login')
def login():
	return  render_template('login.html')
	