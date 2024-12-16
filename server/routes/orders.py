from flask import Blueprint, request, jsonify
from server.services.chef_service import order_queue, lock
from server.datas.halls import halls

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    recipe_name = data.get("recipe_name")
    quantity = data.get("quantity")
    table_id = data.get("table_id")
    hall_id = data.get("hall_id")

    if not recipe_name or not quantity or not table_id or not hall_id:
        return jsonify({"error": "Invalid data"}), 400

    table_found = False
    for hall in halls:
        if hall["id"] == hall_id:
            for table in hall["tables"]:
                if table["id"] == table_id:
                    if table["status"] != "reserved":
                        return jsonify({"error": "Table is not reserved"}), 400
                    table_found = True
                    break

    if not table_found:
        return jsonify({"error": "Table not found"}), 404

    order = {"recipe_name": recipe_name, "quantity": quantity, "table_id": table_id}
    with lock:
        order_queue.append(order)

    return jsonify({"status": "Order added", "order": order}), 201