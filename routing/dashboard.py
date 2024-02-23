# dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from session.user import User
from session.governance import requires_login

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')


def init(app, openai_playground):
    @dashboard_bp.route('/')
    @dashboard_bp.route('/dashboard')
    @requires_login
    def dashboard():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))

        user = User.query.get(user_id)
        if not user:
            session.pop('user_id', None)
            return redirect(url_for('auth.login'))

        return render_template('dashboard.html', username=user.username)

    # Register the blueprint with the app
    app.register_blueprint(dashboard_bp)
