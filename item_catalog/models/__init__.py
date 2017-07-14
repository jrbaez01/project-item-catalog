from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from item_catalog.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))

    def __repr__(self):
        """Return a string representation. Useful for debugging."""
        return "<User(name='%s', email='%s')>" % (self.name, self.email)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(250), unique=True)

    def __repr__(self):
        """Return a string representation. Useful for debugging."""
        return "<Category(name='%s')>" % (self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    user = relationship(User)
    category = relationship(Category)

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String(250), unique=True)
    desc = Column(String(250))

    def __repr__(self):
        """Return a string representation. Useful for debugging."""
        return "<Item(name='%s', desc='%s')>" % (self.name, self.desc)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'name': self.name,
            'desc': self.desc,
        }
