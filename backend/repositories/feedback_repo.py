# 反馈数据访问
from models import Feedback
from repositories.base import BaseRepository
from utils.db_session import get_db
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class FeedbackRepository(BaseRepository):
    model = Feedback
    
    @classmethod
    def get_recent(cls, limit: int = 100) -> List[Dict]:
        """获取最近的反馈（返回 dict 列表）"""
        with get_db() as db:
            feedbacks = db.query(Feedback).order_by(
                Feedback.created_at.desc()
            ).limit(limit).all()
            return [f.to_dict() for f in feedbacks]
    
    @classmethod
    def get_by_user(cls, user_id: int) -> List[Dict]:
        """获取用户的反馈（返回 dict 列表）"""
        with get_db() as db:
            feedbacks = db.query(Feedback).filter(
                Feedback.user_id == user_id
            ).all()
            return [f.to_dict() for f in feedbacks]
    
    @classmethod
    def get_by_question(cls, question_id: int) -> List[Dict]:
        """获取题目的反馈（返回 dict 列表）"""
        with get_db() as db:
            feedbacks = db.query(Feedback).filter(
                Feedback.question_id == question_id
            ).all()
            return [f.to_dict() for f in feedbacks]
    
    @classmethod
    def count(cls, question_id: int = None) -> int:
        """计数"""
        with get_db() as db:
            query = db.query(Feedback)
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            return query.count()
    
    @classmethod
    def count_by_prefer(cls, prefer: str, question_id: int = None) -> int:
        """按偏好计数"""
        with get_db() as db:
            query = db.query(Feedback).filter(Feedback.prefer == prefer)
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            return query.count()
    
    @classmethod
    def count_by_willingness(cls, willingness: str, question_id: int = None) -> int:
        """按意愿计数"""
        with get_db() as db:
            query = db.query(Feedback).filter(Feedback.willing_to_train == willingness)
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            return query.count()
    
    @classmethod
    def count_today(cls, question_id: int = None) -> int:
        """今日计数"""
        with get_db() as db:
            today = datetime.now().date()
            today_start = f"{today} 00:00:00"
            today_end = f"{today} 23:59:59"
            query = db.query(Feedback).filter(
                Feedback.created_at >= today_start,
                Feedback.created_at <= today_end
            )
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            return query.count()
    
    @classmethod
    def get_trend(cls, days: int = 7, question_id: int = None) -> List[Dict]:
        """获取趋势数据"""
        with get_db() as db:
            today = datetime.now().date()
            dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days - 1, -1, -1)]
            
            trend_data = []
            for date_str in dates:
                start_date = f"{date_str} 00:00:00"
                end_date = f"{date_str} 23:59:59"
                
                query = db.query(Feedback).filter(
                    Feedback.created_at >= start_date,
                    Feedback.created_at <= end_date
                )
                if question_id:
                    query = query.filter(Feedback.question_id == question_id)
                
                count = query.count()
                
                query_a = db.query(Feedback).filter(
                    Feedback.created_at >= start_date,
                    Feedback.created_at <= end_date,
                    Feedback.prefer == 'A'
                )
                if question_id:
                    query_a = query_a.filter(Feedback.question_id == question_id)
                prefer_a = query_a.count()
                
                query_b = db.query(Feedback).filter(
                    Feedback.created_at >= start_date,
                    Feedback.created_at <= end_date,
                    Feedback.prefer == 'B'
                )
                if question_id:
                    query_b = query_b.filter(Feedback.question_id == question_id)
                prefer_b = query_b.count()
                
                trend_data.append({
                    'date': date_str,
                    'label': f"{int(date_str[5:7])}/{int(date_str[8:10])}",
                    'count': count,
                    'prefer_a': prefer_a,
                    'prefer_b': prefer_b
                })
            
            return trend_data
    
    @classmethod
    def get_all_with_filter(cls, question_id: int = None) -> List[Dict]:
        """获取所有反馈（可筛选，返回 dict 列表）"""
        with get_db() as db:
            query = db.query(Feedback)
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            feedbacks = query.all()
            return [f.to_dict() for f in feedbacks]
