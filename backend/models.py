# 数据库模型
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import SQLITE_DB_PATH
from flask_login import UserMixin

# 创建数据库连接（SQLite）
connection_string = f"sqlite:///{SQLITE_DB_PATH}"
engine = create_engine(connection_string, echo=True, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    """用户信息表"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    score = Column(String(10), nullable=False)  # 申论分数
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'phone': self.phone,
            'score': self.score,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Admin(Base, UserMixin):
    """管理员表"""
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    nickname = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Question(Base):
    """题目表"""
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)  # 题目名称
    material = Column(Text, nullable=False)  # 给定资料
    requirement = Column(Text, nullable=False)  # 作答要求
    score = Column(Integer, default=15)  # 分值
    status = Column(String(20), default='active')  # active/inactive
    answer_image = Column(Text, nullable=True)  # 用户作答图片 URL
    user_answer_text = Column(Text, nullable=True)  # 用户作答文字版
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'material': self.material,
            'requirement': self.requirement,
            'score': self.score,
            'status': self.status,
            'answer_image': self.answer_image,
            'user_answer_text': self.user_answer_text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Answer(Base):
    """答案表"""
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, nullable=False)  # 关联题目 ID
    version = Column(String(10), nullable=False)  # A 或 B
    content = Column(Text, nullable=False)  # 答案内容
    source = Column(String(50), nullable=True)  # 答案来源：上岸仓、粉笔
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'version': self.version,
            'content': self.content,
            'source': self.source,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class AnswerReview(Base):
    """答案批改详情表"""
    __tablename__ = 'answer_reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, nullable=False)  # 关联题目 ID
    review_style = Column(String(20), nullable=False, default='shangancang')  # 批改风格：shangancang/fenbi
    
    # 评分信息
    question_total_score = Column(Integer, default=15)  # 题目总分
    answer_total_score = Column(Integer, default=0)     # 答案得分总分
    
    # 要点统计 (JSON)
    # {"total": 5, "point_score": 3, "fully_scored": 3, "partially_scored": 1, "missing": 1}
    key_points_stats = Column(JSON, default=lambda: {
        "total": 0,
        "point_score": 0,
        "fully_scored": 0,
        "partially_scored": 0,
        "missing": 0
    })
    
    # 总体评价
    performance_summary = Column(Text, default="")     # 本次得分与表现
    next_steps = Column(Text, default="")              # 下一步提升方向
    
    # 遗漏要点列表 (JSON数组)
    # [{"title": "...", "analysis": "...", "suggestion": "..."}, ...]
    missing_points = Column(JSON, default=lambda: [])
    
    # 部分得分要点列表 (JSON数组)
    # [{"title": "...", "analysis": "...", "suggestion": "..."}, ...]
    partial_points = Column(JSON, default=lambda: [])
    
    # 作答逻辑评价
    logic_analysis = Column(Text, default="")
    
# 粉笔批改特有数据 (JSON)
    # {
    #   "my_answer": {
    #     "highlights": [{"text": "...", "score": 0.5}, ...],
    #     "diagnosis": "优缺点诊断（富文本）"
    #   },
    #   "score_analysis": [
    #     {"content": "...", "score": 0.5, "max_score": 3, "detail": "..."}
    #   ],
    #   "answer_demo": "答题演示（富文本）"
    # }
    fenbi_review_data = Column(JSON, nullable=True)
    
    # 上岸仓批改特有数据 (JSON)
    # {
    #   "my_answer": {
    #     "highlights": [{"text": "...", "score": 0.5}, ...]
    #   }
    # }
    shangancang_review_data = Column(JSON, nullable=True)
    
    # 要点描述文案（上岸仓批改专用）
    points_description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'review_style': self.review_style,
            'question_total_score': self.question_total_score,
            'answer_total_score': self.answer_total_score,
            'key_points_stats': self.key_points_stats,
            'performance_summary': self.performance_summary,
            'next_steps': self.next_steps,
            'missing_points': self.missing_points,
            'partial_points': self.partial_points,
            'logic_analysis': self.logic_analysis,
            'fenbi_review_data': self.fenbi_review_data,
            'shangancang_review_data': self.shangancang_review_data,
            'points_description': self.points_description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Feedback(Base):
    """用户反馈表"""
    __tablename__ = 'feedbacks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 用户 ID
    question_id = Column(Integer, nullable=False)  # 题目 ID
    prefer = Column(String(10), nullable=False)  # 最终偏好：A 或 B
    answer_prefer = Column(String(10), nullable=True)  # 答案偏好：A 或 B
    review_prefer = Column(String(10), nullable=True)  # 批改偏好：A 或 B
    reasons = Column(JSON, nullable=True)  # 选择的原因列表
    other_reason = Column(Text, nullable=True)  # 其他原因
    willing_to_train = Column(String(20), nullable=True)  # 是否愿意参与训练
    ip_address = Column(String(50), nullable=True)  # IP 地址
    answer_image = Column(Text, nullable=True)  # 用户作答图片 URL
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'prefer': self.prefer,
            'answer_prefer': self.answer_prefer,
            'review_prefer': self.review_prefer,
            'reasons': self.reasons,
            'other_reason': self.other_reason,
            'willing_to_train': self.willing_to_train,
            'ip_address': self.ip_address,
            'answer_image': self.answer_image,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# 创建所有表
def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
    print("数据库表创建成功！")
