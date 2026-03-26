# 反馈服务
from repositories.feedback_repo import FeedbackRepository
from repositories.user_repo import UserRepository
from utils.exceptions import ValidationError

class FeedbackService:
    @staticmethod
    def submit(user_id: int, question_id: int, prefer: str, ip_address: str = None,
               answer_prefer: str = None, review_prefer: str = None,
               reasons: list = None, other_reason: str = None,
               willing_to_train: str = None, answer_image: str = None):
        """提交反馈"""
        if not user_id or not question_id or not prefer:
            raise ValidationError('缺少必要参数')
        
        feedback = FeedbackRepository.create(
            user_id=user_id,
            question_id=question_id,
            prefer=prefer,
            answer_prefer=answer_prefer,
            review_prefer=review_prefer,
            reasons=reasons or [],
            other_reason=other_reason,
            willing_to_train=willing_to_train,
            ip_address=ip_address,
            answer_image=answer_image
        )
        return feedback
    
    @staticmethod
    def get_recent(limit: int = 100):
        """获取最近反馈"""
        feedbacks = FeedbackRepository.get_recent(limit)
        return [f.to_dict() for f in feedbacks]
