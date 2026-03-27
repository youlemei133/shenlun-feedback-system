# 题目、答案、批改数据访问
from models import Question, Answer, AnswerReview, Feedback
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import Optional, List, Dict
from sqlalchemy import func

class QuestionRepository(BaseRepository):
    model = Question
    
    @classmethod
    def get_active(cls) -> List[Dict]:
        """获取所有激活的题目（返回 dict 列表）"""
        with get_db() as db:
            questions = db.query(Question).filter(
                Question.status == 'active'
            ).order_by(Question.created_at.desc()).all()
            return [q.to_dict() for q in questions]
    
    @classmethod
    def get_next_for_user(cls) -> Optional[Dict]:
        """获取下一个应该下发给用户的题目（反馈数最少的激活题目）"""
        with get_db() as db:
            # 左连接统计每个题目的反馈数，按反馈数升序排序
            result = db.query(
                Question,
                func.count(Feedback.id).label('feedback_count')
            ).outerjoin(
                Feedback, Question.id == Feedback.question_id
            ).filter(
                Question.status == 'active'
            ).group_by(
                Question.id
            ).order_by(
                func.count(Feedback.id).asc()
            ).first()
            
            if result:
                question, feedback_count = result
                question_dict = question.to_dict()
                question_dict['feedback_count'] = feedback_count
                return question_dict
            return None
    
    @classmethod
    def get_with_answers(cls, question_id: int) -> Optional[Dict]:
        """获取题目及答案（返回 dict）"""
        with get_db() as db:
            question = db.query(Question).get(question_id)
            if not question:
                return None
            
            answers = db.query(Answer).filter(Answer.question_id == question_id).all()
            answer_a = next((a.to_dict() for a in answers if a.version == 'A'), None)
            answer_b = next((a.to_dict() for a in answers if a.version == 'B'), None)
            
            reviews = db.query(AnswerReview).filter(AnswerReview.question_id == question_id).all()
            reviews_dict = {}
            for r in reviews:
                key = f"{r.answer_version.lower()}_{r.review_style}"
                reviews_dict[key] = r.to_dict()
            
            return {
                'question': question.to_dict(),
                'answer_a': answer_a,
                'answer_b': answer_b,
                'reviews': reviews_dict
            }

class AnswerRepository(BaseRepository):
    model = Answer
    
    @classmethod
    def get_by_question_and_version(cls, question_id: int, version: str) -> Optional[Dict]:
        """根据题目ID和版本获取答案（返回 dict）"""
        with get_db() as db:
            answer = db.query(Answer).filter(
                Answer.question_id == question_id,
                Answer.version == version
            ).first()
            return answer.to_dict() if answer else None
    
    @classmethod
    def create_or_update(cls, question_id: int, version: str, content: str, source: str = '') -> Dict:
        """创建或更新答案（返回 dict）"""
        with get_db() as db:
            existing = db.query(Answer).filter(
                Answer.question_id == question_id,
                Answer.version == version
            ).first()
            
            if existing:
                existing.content = content
                existing.source = source
                db.flush()
                db.refresh(existing)
                return existing.to_dict()
            else:
                answer = Answer(
                    question_id=question_id,
                    version=version,
                    content=content,
                    source=source
                )
                db.add(answer)
                db.flush()
                db.refresh(answer)
                return answer.to_dict()

class AnswerReviewRepository(BaseRepository):
    model = AnswerReview
    
    @classmethod
    def get_by_question_answer_style(cls, question_id: int, answer_version: str, review_style: str) -> Optional[Dict]:
        """根据题目ID、答案版本和批改风格获取批改（返回 dict）"""
        with get_db() as db:
            review = db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id,
                AnswerReview.answer_version == answer_version,
                AnswerReview.review_style == review_style
            ).first()
            return review.to_dict() if review else None
    
    @classmethod
    def get_by_question_and_version(cls, question_id: int, answer_version: str) -> List[Dict]:
        """根据题目ID和答案版本获取所有批改（返回 dict 列表）"""
        with get_db() as db:
            reviews = db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id,
                AnswerReview.answer_version == answer_version
            ).all()
            return [r.to_dict() for r in reviews]
    
    @classmethod
    def get_by_question(cls, question_id: int) -> List[Dict]:
        """获取题目的所有批改（返回 dict 列表）"""
        with get_db() as db:
            reviews = db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id
            ).all()
            return [r.to_dict() for r in reviews]
    
    @classmethod
    def create_or_update(cls, question_id: int, answer_version: str, review_style: str, **kwargs) -> Dict:
        """创建或更新批改（返回 dict）"""
        with get_db() as db:
            existing = db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id,
                AnswerReview.answer_version == answer_version,
                AnswerReview.review_style == review_style
            ).first()
            
            if existing:
                for key, value in kwargs.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                db.flush()
                db.refresh(existing)
                return existing.to_dict()
            else:
                review = AnswerReview(
                    question_id=question_id,
                    answer_version=answer_version,
                    review_style=review_style,
                    **kwargs
                )
                db.add(review)
                db.flush()
                db.refresh(review)
                return review.to_dict()
