from flask import Blueprint, request
from server.models.pizza import Pizza
from server.database import db

pizza_bp = Blueprint('pizza_bp', __name__, url_prefix='/pizzas')

@pizza_bp.route('/', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in pizzas], 200

@pizza_bp.route('/', methods=['POST'])
def create_pizza():
    data = request.get_json()
    name = data.get('name')
    ingredients = data.get('ingredients')
    if not name or not ingredients:
        return {'error': 'Name and ingredients are required'}, 400
    pizza = Pizza(name=name, ingredients=ingredients)
    db.session.add(pizza)
    db.session.commit()
    return pizza.to_dict(), 201