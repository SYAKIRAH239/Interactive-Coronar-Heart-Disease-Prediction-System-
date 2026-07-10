from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from config import Config

mysql         = MySQL()
bcrypt        = Bcrypt()
login_manager = LoginManager()

# ================================================
# User class for Flask-Login
# ================================================
class Doctor(UserMixin):
    def __init__(self, doctor_id, username, email, profile_image=None):
        self.id            = doctor_id
        self.username      = username
        self.email         = email
        self.profile_image = profile_image or 'default_profile.png'

@login_manager.user_loader
def load_user(doctor_id):
    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return Doctor(
            user['doctor_id'],
            user['username'],
            user['email'],
            user['profile_image']
        )
    return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view            = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.routes.auth      import auth
    from app.routes.dashboard import dashboard
    from app.routes.patient   import patient
    from app.routes.profile   import profile

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(patient)
    app.register_blueprint(profile)

    return app

