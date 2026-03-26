# 重置数据库脚本
import os
import sys

# 删除数据库文件
db_path = os.path.join(os.path.dirname(__file__), 'shenlun_feedback.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✓ 已删除数据库文件: {db_path}")
else:
    print("数据库文件不存在")

# 重新创建表
from models import init_db
init_db()
print("✓ 数据库表已重新创建")
print("\n现在可以重新启动后端服务了：python app.py")
