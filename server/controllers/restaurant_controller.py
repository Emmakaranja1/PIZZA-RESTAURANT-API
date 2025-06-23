from flask import Blueprint, request
from server.models.restaurant import Restaurant
from server.database import db

restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/restaurants')

@restaurant_bp.route('/', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [restaurant.to_dict() for restaurant in restaurants], 200

@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant_with_pizzas(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {'error': 'Restaurant not found'}, 404
    pizzas = []
    for rp in restaurant.restaurant_pizzas:
        p = rp.pizza.to_dict()
        p['price'] = rp.price
        pizzas.append(p)
    data = restaurant.to_dict()
    data['pizzas'] = pizzas
    return data, 200

@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {'error': 'Restaurant not found'}, 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204


