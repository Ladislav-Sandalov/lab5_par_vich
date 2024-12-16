from flask import Blueprint, jsonify

warehouse_bp = Blueprint('warehouse', __name__)

warehouse_data = {
    "name": "Main Warehouse",
    "ingredients": [
        {"ingredient_id": 1, "name": "Tomatoes", "amount": 100},
        {"ingredient_id": 2, "name": "Cheese", "amount": 50},
        {"ingredient_id": 3, "name": "Dough", "amount": 200},
    ]
}

@warehouse_bp.route("/", methods=["GET"])
def get_warehouse():
    return jsonify(warehouse_data)