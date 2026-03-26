# 认证路由
from flask import Blueprint, request
from flask_login import login_required, current_user
from utils.response import success, error
from utils.exceptions import AppException
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/admin')

@auth_bp.route('/login', methods=['POST'])
def login():
    """管理员登录"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return error('请输入用户名和密码')
    
    try:
        admin = AuthService.login(username, password)
        return success({'admin': admin.to_dict()})
    except AppException as e:
        return error(e.message)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """管理员登出"""
    AuthService.logout()
    return success()

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """检查登录状态"""
    if current_user.is_authenticated:
        return success({
            'authenticated': True,
            'admin': {
                'id': current_user.id,
                'username': current_user.username,
                'nickname': current_user.nickname
            }
        })
    return success({'authenticated': False})
