from flask import render_template, request, jsonify, url_for, flash, abort
from flask import make_response, redirect
from flask import session as login_session
from flask import Blueprint
from oauth2client import client
import httplib2
import requests
import random
import string
import json

from item_catalog.db import DBSession
from .models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp = Blueprint('auth', __name__, url_prefix='/auth')


# ============================================================================
# Helpers
# ============================================================================

# Set path to the Web application client_secret_*.json file you
# downloaded from the Google API Console:
# https://console.developers.google.com/apis/credentials
# TODO: move to config.
CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_ID = json.loads(
    open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    DBSession.add(newUser)
    DBSession.commit()
    user = DBSession.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = DBSession.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = DBSession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# ============================================================================
# Controlers
# ============================================================================


@bp.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32)
    )
    login_session['state'] = state
    return render_template('auth/login.html', STATE=state)


@bp.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    # (Receive auth_code by HTTPS POST)
    if request.method == 'POST':
        # Validate state token
        if request.args.get('state') != login_session['state']:
            response = make_response(json.dumps('Invalid state.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If this request does not have `X-Requested-With` header,
        # this could be a CSRF
        if not request.headers.get('X-Requested-With'):
            response = make_response(
                json.dumps('Request does not have `X-Requested-With` header.'),
                403
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Obtain one time authorization code
        auth_code = request.data

        # Exchange auth code for access token, refresh token,
        # and ID token(credentials object)
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                CLIENT_SECRET_FILE,
                ['profile', 'email'],
                auth_code)
        except client.FlowExchangeError:
            response = make_response(
                json.dumps('Failed to upgrade the authorization code.'),
                401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        http = httplib2.Http()
        result = json.loads(http.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(
                json.dumps("Token's user ID doesn't match given user ID."), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_credentials = login_session.get('credentials')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_credentials is not None and gplus_id == stored_gplus_id:
            flash(
                "You were already logged in as %s" % login_session['username'],
                "info")
            response = make_response(
                json.dumps('Current user is already connected.'), 200
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response = make_response(
                json.dumps("Token's client ID does not match app's."), 401
            )
            print "Token's client ID does not match app's."
            response.headers['Content-Type'] = 'application/json'
            return response

        # Store the access token in the session for later use.
        login_session['credentials'] = credentials.to_json()
        login_session['gplus_id'] = gplus_id

        # Call Google API
        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        userinfo = answer.json()

        login_session['username'] = userinfo['name']
        login_session['picture'] = userinfo['picture']
        login_session['email'] = userinfo['email']

        # See if a user exists, if it doesn't make a new one
        local_user_id = getUserID(login_session['email'])
        if not local_user_id:
            local_user_id = createUser(login_session)

        login_session['user_id'] = local_user_id
        login_session['loggedin'] = True

        flash(
            "You are now logged in as %s" % login_session['username'],
            "success")

        response = make_response(
            json.dumps("You are now logged in."), 200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    return redirect('/login')


# DISCONNECT - Revoke a current user's token and reset their login_session
@bp.route('/gdisconnect')
def gdisconnect():
    # return login_session.get('credentials')
    # Only disconnect a connected user.
    if login_session.get('credentials'):
        credentials = client.OAuth2Credentials.from_json(
            login_session.get('credentials')
        )
    else:
        flash(
            "Current user not connected.",
            "warning")
        return redirect('/')

    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]
    # return result['status']
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['loggedin']

        flash(
            "You were successfully disconnected.",
            "info")
    else:
        # For whatever reason, the given token was invalid.
        # TODO: handle case when the token expire
        flash(
            "Failed to revoke token for given user.",
            "danger")
    return redirect('/')
