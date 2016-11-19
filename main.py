from flask import Flask, render_template, request, redirect, abort, url_for
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


@app.route('/login/')
def login():
    return "This will log the user in"


@app.route('/logout/')
def logout():
    return "This will log the user out"


@app.route('/new/', methods=['GET', 'POST'])
def create_item():
    ## still requires a lot of work need to add categories and user
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        params = dict(name=name, price=price, description=description)
        has_error = False

        if not name:
            has_error = True
            params['name_class'] = "has-error"
            params['name_error'] = "We need an item name!"
        if not price:
            has_error = True
            params['price_class'] = "has-error"
            params['price_error'] = "We need a price!"
        if not description:
            has_error = True
            params['description_class'] = "has-error"
            params['description_error'] = "We need a description!"

        if has_error:
            return render_template("new_item.html", **params)
        else:
            new_item = Item(name=name, price=price, description=description)
            session.add(Item)
            session.commit()
            return redirect(url_for('show_item', category_id=category_id,
                            item_id=item_id))
    else:
        return render_template("edit.html", i=item)


@app.route('/<int:category_id>/')
def show_category(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category.html', items=items,
                           category=category_by_id(category_id))


@app.route('/<int:category_id>/<int:item_id>/')
def show_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.category_id != category_id:
        return abort(404)
    return render_template('item.html', i=item)


@app.route('/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.category_id != category_id:
        return abort(404)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category']

        has_error = ""
        if not name:
            has_error += "name"
        if not price:
            has_error += "price"
        if not description:
            has_error += "description"

        if has_error:
            return render_template("edit.html", i=item, error=has_error)
        else:
            item.name = name
            item.price = price
            item.description = description
            item.category_id = category_id
            session.add(item)
            session.commit()
            return redirect(url_for('show_item', category_id=category_id,
                            item_id=item_id))
    else:
        return render_template("edit.html", i=item)


@app.route('/<int:category_id>/<int:item_id>/delete/')
def delete_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if item.category_id != category_id:
        return abort(404)
    return render_template("delete.html", i=item)


# JSON routes
@app.route('/catalog/json/')
def catalog_json():
    return "presents the entire catalog in json format"


@app.route('/<int:category_id>/json/')
def category_json():
    return "presents an entire category in json format"


@app.route('/<int:category_id>/<int:item_id>/json/')
def item_json():
    return "presents an item in json format"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)