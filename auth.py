from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from DataBase import DBase
from UserLogin import UserLogin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder="assets")


@auth_bp.route('/login.html', methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        loginForm=request.form
        if "username" in loginForm.keys():
            if loginForm.get("password")==loginForm.get("passwordRepeat"):
                if DBase().addUser(loginForm["username"],loginForm["email"],loginForm["password"])==0:
                    return redirect("login.html")
                else:
                    LM = UserLogin().createUser(DBase().getUserByLogin(loginForm["username"]))
                    login_user(LM)
                    return redirect("/index.html")
            else:
                return redirect("login.html")
        else:
            if DBase().getUserByEmail(loginForm.get("email"))!=None:
                user=DBase().getUserByEmail(loginForm.get("email"))
                if user[3]==loginForm.get("password"):
                    LM = UserLogin().createUser(DBase().getUserByLogin(user[1]))
                    login_user(LM)
                    return redirect("/index.html")
        return redirect("login.html")

@auth_bp.route("/reway.html")
def reway():
    return redirect("/")

@auth_bp.route("/exit.html")
@login_required
def exit():
    logout_user()
    return redirect("/")