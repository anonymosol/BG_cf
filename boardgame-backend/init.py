from flask import Flask
from utils.db import init_db
from routes.shifts import shift_bp  # ✅ Make sure this matches the Blueprint object name

app = Flask(__name__)
app.config['DATABASE'] = 'instance/database.db'
app.register_blueprint(shift_bp, url_prefix='/api')

with app.app_context():
    init_db()
