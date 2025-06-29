from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import blueprints
from routes.salary import salary_bp
from routes.employees import employee_bp
from routes.shifts import shift_bp
from routes.booking import booking_bp

# Import DB utils
from utils.db import init_db, close_db

# Initialize Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Ensure instance folder exists for SQLite DB
os.makedirs("instance", exist_ok=True)

# App configuration
app.config['DATABASE'] = os.path.join("instance", "database.db")
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production

# Register blueprints with clear URL prefixes
app.register_blueprint(shift_bp, url_prefix='/api/shifts')
app.register_blueprint(booking_bp, url_prefix='/api/bookings')
app.register_blueprint(salary_bp, url_prefix='/api/salary')
app.register_blueprint(employee_bp, url_prefix='/api/employees')

# Initialize DB when app context starts
with app.app_context():
    init_db()

# Close DB connection on app context teardown
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Serve files in 'outputs' folder for download
@app.route('/api/outputs/<path:filename>')
def download_file(filename):
    outputs_dir = os.path.abspath('outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    return send_from_directory(outputs_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
