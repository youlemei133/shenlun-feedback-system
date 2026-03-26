# 用户数据访问
from models import User
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import Optional, List

class UserRepository(BaseRepository):
    model = User
    
    @classmethod
    def get_by_phone(cls, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        with get_db() as db:
            return db.query(User).filter(User.phone == phone).first()
    
    @classmethod
    def get_all_with_feedback_count(cls) -> List[dict]:
        """获取所有用户及其反馈数"""
        with get_db() as db:
            users = db.query(User).order_by(User.created_at.desc()).all()
            result = []
            for user in users:
                user_dict = user.to_dict()
                from models import Feedback
                user_dict['feedback_count'] = db.query(Feedback).filter(
                    Feedback.user_id == user.id
                ).count()
                result.append(user_dict)
            return result
