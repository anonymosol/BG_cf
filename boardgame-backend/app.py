from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes.salary import salary_bp
from utils.db import init_db, close_db
from routes.employees import employee_bp
from routes.shifts import shift_bp
from routes.booking import booking_bp
from routes.salary import salary_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Đảm bảo thư mục instance tồn tại để lưu database
os.makedirs("instance", exist_ok=True)

# Cấu hình app
app.config['DATABASE'] = os.path.join("instance", "database.db")
app.config['SECRET_KEY'] = 'your-secret-key'  # Thay bằng key bảo mật riêng
app.register_blueprint(shift_bp, url_prefix='/api')
app.register_blueprint(booking_bp)
# Đăng ký blueprint cho module lương
app.register_blueprint(salary_bp, url_prefix='/api/salary')
app.register_blueprint(employee_bp, url_prefix='/api/employees')

# Khởi tạo database khi app chạy trong app context
with app.app_context():
    init_db()

# Đóng kết nối database khi app context kết thúc
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Route phục vụ file download từ thư mục 'outputs'
@app.route('/api/outputs/<path:filename>')
def download_file(filename):
    # Đảm bảo folder 'outputs' tồn tại, tránh lỗi
    outputs_dir = os.path.abspath('outputs')
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    return send_from_directory(outputs_dir, filename, as_attachment=True)

if __name__ == '__main__':
    # Chạy debug mode khi phát triển
    app.run(debug=True)
