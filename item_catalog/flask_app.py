from flask import Flask
from flask import render_template, redirect, url_for

app = None


def init_app():
    global app
    app = Flask(__name__.split('.')[0])
    app.secret_key = 'super_secret_key_TODO'

    register_blueprints(app)
    register_handlers(app)

    return app


def register_blueprints(app):
    from item_catalog.blueprints.auth.controlers import bp as auth_bp
    from item_catalog.blueprints.catalog.controlers import bp as catalog_bp
    from item_catalog.blueprints.api.controlers import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(api_bp)


def register_handlers(app):
    @app.route('/')
    def index():
        return redirect(url_for('catalog.index'))

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
