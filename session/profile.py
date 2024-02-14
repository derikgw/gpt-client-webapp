# profile.py
from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from utility.db_utility import db  # Adjust the import path as necessary
from session.user import User  # Adjust the import path as necessary

profile_bp = Blueprint('profile', __name__, template_folder='templates')


@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')

        # Ensure new username and email are unique
        if User.query.filter(User.username == new_username, User.id != user_id).first():
            flash('Username already taken.', 'error')
        elif User.query.filter(User.email == new_email, User.id != user_id).first():
            flash('Email already in use.', 'error')
        else:
            user.username = new_username
            user.email = new_email
            db.session.commit()
            flash('Profile updated successfully!', 'success')

    return render_template('profile.html', user=user)
