# Lazy SQLAlchemy setup, re http://flask.pocoo.org/snippets/22/
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = None

Base = declarative_base()
DBSession = scoped_session(sessionmaker())

Base.query = DBSession.query_property()


def init_db(engine_url='sqlite://:memory:'):
    global engine
    engine = create_engine(engine_url, echo=True)

    import_models()

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    return DBSession


def import_models():
    import item_catalog.blueprints.auth.models
    import item_catalog.blueprints.catalog.models
