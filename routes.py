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
