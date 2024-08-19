from google.cloud import firestore
import random
import string

db = firestore.Client()


def generate_unique_barcode():
    """Generate a random 10-digit barcode."""
    return ''.join(random.choices(string.digits, k=10))


def check_barcode_exists(barcode):
    """Check if the barcode already exists in the inventory."""
    docs = db.collection('inventory').where('barcode', '==', barcode).stream()
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
