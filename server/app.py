from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants_list = []

    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name,
        }
        restaurants_list.append(restaurant_dict)

    response = make_response(jsonify(restaurants_list), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant is None:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    if request.method == 'GET':
        restaurant_dict = restaurant.to_dict()
        response = make_response(jsonify(restaurant_dict), 200)
        return response

    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Restaurant deleted",
        }

        response = make_response(jsonify(response_body), 204)
        return response

@app.route('/pizzas')
def pizzas():
    pizzas_list = []

    for pizza in Pizza.query.all():
        pizza_dict = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name,
        }
        pizzas_list.append(pizza_dict)

    response = make_response(jsonify(pizzas_list), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizza():
    if request.method == 'POST':
        try:
            new_restaurantpizza = RestaurantPizza(
                price=request.get_json().get("price"),
                pizza_id=request.get_json().get("pizza_id"),
                restaurant_id=request.get_json().get("restaurant_id"),
            )

            db.session.add(new_restaurantpizza)
            db.session.commit()

            restaurantpizza_dict = new_restaurantpizza.to_dict()

            response = make_response(jsonify(restaurantpizza_dict), 201)
            return response

        except ValueError as exception_message:
            return jsonify(errors=[str(exception_message)]), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
