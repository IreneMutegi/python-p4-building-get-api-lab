from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Bakery, BakedGood  # Import the models

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # For pretty JSON output

# Initialize Migrate and SQLAlchemy
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    """Return all bakeries in JSON format."""
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    """Return a bakery by its ID in JSON format."""
    bakery = db.session.get(Bakery, id)  # Use session.get() instead of query.get()
    if bakery:
        return jsonify(bakery.to_dict())  # Convert the bakery to a dictionary and return it
    else:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    """Return all baked goods sorted by price in descending order."""
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()  # Sort by price in descending order
    return jsonify([baked_good.to_dict() for baked_good in baked_goods])  # Return the list of baked goods as JSON

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    """Return the most expensive baked good."""
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify(most_expensive.to_dict())
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
