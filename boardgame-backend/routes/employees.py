from flask import Blueprint, request, jsonify
from utils.db import get_all_employees, add_employee, delete_employee, update_employee, get_employee_by_name, get_employee_by_id


employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/', methods=['OPTIONS'])
def options_employees():
    return '', 204

@employee_bp.route('/', methods=['GET'])
def get_employees():
    try:
        employees = get_all_employees()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@employee_bp.route('', methods=['POST'])
def create_employee():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name required"}), 400

    position = data.get('position')
    salary = data.get('salary', 0.0)
    role = data.get('role', 'staff')

    try:
        employee_id = add_employee(name, position, salary, role)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Employee added", "id": employee_id}), 201


@employee_bp.route('/<int:id>', methods=['PUT'])
def edit_employee(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    existing = get_employee_by_id(id)
    if not existing:
        return jsonify({"error": "Employee not found"}), 404

    update_employee(id, data)
    return jsonify({"message": "Updated successfully"})

@employee_bp.route('/<int:id>', methods=['DELETE'])
def remove_employee(id):
    existing = get_employee_by_id(id)
    if not existing:
        return jsonify({"error": "Employee not found"}), 404

    delete_employee(id)
    return jsonify({"message": "Deleted successfully"})
