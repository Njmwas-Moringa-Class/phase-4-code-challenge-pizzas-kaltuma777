#!/usr/bin/env python3

from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

with app.app_context():

    print("Deleting data...")
    db.drop_all()
    db.create_all()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    db.session.add_all([shack, bistro, palace])

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    db.session.add_all([cheese, pepperoni, california])

    print("Creating RestaurantPizza...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=1)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=5)
    db.session.add_all([pr1, pr2, pr3])

    db.session.commit()

    print("Seeding done!")