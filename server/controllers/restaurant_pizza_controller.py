from flask import Blueprint, request
from server.models.restaurant_pizza import RestaurantPizza
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.database import db

restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__, url_prefix='/restaurant_pizzas')

@restaurant_pizza_bp.route('/', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    restaurant_id = data.get('restaurant_id')
    pizza_id = data.get('pizza_id')
    errors = []

    # Validation
    if price is None or not (1 <= price <= 30):
        errors.append("Price must be between 1 and 30")
    if not Restaurant.query.get(restaurant_id):
        errors.append("Invalid restaurant_id")
    if not Pizza.query.get(pizza_id):
        errors.append("Invalid pizza_id")
    if errors:
        return {"errors": errors}, 400

    rp = RestaurantPizza(price=price, restaurant_id=restaurant_id, pizza_id=pizza_id)
    db.session.add(rp)
    db.session.commit()

    response = rp.to_dict()
    response["pizza"] = rp.pizza.to_dict()
    response["restaurant"] = rp.restaurant.to_dict()

    return response, 201
