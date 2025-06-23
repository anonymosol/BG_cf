from flask import Blueprint, jsonify
from utils.db import get_db

salary_bp = Blueprint('salary', __name__)

@salary_bp.route('/salary-report', methods=['GET'])
def get_salary_report():
    db = get_db()
    reports = db.execute('''
        SELECT sr.id, e.name, sr.total_salary, sr.report_date
        FROM salary_reports sr
        JOIN employees e ON sr.employee_id = e.id
        ORDER BY sr.report_date DESC
    ''').fetchall()
    return jsonify([dict(r) for r in reports])
