from server.database import db
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza

def seed():
    db.drop_all()
    db.create_all()

    r1 = Restaurant(name='Pizza Palace', address='123 Main St')
    r2 = Restaurant(name='Pizzeria Roma', address='456 Elm St')
    p1 = Pizza(name='Margherita', ingredients='Tomato, Mozzarella, Basil')
    p2 = Pizza(name='Pepperoni', ingredients='Pepperoni, Cheese')
    p3 = Pizza(name='Veggie', ingredients='Bell Peppers, Olives, Onions, Tomato')

    db.session.add_all([r1, r2, p1, p2, p3])
    db.session.commit()

    rp1 = RestaurantPizza(price=10, restaurant_id=r1.id, pizza_id=p1.id)
    rp2 = RestaurantPizza(price=12, restaurant_id=r1.id, pizza_id=p2.id)
    rp3 = RestaurantPizza(price=11, restaurant_id=r2.id, pizza_id=p3.id)

    db.session.add_all([rp1, rp2, rp3])
    db.session.commit()