from item_catalog.flask_app import init_app
from item_catalog.db import init_db

DBSession = init_db(engine_url='sqlite:///item_catalog.db')
app = init_app()


@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()
