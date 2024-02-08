# session/governance.py
from flask import Blueprint, session, redirect, url_for, request
from functools import wraps
from .user import User  # Adjust the import path based on your project structure

governance_bp = Blueprint('governance', __name__)


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


def requires_role(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            user = User.query.get(user_id) if user_id else None
            if not user or user.role != role or not user.active:
                return redirect(url_for('index'))  # or some error page
            return func(*args, **kwargs)

        return decorated_function

    return decorator


@governance_bp.before_app_request
def before_request():
    open_routes = ['login', 'register', 'static']
    if request.endpoint not in open_routes and 'user_id' not in session:
        return redirect(url_for('login'))
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if not user or not user.active:
            session.pop('user_id', None)
            return redirect(url_for('login'))