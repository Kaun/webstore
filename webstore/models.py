from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# m2m
meal_order_association = db.Table('meal_order',
                                  db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
                                  db.Column('orders_id', db.Integer, db.ForeignKey('orders.id')))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    # address = db.Column(db.String)
    # phone = db.Column(db.String)
    orders = db.relationship('Order', back_populates="user")


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="meals")
    orders = db.relationship('Order', secondary=meal_order_association, back_populates="meals")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', back_populates="category")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', secondary=meal_order_association, back_populates="orders")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")


