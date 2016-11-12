from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_schema import Base, User, Category, Item

from random import randint
import datetime
import random

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# First delete all existing data
session.query(User).delete()
session.query(Category).delete()
session.query(Item).delete()
session.commit()

# Add new sample users
User1 = User(name="Nicholas Savini", email="nicholasmsavini@gmail.com", image="blank")
session.add(User1)

User2 = User(name="Luke Skywalker", email="tatooinefarmboy@gmail.com", image="http://vignette3.wikia.nocookie.net/starwars/images/6/62/LukeGreenSaber-MOROTJ.png/revision/latest?cb=20150426200707")
session.add(User2)

# Add new sample categories
Category1 = Category(category="Keyboards")
session.add(Category1)
Category2 = Category(category="Keysets")
session.add(Category2)
Category3 = Category(category="Switches")
session.add(Category3)
Category4 = Category(category="Accessories")
session.add(Category4)


# Create a few sample items
Item1 = Item(name="Whitefox", category_id=1, price=179.99, description="The WhiteFox is a collaboration project between Matteo Spinelli (matt3o), Massdrop, and Input Club. The design of the WhiteFox was meticulously prepared and took almost an entire year to come to life. The WhiteFox is a 65% mechanical keyboard with an aluminum case and plate, Cherry profile PBT dye-sublimated keycaps, a huge variety of keyswitch options including Cherry MX, Gateron, and Zealios, and a fully programmable PCB",
             image="https://input.club/wp-content/uploads/2015/12/MD-13679_20151209152005_1e1b1cae1b0ffe53-1.jpg",
             created_by=1)
session.add(Item1)
Item2 = Item(name="HHKB 2", category_id=1, price=249.99, description="The Happy Hacking Professional 2 (HHKB2) is a minimalist's dream come true; packing more features than a full size keyboard into a very small package. The HHKB2 still provides full-size keycaps, and uses Topre's unique capacitive tactile key switches for comfort and high reliability. PC and Mac friendly, the HHKB2 maintains its wide functionality by replacing lesser used keys with key combinations, which once you get the hang of it, you may never want to use a full size keyboard again; the HHKB2 even provides audio controls (Mac only) and a built-in 2-port USB 2.0 hub!",
             image="https://elitekeyboards.com/products.php?sub=pfu_keyboards,hhkbpro2&pid=pdkb400b#",
             created_by=2)
session.add(Item2)
Item3 = Item(name="SA Grand Budapest", category_id=2, price=185.99, description="Designed by Madeo, the SA Grand Budapest set was made out of love for Grand Budapest the Movie. The set uses pink, purple, and red to create a very classical and modern color combination.",
             image="https://www.keyclack.com/wp-content/uploads/2016/10/SA-F4-TKL-2.jpg",
             created_by=1)
session.add(Item3)
Item4 = Item(name="Sky Dolch", category_id=2, price=135, description="A classic style with a modern take, this keyset was inspired with a combination of Dolch and SoWaRe (Sky Blue Wyse Replica). The dark and medium grey looking colors are embodied with a vibrant cyan font. The word Sky refers to the legend as being a vibrant blue with the word Dolch referring to the body of colors.",
             image="https://cdn.shopify.com/s/files/1/0267/1905/products/skydolch1_1024x1024.jpg?v=1478746274",
             created_by=1)
session.add(Item4)
Item5 = Item(name="Gateron Blues (70 Pack)", category_id=3, price=20, description="Gateron switches are one of the most sought after products in the mechanical keyboard community. Gateron switches provide a clear transparent housing with 50 million cycles. The inside is finished with copper click leaf and soft plastic stem to provide a smooth typing experience. These switches are made with the same stem as Cherry so all our keycaps are compatible with this DIY product.",
             image="https://cdn.shopify.com/s/files/1/0267/1905/products/gateron-blue_811fc0e9-2886-44a8-b6be-eed910d18030_1024x1024.jpg?v=1476249067",
             created_by=2)
session.add(Item5)
Item6 = Item(name="Zealio (70 Pack)", category_id=3, price=59.99, description="65g Zealios - Smooth, long, drawn out tactile bump in the middle. Nice cushion during bottom out.",
             image="https://cdn.shopify.com/s/files/1/0490/7329/products/zealios2.jpeg?v=1453017871",
             created_by=2)
session.add(Item6)
Item7 = Item(name="Keycap Puller", category_id=4, price=6.99, description="The perfect tool to set up your keyboard with all your new custom keys.  The wire puller design makes it simple to quickly and safely remove a cap from almost any kind of keyboard on the market.",
             image="http://cdn.shopify.com/s/files/1/0218/4886/products/KeyPuller2_1024x1024.jpg?v=1429499476",
             created_by=1)
session.add(Item7)
Item8 = Item(name="Wooden Wrist Rest", category_id=4, price=36.99, description="Material: Genuine Black Walnut Wood",
             image="http://images.bigcartel.com/product_images/175260229/20160315_132518_resized.jpg?auto=format&fit=max&h=300&w=300",
             created_by=1)
session.add(Item8)

session.commit()