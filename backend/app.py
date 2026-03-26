# Flask 主应用入口
from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from models import init_db, Admin
from config import SECRET_KEY
from routes import register_blueprints
from utils.exceptions import AppException

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.secret_key = SECRET_KEY
    
    # Session 配置
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # CORS 配置
    CORS(app, supports_credentials=True)
    
    # Flask-Login 配置
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin'
    
    @login_manager.user_loader
    def load_user(user_id):
        from utils.db_session import get_db
        with get_db() as db:
            admin = db.query(Admin).get(int(user_id))
            if admin:
                db.expunge(admin)
            return admin
    
    # 初始化数据库
    init_db()
    
    # 注册蓝图
    register_blueprints(app)
    
    # 全局异常处理
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        return jsonify({'success': False, 'message': e.message}), e.code
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'success': False, 'message': '资源不存在'}), 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
