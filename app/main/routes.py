import pyhibp
from flask import render_template, request, redirect, url_for
from pyhibp import pwnedpasswords as ppw
from sqlalchemy import desc

from extensions import bcrypt
from main import bp
from models.user import User

# Required: A descriptive user agent must be set describing the application consuming the HIBP API
pyhibp.set_user_agent(ua="Awesome application/0.0.1 (An awesome description)")


@bp.route('/', methods=["GET", "POST"])
def index():
    pawned_count = -1
    user_email = ""
    user_password = ""

    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")

        # Check a password to see if it has been disclosed in a public breach corpus
        pawned_count = ppw.is_password_breached(password=user_password)
        if pawned_count:
            print(f"Password breached! - This password was used {pawned_count} time(s) before.")
        else:
            user_password_hashed = bcrypt.generate_password_hash(user_password).decode('utf-8')
            User.add_user(user_email, user_password_hashed)
            return redirect(url_for('main.list_users'))

    return render_template('index.html', user_email=user_email, user_password=user_password, pawned_count=pawned_count)


@bp.route('/users')
def list_users():
    users = User.query.order_by(desc(User.created_at))
    return render_template('users/list_users.html', users=users)


@bp.post('/<int:user_id>/delete/')
def delete(user_id):
    User.remove_user(user_id)
    return redirect(url_for('main.list_users'))
