# 管理员数据访问
from models import Admin
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import Optional, Dict

class AdminRepository(BaseRepository):
    model = Admin
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional[Dict]:
        """根据用户名获取管理员（返回 dict）"""
        with get_db() as db:
            admin = db.query(Admin).filter(Admin.username == username).first()
            return admin.to_dict() if admin else None
    
    @classmethod
    def username_exists(cls, username: str) -> bool:
        """检查用户名是否存在"""
        with get_db() as db:
            return db.query(Admin).filter(Admin.username == username).first() is not None
