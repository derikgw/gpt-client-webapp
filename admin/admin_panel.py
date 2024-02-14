# admin/admin_panel.py
from flask import Blueprint, render_template, redirect, url_for, session, request

from session.governance import requires_role, requires_login
from utility.db_utility import db
from session.user import User
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/admin.admin_panel', methods=['GET'])
@requires_role('admin')
@requires_login
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        return redirect(url_for('index'))  # or some other error handling

    users = User.query.all()
    return render_template('admin_panel.html', users=users)


@admin_bp.route('/admin.activate-user/<int:user_id>', methods=['POST'])
def activate_user(user_id):
    # Similar logic as admin_panel to check for admin user
    user = User.query.get(user_id)
    user.active = True
    user.date_enabled = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/admin.deactivate-user/<int:user_id>', methods=['POST'])
def deactivate_user(user_id):
    # Similar logic as admin_panel to check for admin user
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/admin.delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Similar logic as admin_panel to check for admin user
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin_panel'))
