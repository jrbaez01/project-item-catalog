# Lazy SQLAlchemy setup, re http://flask.pocoo.org/snippets/22/
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None
session_maker = sessionmaker()
DBSession = scoped_session(session_maker)

Base = declarative_base()
Base.query = DBSession.query_property()


def init_db(engine_url='sqlite://:memory:'):
    import item_catalog.models
    global engine

    engine = create_engine(engine_url, echo=True)

    DBSession.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    return DBSession
