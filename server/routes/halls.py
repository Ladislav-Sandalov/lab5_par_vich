from flask import Blueprint, jsonify, request
from server.datas.halls import halls


halls_bp = Blueprint('halls', __name__)

halls_data = {
    1: {"name": "VIP Hall", "tables": {1: "free", 2: "reserved", 3: "free", 4: "free", 5: "reserved"}},
    2: {"name": "Standard Hall", "tables": {1: "free", 2: "reserved", 3: "free", 4: "free", 5: "free",
                                            6: "free", 7: "reserved", 8: "free", 9: "free", 10: "free"}},
}

@halls_bp.route("/halls", methods=["GET"])
def get_halls():
    return jsonify([{"id": hall_id, "name": hall["name"], "tables": hall["tables"]} for hall_id, hall in halls_data.items()])

@halls_bp.route("/<int:hall_id>/tables/<int:table_id>/reserve", methods=["POST"])
def reserve_table(hall_id, table_id):
    hall = halls_data.get(hall_id)
    if not hall:
        return jsonify({"error": "Hall not found"}), 404
    if table_id not in hall["tables"]:
        return jsonify({"error": "Table not found"}), 404
    if hall["tables"][table_id] == "reserved":
        return jsonify({"error": "Table already reserved"}), 400

    hall["tables"][table_id] = "reserved"
    return jsonify({"status": "Table reserved successfully"}), 200

@halls_bp.route("/<int:hall_id>/tables/<int:table_id>/free", methods=["POST"])
def free_table(hall_id, table_id):
    hall = halls_data.get(hall_id)
    if not hall:
        return jsonify({"error": "Hall not found"}), 404
    if table_id not in hall["tables"]:
        return jsonify({"error": "Table not found"}), 404

    hall["tables"][table_id] = "free"
    return jsonify({"status": "Table freed successfully"}), 200