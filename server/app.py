from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.database import db
from server.config import DATABASE_URL
from server.seed import seed

# Import models to ensure they're registered
from server.models import  Restaurant, RestaurantPizza, Pizza

# Import blueprints from controllers
from server.controllers.pizza_controller import pizza_bp
from server.controllers.restaurant_controller import restaurant_bp
from server.controllers.restaurant_pizza_controller import restaurant_pizza_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints for routes
app.register_blueprint(pizza_bp)
app.register_blueprint(restaurant_bp)
app.register_blueprint(restaurant_pizza_bp)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Pizza API!"
    })

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    result = []
    for r in restaurants:
        result.append({
            "id": r.id,
            "name": r.name,
            "address": r.address
        })
    return jsonify(result)

# Get a restaurant by id, including its pizzas
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    # get related pizzas
    restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
    pizzas = []
    for rp in restaurant_pizzas:
        pizza_obj = Pizza.query.get(rp.pizza_id)
        pizzas.append({
            "id": pizza_obj.id,
            "name": pizza_obj.name,
            "ingredients": pizza_obj.ingredients,
            "price": rp.price
        })
    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": pizzas
    })

# Delete a restaurant and related RestaurantPizzas
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Delete associated RestaurantPizzas
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

# Get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    result = []
    for p in pizzas:
        result.append({
            "id": p.id,
            "name": p.name,
            "ingredients": p.ingredients
        })
    return jsonify(result)

# Create a new RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    errors = []

    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Validate inputs...
    # (Omitted for brevity; your existing validation code)

    new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(new_rp)
    db.session.commit()

    # Return the created relation
    pizza_obj = Pizza.query.get(pizza_id)
    restaurant_obj = Restaurant.query.get(restaurant_id)

    return jsonify({
        "id": new_rp.id,
        "price": new_rp.price,
        "pizza": {
            "id": pizza_obj.id,
            "name": pizza_obj.name,
            "ingredients": pizza_obj.ingredients
        },
        "restaurant": {
            "id": restaurant_obj.id,
            "name": restaurant_obj.name,
            "address": restaurant_obj.address
        }
    }), 201

@app.route('/seed', methods=['GET'])
def run_seed():
    seed()  # Call the seed function to populate the database
    return jsonify({"message": "Database seeded successfully!"})


if __name__ == '__main__':
    seed()
    app.run(debug=True, port=5002)
