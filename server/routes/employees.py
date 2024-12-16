from flask import Blueprint, jsonify, request

# Blueprint для сотрудников
employees_bp = Blueprint('employees', __name__)

# Пример данных о сотрудниках
employees = {
    "cooks": [
        {"id": 1, "name": "Chef A", "busy": False},
        {"id": 2, "name": "Chef B", "busy": False}
    ],
    "waiters": [
        {"id": 1, "name": "Waiter A", "busy": False},
        {"id": 2, "name": "Waiter B", "busy": False}
    ]
}

# Получить информацию о сотрудниках
@employees_bp.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# Обновить статус сотрудника (например, "занят/свободен")
@employees_bp.route('/employees/<role>/<int:employee_id>', methods=['PUT'])
def update_employee_status(role, employee_id):
    if role in employees:
        for employee in employees[role]:
            if employee['id'] == employee_id:
                employee['busy'] = request.json.get('busy', employee['busy'])
                return jsonify({"message": "Employee status updated.", "employee": employee})
    return jsonify({"error": "Employee not found."}), 404