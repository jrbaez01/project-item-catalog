from item_catalog import db


class User(db.Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    picture = db.Column(db.String(250))

    def __repr__(self):
        """Return a string representation. Useful for debugging."""
        return "<User(name='%s', email='%s')>" % (self.name, self.email)
