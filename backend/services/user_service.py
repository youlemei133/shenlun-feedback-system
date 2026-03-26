# 用户服务
from repositories.user_repo import UserRepository
from utils.exceptions import ValidationError, DuplicateError

class UserService:
    @staticmethod
    def register(nickname: str, phone: str, score: str):
        """用户注册"""
        if not nickname or not phone or not score:
            raise ValidationError('请填写完整信息')
        
        existing = UserRepository.get_by_phone(phone)
        if existing:
            raise DuplicateError('该手机号已注册')
        
        user = UserRepository.create(
            nickname=nickname,
            phone=phone,
            score=score
        )
        return user
    
    @staticmethod
    def get_all_with_feedback_count():
        """获取所有用户及反馈数"""
        return UserRepository.get_all_with_feedback_count()
