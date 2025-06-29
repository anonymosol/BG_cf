from flask import Blueprint, jsonify
from utils.db import get_db

salary_bp = Blueprint('salary', __name__)

@salary_bp.route('/report', methods=['GET'])
def get_salary_report():
    """
    Lấy danh sách báo cáo lương, kèm tên nhân viên, tổng lương, ngày báo cáo.
    Trả về JSON để frontend React hiển thị.
    """
    db = get_db()
    query = '''
        SELECT sr.id, e.name, sr.total_salary, sr.report_date
        FROM salary_reports sr
        JOIN employees e ON sr.employee_id = e.id
        ORDER BY sr.report_date DESC
    '''
    reports = db.execute(query).fetchall()
    return jsonify([dict(r) for r in reports])
