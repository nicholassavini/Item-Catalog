from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """
    Creates the 'user' table. Name, email, and picture all come from the user's
    gmail account.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Categories(Base):
    """ Creates 'categories' table, containing all possible item categories """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    category = Column(String(80))

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
