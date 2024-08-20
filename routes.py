import os
from datetime import timedelta


from flask import request, jsonify
from flask.cli import load_dotenv

from app import app
from models import *
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

load_dotenv(".env")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route('/inventory', methods=['POST'])
@jwt_required()
def create_inventory_item():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    data = request.get_json()
    item_id = add_inventory_item(data)
    return jsonify({"message": "Item added successfully", "item_id": item_id}), 201


@app.route('/inventory/<item_id>', methods=['GET'])
@jwt_required()
def retrieve_inventory_item(item_id):
    item = get_inventory_item(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404


@app.route('/inventory/<item_id>', methods=['PUT'])
@jwt_required()
def modify_inventory_item(item_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    data = request.get_json()
    success = update_inventory_item(item_id, data)
    if success:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "Failed to update item"}), 400


@app.route('/inventory/<item_id>', methods=['DELETE'])
@jwt_required()
def remove_inventory_item(item_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    success = delete_inventory_item(item_id)
    if success:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "Failed to delete item"}), 400


@app.route('/inventory', methods=['GET'])
@jwt_required()
def list_inventory_items():
    try:
        items_ref = db.collection('inventory').stream()
        items = []
        for item in items_ref:
            item_data = item.to_dict()
            item_data['id'] = item.id  # Add the document ID to the item data
            items.append(item_data)
        return jsonify(items), 200
    except Exception as e:
        print(f"Error: {e}")  # Logging the error for debugging
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    try:
        data = request.get_json()
        sale_id = add_sale(data['items'])
        return jsonify({"message": "Sale recorded successfully", "sale_id": sale_id}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    try:
        sales_ref = db.collection('sales').stream()
        sales = []
        for sale in sales_ref:
            sale_data = sale.to_dict()
            sale_data['sale_id'] = sale.id
            sales.append(sale_data)
        return jsonify(sales), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/sales/<sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    try:
        sale_ref = db.collection('sales').document(sale_id)
        sale = sale_ref.get()
        if sale.exists:
            sale_data = sale.to_dict()
            sale_data['sale_id'] = sale.id
            return jsonify(sale_data), 200
        else:
            return jsonify({"message": "Sale not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        create_user(data['username'], data['password'])
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = authenticate_user(data['username'], data['password'])
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/test', methods=['GET'])
def test():
    return "Test route is working!"