# 认证服务
from repositories.admin_repo import AdminRepository
from utils.exceptions import AuthError
from flask_login import login_user, logout_user

class AuthService:
    @staticmethod
    def authenticate(username: str, password: str):
        """认证用户"""
        admin = AdminRepository.get_by_username(username)
        if not admin:
            raise AuthError('用户名不存在')
        if admin.password != password:
            raise AuthError('密码错误')
        return admin
    
    @staticmethod
    def login(username: str, password: str):
        """登录"""
        admin = AuthService.authenticate(username, password)
        login_user(admin)
        return admin
    
    @staticmethod
    def logout():
        """登出"""
        logout_user()
