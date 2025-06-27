from flask import Blueprint, request, jsonify
from utils.db import (
    get_all_employees,
    add_employee,
    delete_employee,
    update_employee,
    get_employee_by_name,
    get_employee_by_id,
)

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['OPTIONS'])
def options_employees():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response, 204

@employee_bp.route('/', methods=['GET'])
def get_employees():
    try:
        employees = get_all_employees()
        return jsonify(employees), 200
    except Exception as e:
        print(f"[ERROR] Get Employees: {e}")
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        print(f"[CREATE EMPLOYEE] Data received: {data}")
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        position = data.get('position')
        salary = data.get('salary', 0.0)
        role = data.get('role', 'staff')

        if not name:
            return jsonify({"error": "Name required"}), 400

        employee_id = add_employee(name, email, phone, position, salary, role)
        print(f"[CREATE EMPLOYEE] Added employee with ID {employee_id}")
        return jsonify({"message": "Employee added", "id": employee_id}), 201

    except Exception as e:
        print(f"[ERROR] Create Employee: {e}")
        return jsonify({"error": str(e)}), 500

@employee_bp.route('/<int:id>', methods=['PUT'])
def edit_employee(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No update data provided"}), 400

        existing = get_employee_by_id(id)
        if not existing:
            return jsonify({"error": "Employee not found"}), 404

        update_employee(id, data)
        return jsonify({"message": "Updated successfully"}), 200

    except Exception as e:
        print(f"[ERROR] Update Employee: {e}")
        return jsonify({"error": str(e)}), 500

@employee_bp.route('/<int:id>', methods=['DELETE'])
def remove_employee(id):
    try:
        existing = get_employee_by_id(id)
        if not existing:
            return jsonify({"error": "Employee not found"}), 404

        delete_employee(id)
        return jsonify({"message": "Deleted successfully"}), 200

    except Exception as e:
        print(f"[ERROR] Delete Employee: {e}")
        return jsonify({"error": str(e)}), 500
