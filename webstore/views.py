from hashlib import md5

from flask import render_template, request, session, redirect
from datetime import datetime, date, time
from sqlalchemy.sql.expression import func

from webstore import app, db
from webstore.models import db, User, Meal, Category, Order
from webstore.forms import OrderForm, RegisterForm, LoginForm


@app.route('/')
def route_main():
    categories = db.session.query(Category).all()
    category_and_meals = {}
    for category in categories:
        meals_query = db.session.query(Meal).filter(Meal.category_id == category.id).order_by(func.random()).limit(3)
        category_and_meals[category.id] = meals_query
    return render_template('main.html', meals=category_and_meals, categories=categories, count=session.get("count", 0),
                           cost=session.get("cost", 0))


@app.route('/cart/', methods=["GET", "POST"])
def route_cart():
    form = OrderForm(email=session.get("user_email", ''))
    meals = []
    cost = 0
    for meal_id in session.get('cart', []):
        meal_db = db.session.query(Meal).get_or_404(meal_id)
        meals.append(meal_db)
    for meal in meals:
        cost += int(meal.price)
    count = len(meals)
    session['count'] = count
    session['cost'] = cost
    if request.method == "POST" and form.validate():
        name = form.name.data
        adress = form.address.data
        email = form.email.data
        phone = form.phone.data
        order = Order(data=datetime.now(), sum=cost, status=True, name=name, address=adress, email=email, phone=phone,
                      user_id=session.get("user_id", None))
        for meal in meals:
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()

        return redirect('/ordered/')
    else:
        if session.get('remove'):
            session.pop('remove')
            remove = True
        else:
            remove = False
        return render_template('cart.html', meals=meals, count=session.get("count", 0),
                               cost=session.get("cost", 0), form=form, remove=remove)


@app.route('/category/<id>/')
def route_category(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    meals_query = db.session.query(Meal).filter(Meal.category_id == category.id).order_by(func.random()).all()
    return render_template('category.html', category=category.title, meals=meals_query, count=session.get("count", 0),
                           cost=session.get("cost", 0))


@app.route('/account/')
def route_account():
    if session.get("user_id") is not None:
        orders_user = db.session.query(Order).filter(Order.user_id == session.get("user_id")).\
                      order_by(Order.id.desc()).all()
        return render_template('account.html', orders=orders_user, count=session.get("count", 0), cost=session.get("cost", 0))
    else:
        return redirect('/')


@app.route('/login/', methods=["GET", "POST"])
def route_login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        email = form.email.data
        pswd = form.pswd.data
        hash_password = md5(pswd.encode())
        password = hash_password.hexdigest()
        user_db = db.session.query(User).filter(User.email == email).first()
        if user_db is not None and user_db.password == password:
            session["user_id"] = user_db.id
            session["user_email"] = user_db.email
            session["is_auth"] = True
            return redirect('/')
        else:
            form.email.errors.append("Неверный пользователь или пароль")
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/register/', methods=["GET", "POST"])
def route_register():
    error_msg = ''
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        email = form.email.data
        pswd = form.pswd.data
        hash_password = md5(pswd.encode())
        password = hash_password.hexdigest()
        user_db = db.session.query(User).filter_by(email=email).first()
        if len(pswd) > 5 and user_db is None:
            user = User(email=email, password=password)

            db.session.add(user)
            db.session.commit()
            return redirect('/login/')
        else:
            if user_db:
                form.pswd.errors.append("Пользователь уже существует")
            else:
                form.pswd.errors.append("Пароль должен быть больше 5 символов")
            return render_template('register.html', form=form, error_msg=error_msg)

    else:
        return render_template('register.html', form=form)


@app.route('/logout/')
def route_logout():
    session.pop("user_id")
    session.pop("user_email")
    session.pop("is_auth")
    session.pop("cart", [])
    session.pop('count', 0)
    session.pop('cost', 0)
    return redirect('/')


@app.route('/ordered/')
def route_ordered():
    session.pop("cart", [])
    session.pop('count', 0)
    session.pop('cost', 0)
    return render_template('ordered.html')


@app.route('/addtocart/<id>')
@app.route('/remove/<id>')
def route_add_remove_meal(id):
    cart = session.get('cart', [])
    if request.path.split('/')[-2] == "addtocart":
        cart.append(id)
    elif request.path.split('/')[-2] == "remove":
        cart.remove(id)
        session['remove'] = True
    session['cart'] = cart
    return redirect('/cart/')

