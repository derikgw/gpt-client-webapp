# auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from session.role import Role
from utility.db_utility import db
from session.user import User
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__, template_folder='templates')

bcrypt = Bcrypt()


def init(app, openai_playground):
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            if User.query.filter_by(email=email).first():
                flash('An account with this email already exists.', 'error')
                return redirect(url_for('auth.register'))

            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            default_role = Role.query.filter_by(name='user').first()

            if not default_role:
                flash('Registration error: default role not found.', 'error')
                return redirect(url_for('auth.register'))

            user = User(username=username, email=email, password_hash=hashed_pw, active=False, role=default_role)
            db.session.add(user)
            db.session.commit()

            flash('Your account has been created. Please wait for an admin to activate it.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('register.html')

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user is None or not bcrypt.check_password_hash(user.password_hash, password):
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))

            if not user.active:
                flash('Your account is not active. Please contact an administrator.', 'warning')
                return redirect(url_for('auth.login'))

            session['user_id'] = user.id
            return redirect(url_for('dashboard.dashboard'))

        return render_template('login.html')

    @auth_bp.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    # Register the blueprint with the app
    app.register_blueprint(auth_bp)
