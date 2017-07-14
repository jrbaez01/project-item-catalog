from item_catalog.flask_app import init_app
from item_catalog.db import init_db

app = init_app()
DBSession = init_db(engine_url='sqlite:///item_catalog.db')


@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()

import item_catalog.views
