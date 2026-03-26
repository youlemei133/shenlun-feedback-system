# 路由层
from routes.public import public_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.admin_manage import admin_manage_bp
from routes.upload import upload_bp

def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_manage_bp)
    app.register_blueprint(upload_bp)
