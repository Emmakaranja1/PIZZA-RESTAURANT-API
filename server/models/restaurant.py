from server.database import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    # Relationships
    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='restaurant',
        cascade='all, delete'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
