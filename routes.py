from flask import request, jsonify
from app import app
from models import *


@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    item_id = add_inventory_item(data)
    return jsonify({"message": "Item added successfully", "item_id": item_id}), 201


@app.route('/inventory/<item_id>', methods=['GET'])
def retrieve_inventory_item(item_id):
    item = get_inventory_item(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404


@app.route('/inventory/<item_id>', methods=['PUT'])
def modify_inventory_item(item_id):
    data = request.get_json()
    success = update_inventory_item(item_id, data)
    if success:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "Failed to update item"}), 400


@app.route('/inventory/<item_id>', methods=['DELETE'])
def remove_inventory_item(item_id):
    success = delete_inventory_item(item_id)
    if success:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "Failed to delete item"}), 400


@app.route('/sales', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        sale_id = add_sale(data['items'])
        return jsonify({"message": "Sale recorded successfully", "sale_id": sale_id}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": e}), 500


@app.route('/sales', methods=['GET'])
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
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/sales/<sale_id>', methods=['GET'])
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
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/test', methods=['GET'])
def test():
    return "Test route is working!"
