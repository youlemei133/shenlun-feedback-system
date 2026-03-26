# 管理员管理路由
from flask import Blueprint
from flask_login import login_required, current_user
from utils.response import success, error
from utils.exceptions import AppException, ValidationError
from repositories.admin_repo import AdminRepository

admin_manage_bp = Blueprint('admin_manage', __name__, url_prefix='/api/admin')

@admin_manage_bp.route('/admins', methods=['GET'])
@login_required
def get_admins():
    """获取管理员列表"""
    try:
        admins = AdminRepository.get_all(order_by='created_at.desc')
        return success({'admins': [a.to_dict() for a in admins]})
    except AppException as e:
        return error(e.message)

@admin_manage_bp.route('/admins', methods=['POST'])
@login_required
def create_admin():
    """创建管理员"""
    from flask import request
    data = request.json
    if not data:
        return error('数据不能为空')
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    nickname = data.get('nickname', '').strip()
    
    if not username or not password:
        return error('用户名和密码不能为空')
    
    if AdminRepository.username_exists(username):
        return error('用户名已存在')
    
    try:
        admin = AdminRepository.create(
            username=username,
            password=password,
            nickname=nickname or username
        )
        return success({'admin': admin.to_dict()})
    except AppException as e:
        return error(e.message)

@admin_manage_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@login_required
def delete_admin(admin_id):
    """删除管理员"""
    if admin_id == current_user.id:
        return error('不能删除当前登录的管理员')
    
    try:
        AdminRepository.delete(admin_id)
        return success()
    except AppException as e:
        return error(e.message)
