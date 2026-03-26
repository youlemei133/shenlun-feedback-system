# 统计服务
from repositories.feedback_repo import FeedbackRepository
from repositories.user_repo import UserRepository
from repositories.question_repo import AnswerRepository
from utils.constants import AnswerSource, Willingness, ScoreThreshold
from utils.db_session import get_db
from datetime import datetime

class StatsService:
    @staticmethod
    def get_basic():
        """获取基础统计"""
        total_feedbacks = FeedbackRepository.count()
        prefer_a = FeedbackRepository.count_by_prefer('A')
        prefer_b = FeedbackRepository.count_by_prefer('B')
        total_users = UserRepository.count()
        
        return {
            'total_feedbacks': total_feedbacks,
            'prefer_a': prefer_a,
            'prefer_b': prefer_b,
            'total_users': total_users,
            'prefer_a_rate': round(prefer_a / total_feedbacks * 100, 2) if total_feedbacks > 0 else 0,
            'prefer_b_rate': round(prefer_b / total_feedbacks * 100, 2) if total_feedbacks > 0 else 0
        }
    
    @staticmethod
    def get_trend(days: int = 7, question_id: int = None):
        """获取趋势数据"""
        return FeedbackRepository.get_trend(days, question_id)
    
    @staticmethod
    def get_detailed(question_id: int = None):
        """获取详细统计"""
        today = datetime.now().date()
        today_start = f"{today} 00:00:00"
        today_end = f"{today} 23:59:59"
        
        all_feedbacks = FeedbackRepository.get_all_with_filter(question_id)
        
        answer_source_stats = StatsService._calc_answer_source(all_feedbacks, today_start, today_end, question_id)
        review_source_stats = StatsService._calc_review_source(question_id, today_start, today_end)
        willingness_stats = StatsService._calc_willingness(question_id, today_start, today_end)
        willingness_by_score = StatsService._calc_willingness_by_score(question_id)
        
        total_feedbacks = len(all_feedbacks)
        today_feedbacks = FeedbackRepository.count_today(question_id)
        
        return {
            'summary': {
                'total_feedbacks': total_feedbacks,
                'today_feedbacks': today_feedbacks,
                'prefer_ai_answer': {
                    'total': answer_source_stats['total'].get(AnswerSource.SHANGANCANG, 0),
                    'today': answer_source_stats['today'].get(AnswerSource.SHANGANCANG, 0)
                },
                'prefer_shangancang_review': {
                    'total': review_source_stats['total'].get(AnswerSource.SHANGANCANG, 0),
                    'today': review_source_stats['today'].get(AnswerSource.SHANGANCANG, 0)
                },
                'willing_to_experience': {
                    'total': willingness_stats['total'].get(Willingness.VERY_WILLING, 0) + willingness_stats['total'].get(Willingness.WILLING, 0),
                    'today': willingness_stats['today'].get(Willingness.VERY_WILLING, 0) + willingness_stats['today'].get(Willingness.WILLING, 0)
                }
            },
            'answer_source': answer_source_stats,
            'review_source': review_source_stats,
            'willingness': willingness_stats,
            'willingness_by_score': willingness_by_score
        }
    
    @staticmethod
    def _calc_answer_source(feedbacks, today_start, today_end, question_id):
        """计算答案来源统计"""
        stats = {
            'total': {AnswerSource.SHANGANCANG: 0, AnswerSource.FENBI: 0, AnswerSource.UNKNOWN: 0},
            'today': {AnswerSource.SHANGANCANG: 0, AnswerSource.FENBI: 0, AnswerSource.UNKNOWN: 0}
        }
        
        for feedback in feedbacks:
            answer = AnswerRepository.get_by_question_and_version(feedback['question_id'], feedback['prefer'])
            source = answer.get('source') if answer else AnswerSource.UNKNOWN
            
            if source in stats['total']:
                stats['total'][source] += 1
            
            # feedback['created_at'] 已经是字符串格式
            feedback_time = feedback['created_at']
            if today_start <= feedback_time <= today_end:
                if source in stats['today']:
                    stats['today'][source] += 1
        
        return stats
    
    @staticmethod
    def _calc_review_source(question_id, today_start, today_end):
        """计算批改来源统计"""
        return {
            'total': {
                AnswerSource.SHANGANCANG: FeedbackRepository.count_by_prefer('A', question_id),
                AnswerSource.FENBI: FeedbackRepository.count_by_prefer('B', question_id)
            },
            'today': StatsService._count_today_by_prefer(question_id, today_start, today_end)
        }
    
    @staticmethod
    def _count_today_by_prefer(question_id, today_start, today_end):
        """今日偏好统计"""
        with get_db() as db:
            from models import Feedback
            query_a = db.query(Feedback).filter(
                Feedback.prefer == 'A',
                Feedback.created_at >= today_start,
                Feedback.created_at <= today_end
            )
            query_b = db.query(Feedback).filter(
                Feedback.prefer == 'B',
                Feedback.created_at >= today_start,
                Feedback.created_at <= today_end
            )
            if question_id:
                query_a = query_a.filter(Feedback.question_id == question_id)
                query_b = query_b.filter(Feedback.question_id == question_id)
            return {
                AnswerSource.SHANGANCANG: query_a.count(),
                AnswerSource.FENBI: query_b.count()
            }
    
    @staticmethod
    def _calc_willingness(question_id, today_start, today_end):
        """计算参与意愿统计"""
        stats = {
            'total': {w: 0 for w in Willingness.ALL},
            'today': {w: 0 for w in Willingness.ALL}
        }
        
        for w in Willingness.ALL:
            stats['total'][w] = FeedbackRepository.count_by_willingness(w, question_id)
            stats['today'][w] = StatsService._count_today_by_willingness(w, question_id, today_start, today_end)
        
        return stats
    
    @staticmethod
    def _count_today_by_willingness(willingness, question_id, today_start, today_end):
        """今日意愿统计"""
        with get_db() as db:
            from models import Feedback
            query = db.query(Feedback).filter(
                Feedback.willing_to_train == willingness,
                Feedback.created_at >= today_start,
                Feedback.created_at <= today_end
            )
            if question_id:
                query = query.filter(Feedback.question_id == question_id)
            return query.count()
    
    @staticmethod
    def _calc_willingness_by_score(question_id):
        """按分数段计算参与意愿"""
        result = {
            'below_55': {'label': '55分以下', **{w: 0 for w in Willingness.ALL}},
            'above_55': {'label': '55分以上', **{w: 0 for w in Willingness.ALL}}
        }
        
        users = UserRepository.get_all()
        
        for user in users:
            try:
                user_score = float(user['score'])
                score_range = 'below_55' if user_score < ScoreThreshold.LOW else 'above_55'
            except (ValueError, TypeError):
                continue
            
            user_feedbacks = FeedbackRepository.get_by_user(user['id'])
            if question_id:
                user_feedbacks = [f for f in user_feedbacks if f['question_id'] == question_id]
            
            for feedback in user_feedbacks:
                mood = feedback.get('willing_to_train') or Willingness.NOT_INTERESTED
                if mood in result[score_range]:
                    result[score_range][mood] += 1
        
        return result
