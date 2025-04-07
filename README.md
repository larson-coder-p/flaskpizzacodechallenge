# flaskpizzacodechallenge
This project is a Flask-based API for managing a Pizza Restaurant domain. The API allows you to perform CRUD operations on restaurants, pizzas, and the associations between them (RestaurantPizza). It is designed to meet the following requirements:

Models & Relationships:

A Restaurant has many Pizzas through RestaurantPizza.

A Pizza has many Restaurants through RestaurantPizza.

A RestaurantPizza belongs to both a Restaurant and a Pizza.

Cascade deletes are configured so that deleting a Restaurant also deletes its associated RestaurantPizza records.

Serialization rules are set to limit recursion.

Seed Data:

The database is seeded with sample data for testing.

Routes:

GET /restaurants: Returns all restaurants with basic fields.

GET /restaurants/<int:id>: Returns a single restaurant along with its associated pizzas.

DELETE /restaurants/<int:id>: Deletes a restaurant and its associated RestaurantPizza records.

GET /pizzas: Returns all pizzas.

POST /restaurant_pizzas: Creates a new RestaurantPizza that links an existing Restaurant and Pizza with a price. Returns errors if validation fails.

Requirements
Python 3.7+

Flask

Flask_SQLAlchemy

Installation
Clone the Repository or Copy the Code:

bash
Copy
git clone git@github.com:larson-coder-p/flaskpizzacodechallenge.git
cd flaskpizza
Create a Virtual Environment (Optional but Recommended):

bash
Copy
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install Flask Flask_SQLAlchemy
Usage
Run the Application:

In your terminal, run:

bash
Copy
python app.py
The Flask server will start on http://127.0.0.1:5000/.

Testing Endpoints:

You can use your web browser, Postman, or another API testing tool to interact with the API.

Home Route:
Visit http://127.0.0.1:5000/ to see the welcome message.

List Restaurants:
GET http://127.0.0.1:5000/restaurants

Get Restaurant Details:
GET http://127.0.0.1:5000/restaurants/1

Delete a Restaurant:
DELETE http://127.0.0.1:5000/restaurants/1

List Pizzas:
GET http://127.0.0.1:5000/pizzas

Create a RestaurantPizza:
POST http://127.0.0.1:5000/restaurant_pizzas
Request Body Example:

json
Copy
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
Endpoints Overview
GET /restaurants
Description: Returns all restaurants with their basic details.

Response Example:

json
Copy
[
  {
    "id": 1,
    "name": "Karen's Pizza Shack",
    "address": "address1"
  },
  {
    "id": 2,
    "name": "Sanjay's Pizza",
    "address": "address2"
  },
  {
    "id": 3,
    "name": "Kiki's Pizza",
    "address": "address3"
  }
]
GET /restaurants/<int:id>
Description: Returns a restaurant with its associated pizzas.

Response Example (if restaurant exists):

json
Copy
{
  "id": 1,
  "name": "Karen's Pizza Shack",
  "address": "address1",
  "restaurant_pizzas": [
    {
      "id": 1,
      "price": 10.0,
      "restaurant_id": 1,
      "pizza_id": 1,
      "pizza": {
        "id": 1,
        "name": "Emma",
        "ingredients": "Dough, Tomato Sauce, Cheese"
      }
    }
  ]
}
Error Response (if restaurant not found):

json
Copy
{
  "error": "Restaurant not found"
}
DELETE /restaurants/<int:id>
Description: Deletes a restaurant (and its associated RestaurantPizza records).

Response:
Returns an empty response with HTTP status code 204.

GET /pizzas
Description: Returns all pizzas.

Response Example:

json
Copy
[
  {
    "id": 1,
    "name": "Emma",
    "ingredients": "Dough, Tomato Sauce, Cheese"
  },
  {
    "id": 2,
    "name": "Geri",
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
  },
  {
    "id": 3,
    "name": "Melanie",
    "ingredients": "Dough, Sauce, Ricotta, Red peppers, Mustard"
  }
]

POST /restaurant_pizzas
Description: Creates a new RestaurantPizza entry.

Request Body Example:

json
Copy
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
Response Example (if successful):

json
Copy
{
  "id": 4,
  "price": 5,
  "restaurant_id": 3,
  "pizza_id": 1,
  "pizza": {
    "id": 1,
    "name": "Emma",
    "ingredients": "Dough, Tomato Sauce, Cheese"
  },
  "restaurant": {
    "id": 3,
    "name": "Kiki's Pizza",
    "address": "address3"
  }
}
Error Response (if validation error):

json
Copy
{
  "errors": ["Missing data for price, pizza_id, or restaurant_id"]
}

Testing
Use Postman or similar tools to send HTTP requests to the endpoints.



