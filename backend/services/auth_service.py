# 认证服务
from utils.exceptions import AuthError
from utils.db_session import get_db
from models import Admin
from flask_login import login_user, logout_user

class AuthService:
    @staticmethod
    def authenticate(username: str, password: str):
        """认证用户（返回 Admin 对象用于 Flask-Login）"""
        with get_db() as db:
            admin = db.query(Admin).filter(Admin.username == username).first()
            if not admin:
                raise AuthError('用户名不存在')
            if admin.password != password:
                raise AuthError('密码错误')
            db.expunge(admin)
            return admin
    
    @staticmethod
    def login(username: str, password: str):
        """登录（返回 dict）"""
        admin = AuthService.authenticate(username, password)
        login_user(admin)
        return admin.to_dict()
    
    @staticmethod
    def logout():
        """登出"""
        logout_user()