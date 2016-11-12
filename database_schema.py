from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime

Base = declarative_base()

class User(Base):
    """
    Creates the 'users' table. Name, email, and picture all come from the user's
    gmail account.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    email = Column(String(250), nullable=False)
    image = Column(String(250))


class Category(Base):
    """ Creates 'categories' table, containing all possible item categories """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    category = Column(String(80))


class Item(Base):
    """
    Creates the 'items' table, containing all the releveant information for
    a given item
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Category)
    price = Column(Float)
    description = Column(Text)
    image = Column(String(250))
    created_by = Column(Integer, ForeignKey('users.id'))
    users = relationship(User)
    created_date = Column(DateTime, default=datetime.datetime.now)
    last_updated = Column(DateTime, default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
