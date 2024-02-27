# session/governance.py
from flask import Blueprint, session, redirect, request
from utility.safe_urls import get_safe_redirect
from functools import wraps
from .user import User  # Import the User class from the user module

# Create a new Blueprint named 'governance'. This will group all governance-related routes.
governance_bp = Blueprint('governance', __name__)


# Decorator to enforce user login for protected routes
def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if 'user_id' is not in session, indicating the user is not logged in
        if 'user_id' not in session:
            # Redirect to the login page with safe redirection checking
            return redirect(get_safe_redirect('auth.login'))
        # Proceed with the original function if the user is logged in
        return func(*args, **kwargs)

    return decorated_function


# Decorator to enforce a specific user role for accessing protected routes
def requires_role(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # Retrieve 'user_id' from the session and fetch the user object
            user_id = session.get('user_id')
            user = User.query.get(user_id) if user_id else None
            # If the user does not exist or does not have the required role or is not active
            if not user or not user.is_admin or not user.active:
                # Redirect to the dashboard or a safe error page with safe redirection checking
                return redirect(get_safe_redirect('dashboard.dashboard'))
            # Proceed with the original function if the user has the required role
            return func(*args, **kwargs)

        return decorated_function

    return decorator


# Before request handler to ensure user authentication on every request
@governance_bp.before_app_request
def before_request():
    # List of routes that do not require authentication
    open_routes = ['auth.login', 'auth.register', 'static']
    # Allow unrestricted access to open routes
    if request.endpoint in open_routes:
        return None  # Do nothing for open routes
    # If 'user_id' is not found in the session, redirect to the login page
    if 'user_id' not in session:
        return redirect(get_safe_redirect('auth.login'))
    # Fetch the user object based on 'user_id' in session
    user = User.query.get(session['user_id'])
    # If the user does not exist or is inactive, clear the session and redirect to login
    if not user or not user.active:
        session.pop('user_id', None)
        return redirect(get_safe_redirect('auth.login'))



