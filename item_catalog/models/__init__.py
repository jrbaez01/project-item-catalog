from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from item_catalog.db import Base

class User(Base):
    __tablename__ = 'user'

    id       = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name     = Column(String(250), nullable=False)
    email    = Column(String(250), nullable=False)
    picture  = Column(String(250))

    def __repr__(self):
        return "<User(name='%s', email='%s', password='%s')>" % (
                             self.name, self.email, self.password)


class Category(Base):
    __tablename__ = 'category'

    id   = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(250))

    def __repr__(self):
        return "<Category(name='%s')>" % (self.name)


class Item(Base):
    __tablename__ = 'item'

    user        = relationship(User)
    category    = relationship(Category)

    id          = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    user_id     = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    name        = Column(String(250))
    desc        = Column(String(250))

    def __repr__(self):
        return "<Item(name='%s', desc='%s')>" % (
                             self.name, self.desc)
