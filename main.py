from flask import Flask, render_template, request, redirect, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, User, Category, Item

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def category_by_id(id):
    return session.query(Category).filter_by(id=id).one()


@app.route('/')
def show_catalog():
    items = session.query(Item).order_by(Item.created_date.desc()).limit(6)
    return render_template('catalog.html', items=items)


@app.route('/login')
def login():
    return "This will log the user in"


@app.route('/logout')
def logout():
    return "This will log the user out"


@app.route('/new')
def create_item():
    return "This will create an item"


@app.route('/<int:category_id>/')
def show_category(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category.html', items=items,
                           category=category_by_id(category_id))


@app.route('/<int:category_id>/<int:item_id>/')
def show_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.category_id == category_id:
        return render_template('item.html', i=item)
    else:
        return abort(404)


@app.route('/<int:category_id>/<int:item_id>/edit')
def edit_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template("edit.html", i=item)


@app.route('/<int:category_id>/<int:item_id>/delete')
def delete_item(category_id, item_id):
    return "this will delete an item"


# JSON routes
@app.route('/catalog/json')
def catalog_json():
    return "presents the entire catalog in json format"


@app.route('/<int:category_id>/json')
def category_json():
    return "presents an entire category in json format"


@app.route('/<int:category_id>/<int:item_id>/json')
def item_json():
    return "presents an item in json format"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)