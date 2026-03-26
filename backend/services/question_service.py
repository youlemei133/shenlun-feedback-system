# 题目服务
from repositories.question_repo import QuestionRepository, AnswerRepository, AnswerReviewRepository
from utils.exceptions import NotFoundError, ValidationError
from utils.constants import QuestionStatus
import os
import uuid
import base64

class QuestionService:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'answer_images')
    
    @staticmethod
    def get_active():
        """获取激活的题目"""
        return QuestionRepository.get_active()
    
    @staticmethod
    def get_with_answers(question_id: int):
        """获取题目及答案"""
        data = QuestionRepository.get_with_answers(question_id)
        if not data:
            raise NotFoundError('题目')
        return data
    
    @staticmethod
    def create(title: str, material: str, requirement: str, score: int = 15, status: str = 'active'):
        """创建题目"""
        if not title or not material or not requirement:
            raise ValidationError('请填写必填项')
        
        return QuestionRepository.create(
            title=title,
            material=material,
            requirement=requirement,
            score=score,
            status=status
        )
    
    @staticmethod
    def update(question_id: int, **kwargs):
        """更新题目"""
        question = QuestionRepository.update(question_id, **kwargs)
        if not question:
            raise NotFoundError('题目')
        return question
    
    @staticmethod
    def toggle_status(question_id: int):
        """切换题目状态"""
        question = QuestionRepository.get_by_id(question_id)
        if not question:
            raise NotFoundError('题目')
        
        new_status = 'inactive' if question.get('status') == 'active' else 'active'
        return QuestionRepository.update(question_id, status=new_status)
    
    @staticmethod
    def upload_answer_image(question_id: int, image_data: str):
        """上传答案图片"""
        question = QuestionRepository.get_by_id(question_id)
        if not question:
            raise NotFoundError('题目')
        
        if not image_data:
            raise ValidationError('图片数据不能为空')
        
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception:
            raise ValidationError('图片格式错误')
        
        os.makedirs(QuestionService.UPLOAD_FOLDER, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(QuestionService.UPLOAD_FOLDER, filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        image_url = f"/api/uploads/{filename}"
        QuestionRepository.update(question_id, answer_image=image_url)
        
        return image_url

class AnswerService:
    @staticmethod
    def create_or_update(question_id: int, version: str, content: str, source: str = ''):
        """创建或更新答案"""
        if not question_id or not version or not content:
            raise ValidationError('缺少必要参数')
        
        return AnswerRepository.create_or_update(
            question_id=question_id,
            version=version,
            content=content,
            source=source
        )

class AnswerReviewService:
    @staticmethod
    def get_by_question(question_id: int):
        """获取题目的批改"""
        return AnswerReviewRepository.get_by_question(question_id)
    
    @staticmethod
    def create_or_update(question_id: int, answer_version: str, **kwargs):
        """创建或更新批改"""
        if not question_id or not answer_version:
            raise ValidationError('缺少必要参数')
        
        default_key_points = {
            "total": 0,
            "point_score": 0,
            "fully_scored": 0,
            "partially_scored": 0,
            "missing": 0
        }
        
        data = {
            'question_total_score': kwargs.get('question_total_score', 15),
            'answer_total_score': kwargs.get('answer_total_score', 0),
            'key_points_stats': kwargs.get('key_points_stats', default_key_points),
            'performance_summary': kwargs.get('performance_summary', ''),
            'next_steps': kwargs.get('next_steps', ''),
            'missing_points': kwargs.get('missing_points', []),
            'partial_points': kwargs.get('partial_points', []),
            'logic_analysis': kwargs.get('logic_analysis', '')
        }
        
        return AnswerReviewRepository.create_or_update(
            question_id=question_id,
            answer_version=answer_version,
            **data
        )
