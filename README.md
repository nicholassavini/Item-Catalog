# Udacity Item Catalog Project
This was the fifth project for the Udacity Full Stack Nanodegree. It displays all of the items in an item catalog, and allows the user to create, edit, and delete items.

## How to Run this Project Locally
This site was written in Python 2.7, using Flask as a framework, and SQL Alchemy as an ORM.
- Download the latest version of Python [here](https://www.python.org/downloads/)
- Install Flask by running `pip install Flask`
- Install Sql Alchemy by running `pip install sqlalchemy`

After all dependencies are installed, you can setup the database by running `python database_schema.py`. After the database is created, you may add sample data by running `python item_generator.py`. Now you just have to run `python main.py` to run the server, and the site will be active. You can visit it at [localhost:8000](localhost:8000).