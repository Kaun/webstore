import csv

from flask import Flask

from webstore.config import Config, current_path
from webstore.models import db, User, Meal, Category, Order, meal_order_association


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    with open(current_path + '\categories.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        data_categories = [row for row in reader]

    with open(current_path + '\meals.csv', encoding='utf-8') as ff:
        reader = csv.reader(ff)
        data_meals = [row for row in reader]
    db_check_categories = db.session.query(Category).get(1)
    db_check_meals = db.session.query(Meal).get(1)
    if db_check_categories is None:
        for row in data_categories[1:]:
            id, title = row
            category = Category(id=int(id), title=title)
            db.session.add(category)
    if db_check_meals is None:
        for row in data_meals[1:]:
            id, title, price, description, picture, category_id = row
            meal = Meal(title=title, price=price, description=description,
                        picture=picture, category_id=category_id)
            db.session.add(meal)
    db.session.commit()


from webstore.views import *

if __name__ == '__main__':
    app.run()
