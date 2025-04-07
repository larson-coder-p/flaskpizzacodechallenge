from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade="all, delete")

    def to_dict(self):
        data = {"id": self.id, "name": self.name, "address": self.address}
        data["restaurant_pizzas"] = [rp.to_dict() for rp in self.restaurant_pizzas]
        return data

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.String(200))
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', cascade="all, delete")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "ingredients": self.ingredients}

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id,
            "pizza": self.pizza.to_dict()
        }

# Routes
@app.route('/')
def home():
    return "Welcome to the Pizza API!"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([r.to_dict() for r in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict())

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([p.to_dict() for p in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({"errors": ["Missing data"]}), 400
    restaurant = Restaurant.query.get(data['restaurant_id'])
    pizza = Pizza.query.get(data['pizza_id'])
    if not restaurant or not pizza:
        return jsonify({"errors": ["Invalid restaurant_id or pizza_id"]}), 400
    try:
        price = float(data['price'])
    except:
        return jsonify({"errors": ["Price must be a number"]}), 400
    rp = RestaurantPizza(price=price, restaurant_id=restaurant.id, pizza_id=pizza.id)
    db.session.add(rp)
    db.session.commit()
    rp_data = rp.to_dict()
    rp_data["restaurant"] = {"id": restaurant.id, "name": restaurant.name, "address": restaurant.address}
    return jsonify(rp_data), 201

# Seed sample data for testing
def seed_data():
    if not Restaurant.query.first() and not Pizza.query.first():
        r1 = Restaurant(name="Karen's Pizza Shack", address="address1")
        r2 = Restaurant(name="Sanjay's Pizza", address="address2")
        r3 = Restaurant(name="Kiki's Pizza", address="address3")
        db.session.add_all([r1, r2, r3])
        p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
        db.session.add_all([p1, p2, p3])
        db.session.commit()
        rp = RestaurantPizza(price=10.0, restaurant_id=r1.id, pizza_id=p1.id)
        db.session.add(rp)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)

