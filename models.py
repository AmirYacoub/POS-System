from datetime import datetime

from google.cloud import firestore
import random
import string

db = firestore.Client()


def update_inventory_item_quantity(item_id, quantity_sold):
    """Update the quantity of an inventory item after a sale."""
    doc_ref = db.collection('inventory').document(item_id)
    item = doc_ref.get()
    if item.exists:
        new_quantity = item.to_dict().get('quantity', 0) - quantity_sold
        if new_quantity < 0:
            raise ValueError("Not enough stock available")
        doc_ref.update({'quantity': new_quantity})
    else:
        raise ValueError(f"Item with ID {item_id} does not exist")


def add_sale(items):
    """Add a new sale record to Firestore and update inventory quantities."""
    total_price = 0
    sale_items = []

    for item in items:
        item_id = item['item_id']
        quantity_sold = item['quantity']

        # Get the item details from inventory
        item_ref = db.collection('inventory').document(item_id)
        item_data = item_ref.get().to_dict()

        if not item_data or item_data['quantity'] < quantity_sold:
            raise ValueError(f"Insufficient stock for item ID {item_id}")

        # Update inventory quantity
        update_inventory_item_quantity(item_id, quantity_sold)

        # Calculate total price and prepare sale item data
        sale_items.append({
            'item_id': item_id,
            'quantity': quantity_sold,
            'price_at_sale': item_data['price']
        })
        total_price += item_data['price'] * quantity_sold

    # Add sale record to Firestore
    sale_data = {
        'items': sale_items,
        'total_price': total_price,
        'sale_date': datetime.now()
    }
    sale_ref = db.collection('sales').document()
    sale_ref.set(sale_data)

    return sale_ref.id


def generate_unique_barcode():
    """Generate a random 10-digit barcode."""
    return ''.join(random.choices(string.digits, k=10))


def check_barcode_exists(barcode):
    """Check if the barcode already exists in the inventory."""
    docs = db.collection('inventory').where(field_path='barcode', op_string='==', value=barcode).stream()
    return any(docs)  # Returns True if any documents exist with the same barcode


def add_inventory_item(data):
    """Add a new item to the inventory, ensuring the barcode is unique."""
    barcode = data.get('barcode', generate_unique_barcode())

    # Check for duplicate barcode and generate a new one if necessary
    while check_barcode_exists(barcode):
        barcode = generate_unique_barcode()

    data['barcode'] = barcode

    # Add the item to Firestore
    doc_ref = db.collection('inventory').document()
    doc_ref.set(data)
    return doc_ref.id


def get_inventory_item(item_id):
    """Retrieve an item from the inventory by its document ID."""
    doc_ref = db.collection('inventory').document(item_id)
    return doc_ref.get().to_dict()


def update_inventory_item(item_id, data):
    """Update an existing inventory item."""
    doc_ref = db.collection('inventory').document(item_id)
    doc_ref.update(data)
    return True


def delete_inventory_item(item_id):
    """Delete an item from the inventory."""
    doc_ref = db.collection('inventory').document(item_id)
    doc_ref.delete()
    return True
