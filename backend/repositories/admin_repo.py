# 管理员数据访问
from models import Admin
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import Optional

class AdminRepository(BaseRepository):
    model = Admin
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional[Admin]:
        """根据用户名获取管理员"""
        with get_db() as db:
            return db.query(Admin).filter(Admin.username == username).first()
    
    @classmethod
    def username_exists(cls, username: str) -> bool:
        """检查用户名是否存在"""
        return cls.get_by_username(username) is not None
