from flask import Flask, render_template, request, redirect, flash
#from werkzeug.security import generate_password_hash, check_password_hash
from DataBase import DBase
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user


app = Flask(__name__, static_folder="assets", template_folder="templates")
app.config["SECRET_KEY"]="GvDeX"
login_manager=LoginManager(app)
login_manager.login_view = '/auth/login'

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromBD(user_id, DBase())


from auth import auth_bp
from core import core_bp

app.register_blueprint(auth_bp)
app.register_blueprint(core_bp)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port="5000", debug=True)