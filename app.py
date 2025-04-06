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