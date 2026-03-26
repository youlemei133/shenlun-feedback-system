# 题目、答案、批改数据访问
from models import Question, Answer, AnswerReview
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import Optional, List

class QuestionRepository(BaseRepository):
    model = Question
    
    @classmethod
    def get_active(cls) -> List[Question]:
        """获取所有激活的题目"""
        with get_db() as db:
            return db.query(Question).filter(
                Question.status == 'active'
            ).order_by(Question.created_at.desc()).all()
    
    @classmethod
    def get_with_answers(cls, question_id: int) -> Optional[dict]:
        """获取题目及答案"""
        with get_db() as db:
            question = db.query(Question).get(question_id)
            if not question:
                return None
            
            answers = db.query(Answer).filter(Answer.question_id == question_id).all()
            answer_a = next((a.to_dict() for a in answers if a.version == 'A'), None)
            answer_b = next((a.to_dict() for a in answers if a.version == 'B'), None)
            
            reviews = db.query(AnswerReview).filter(AnswerReview.question_id == question_id).all()
            review_a = next((r.to_dict() for r in reviews if r.answer_version == 'A'), None)
            review_b = next((r.to_dict() for r in reviews if r.answer_version == 'B'), None)
            
            return {
                'question': question.to_dict(),
                'answer_a': answer_a,
                'answer_b': answer_b,
                'review_a': review_a,
                'review_b': review_b
            }

class AnswerRepository(BaseRepository):
    model = Answer
    
    @classmethod
    def get_by_question_and_version(cls, question_id: int, version: str) -> Optional[Answer]:
        """根据题目ID和版本获取答案"""
        with get_db() as db:
            return db.query(Answer).filter(
                Answer.question_id == question_id,
                Answer.version == version
            ).first()
    
    @classmethod
    def create_or_update(cls, question_id: int, version: str, content: str, source: str = '') -> Answer:
        """创建或更新答案"""
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
                return existing
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
                return answer

class AnswerReviewRepository(BaseRepository):
    model = AnswerReview
    
    @classmethod
    def get_by_question_and_version(cls, question_id: int, answer_version: str) -> Optional[AnswerReview]:
        """根据题目ID和答案版本获取批改"""
        with get_db() as db:
            return db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id,
                AnswerReview.answer_version == answer_version
            ).first()
    
    @classmethod
    def get_by_question(cls, question_id: int) -> List[AnswerReview]:
        """获取题目的所有批改"""
        with get_db() as db:
            return db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id
            ).all()
    
    @classmethod
    def create_or_update(cls, question_id: int, answer_version: str, **kwargs) -> AnswerReview:
        """创建或更新批改"""
        with get_db() as db:
            existing = db.query(AnswerReview).filter(
                AnswerReview.question_id == question_id,
                AnswerReview.answer_version == answer_version
            ).first()
            
            if existing:
                for key, value in kwargs.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                db.flush()
                db.refresh(existing)
                return existing
            else:
                review = AnswerReview(
                    question_id=question_id,
                    answer_version=answer_version,
                    **kwargs
                )
                db.add(review)
                db.flush()
                db.refresh(review)
                return review
