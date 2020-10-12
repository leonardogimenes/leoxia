from flask import Flask
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leoxia.db'
db = SQLAlchemy(app)

from .routes import component_routes, auth_routes, users_routes, command_routes
from .services import auth_service, users_service, command_service
from .models import user_model, component_model, pin_model
from .configs import authorization
from .models.user_model import User


db.create_all()
try:
    user = User(username='admin', password=generate_password_hash('admin@admin'), group=1)
    db.session.add(user)
    db.session.commit()
except Exception:
    pass

