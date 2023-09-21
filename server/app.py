#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return jsonify({'error': 'Bakery not found'}), 404

    bakery_serialized = bakery.to_dict()

    response = make_response(
        jsonify(bakery_serialized),
        200
    )
    return response



@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    try:
        # Get data from the form
        name = request.form.get('name')
        price = request.form.get('price')
        bakery_id = request.form.get('bakery_id')  # Assuming you also send the bakery_id in the form

        # Create a new baked good
        baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)

        # Add it to the database
        db.session.add(baked_good)
        db.session.commit()

        # Return the newly created baked good as JSON
        return jsonify(baked_good.to_dict()), 201  # 201 indicates a resource was successfully created

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return an error message with a 500 status code for any issues

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    try:
        # Get the bakery to update
        bakery = Bakery.query.get(id)

        if not bakery:
            return jsonify({'error': 'Bakery not found'}), 404

        # Update the bakery name if provided in the form
        new_name = request.form.get('name')
        if new_name:
            bakery.name = new_name

        # Commit the changes to the database
        db.session.commit()

        # Return the updated bakery as JSON
        return jsonify(bakery.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    try:
        # Get the baked good to delete
        baked_good = BakedGood.query.get(id)

        if not baked_good:
            return jsonify({'error': 'Baked Good not found'}), 404

        # Delete the baked good from the database
        db.session.delete(baked_good)
        db.session.commit()

        # Return a confirmation message
        return jsonify({'message': 'Baked Good deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
