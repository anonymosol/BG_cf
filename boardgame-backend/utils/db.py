import sqlite3
from flask import g, current_app
import os
import random
def generate_random_employee_id():
    return random.randint(100, 9999)
# Lùi lên 1 cấp từ thư mục chứa file hiện tại để tìm schema.sql
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
schema_path = os.path.join(base_dir, 'schema.sql')

def get_db():
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE', 'instance/database.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # Trả kết quả dạng dict
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    db = get_db()
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            db.executescript(sql)
        db.commit()
        print("[INIT DB] ✅ Database initialized successfully.")
    except Exception as e:
        print("[INIT DB ERROR] ❌", str(e))

# ==========================
# 📦 Employee CRUD operations
# ==========================

def add_employee(name, position, salary, role):
    db = get_db()

    # Tạo ID ngẫu nhiên và đảm bảo không trùng
    for _ in range(10):  # thử tối đa 10 lần
        employee_id = random.randint(100, 9999)
        exists = db.execute("SELECT id FROM employees WHERE id = ?", (employee_id,)).fetchone()
        if not exists:
            break
    else:
        raise Exception("Could not generate unique employee ID")

    db.execute(
        "INSERT INTO employees (id, name, position, salary, role) VALUES (?, ?, ?, ?, ?)",
        (employee_id, name, position, salary, role)
    )
    db.commit()
    return employee_id
def get_all_employees():
    db = get_db()
    result = db.execute("SELECT * FROM employees").fetchall()
    return [dict(row) for row in result]

def get_employee_by_id(emp_id):
    db = get_db()
    row = db.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    return dict(row) if row else None

def update_employee(emp_id, updated_data):
    db = get_db()
    fields = []
    values = []
    for key, value in updated_data.items():
        fields.append(f"{key} = ?")
        values.append(value)
    values.append(emp_id)
    db.execute(f"UPDATE employees SET {', '.join(fields)} WHERE id = ?", values)
    db.commit()

def delete_employee(emp_id):
    db = get_db()
    db.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    db.commit()

def get_employee_id(name):
    db = get_db()
    row = db.execute("SELECT id FROM employees WHERE name = ?", (name,)).fetchone()
    return row['id'] if row else None
def get_employee_by_name(name):
    db = get_db()
    row = db.execute("SELECT * FROM employees WHERE name = ?", (name,)).fetchone()
    return dict(row) if row else None


# ==========================
# 💰 Salary Reporting
# ==========================

def save_salary_report(data):
    db = get_db()
    for item in data:
        db.execute(
            "INSERT INTO salary_reports (employee_id, total_salary, report_date) VALUES (?, ?, ?)",
            (item["employee_id"], item["total_salary"], item["report_date"])
        )
    db.commit()
