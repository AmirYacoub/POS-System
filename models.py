from google.cloud import firestore

db = firestore.Client()


def add_inventory_item(data):
    """Add a new item to the inventory."""
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
