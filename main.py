from flask import Flask, render_template, request, redirect, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, User, Category, Item

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def show_catalog():
    return render_template('catalog.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)