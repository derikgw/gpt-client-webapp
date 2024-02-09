# admin/admin_panel.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash

from session.governance import requires_role, requires_login
from session.role import Role
from utility.db_utility import db
from session.user import User
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/admin', methods=['GET'])
@requires_role('admin')
@requires_login
def admin_panel():
    print("This is the admin panel")
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return redirect(request.referrer or url_for('dashboard'))

    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin_panel.html', users=users, roles=roles)


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

@admin_bp.route('/admin/update-user-role/<int:user_id>', methods=['POST'])
@requires_role('admin')
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    role_id = request.form.get('role_id')
    user.role_id = role_id
    db.session.commit()
    flash('User role updated successfully.', 'success')
    return redirect(url_for('admin.admin_panel'))
