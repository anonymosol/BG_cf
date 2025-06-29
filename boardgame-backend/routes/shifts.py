from flask import Blueprint, jsonify, request
from utils.db import get_db

shift_bp = Blueprint('shift', __name__)

@shift_bp.route('/shifts', methods=['GET'])
def get_shifts():
    db = get_db()
    shifts = db.execute('SELECT * FROM shifts ORDER BY date DESC').fetchall()
    return jsonify([dict(row) for row in shifts])

@shift_bp.route('/shifts', methods=['POST'])
def add_shift():
    data = request.get_json()
    employee_id = data.get('employee_id')
    date = data.get('date')
    shift_type = data.get('shift_type')

    db = get_db()
    db.execute(
        'INSERT INTO shifts (employee_id, date, shift_type) VALUES (?, ?, ?)',
        (employee_id, date, shift_type)
    )
    db.commit()

    return jsonify({"message": "Shift added successfully"}), 201
