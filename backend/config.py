# 配置文件
import os

# SQLite 配置（临时项目推荐，无需数据库服务）
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'shenlun_feedback.db')

# MySQL 配置（如需使用 MySQL，取消下方注释并修改上方 SQLite）
# MYSQL_CONFIG = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'root',
#     'password': 'hudawei',
#     'database': 'shenlun_feedback'
# }

# Flask 配置
SECRET_KEY = os.urandom(24).hex()
DEBUG = True

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
