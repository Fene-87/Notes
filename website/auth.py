from flask import Blueprint, render_template, request, flash, redirect, url_for

from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return '<p>Logout</p>'


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email must at least 4 characters", category='error')
        elif len(first_name) < 4:
            flash("First name must at least 4 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(password1) < 6:
            flash("Password must at least 6 characters", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully registered", category='success')
            return redirect(url_for('views.home'))
        
    return render_template('sign_up.html')
