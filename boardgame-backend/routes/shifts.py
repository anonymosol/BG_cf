from flask import Blueprint, request, jsonify
from utils.db import get_db

shift_bp = Blueprint('shift', __name__)

@shift_bp.route('/shifts', methods=['GET'])
def get_shifts():
    db = get_db()
    rows = db.execute("SELECT * FROM shifts").fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "employee_id": row["employee_id"],
            "shift_date": row["shift_date"],
            "shift_type": row["shift_type"],
            "note": row["note"]
        })
    return jsonify(result)



@shift_bp.route('/shifts/assign', methods=['POST'])
def assign_shift():
    data = request.get_json()
    date = data.get('shift_date')
    shift = data.get('shift_type')
    emp_id = data.get('employee_id')

    if not date or not shift or not emp_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        emp_id = int(emp_id)
    except ValueError:
        return jsonify({'error': 'employee_id must be an integer'}), 400

    db = get_db()

    emp_check = db.execute("SELECT id FROM employees WHERE id = ?", (emp_id,)).fetchone()
    if not emp_check:
        return jsonify({'error': f'Employee with ID {emp_id} does not exist'}), 404

    # Xóa ca cũ
    db.execute("DELETE FROM shift_schedules WHERE date = ? AND shift = ?", (date, shift))

    # Gán ca mới
    db.execute(
        "INSERT INTO shift_schedules (date, shift, employee_id) VALUES (?, ?, ?)",
        (date, shift, emp_id)
    )

    db.commit()
    return jsonify({'message': 'Shift assigned successfully'}), 201

@shift_bp.route('/shifts', methods=['POST'])
def add_shift():
    data = request.get_json()
    employee_id = data.get('employee_id')
    shift_date = data.get('shift_date')
    shift_type = data.get('shift_type')
    note = data.get('note', '')

    if not employee_id or not shift_date or not shift_type:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO shifts (employee_id, shift_date, shift_type, note) VALUES (?, ?, ?, ?)",
        (employee_id, shift_date, shift_type, note)
    )
    db.commit()
    return jsonify({"message": "Shift added successfully"}), 201

@shift_bp.route('/shifts/<int:shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    db = get_db()
    db.execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    db.commit()
    return jsonify({"message": "Shift deleted successfully"}), 200
