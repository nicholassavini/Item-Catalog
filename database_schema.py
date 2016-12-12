from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric, DateTime
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

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'         : self.name,
        }


class Category(Base):
    """ Creates 'categories' table, containing all possible item categories """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    category = Column(String(80))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category'         : self.category,
        }


class Item(Base):
    """
    Creates the 'items' table, containing all the releveant information for
    a given item
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    categories = relationship(Category)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship(User)
    created_date = Column(DateTime, default=datetime.datetime.now)
    last_updated = Column(DateTime, default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id'           : self.id,
            'name'         : self.name,
            'price'        : self.price,
            'description'  : self.description,
            'created_by'   : self.created_by
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
