# 清空所有数据但保留表结构
from models import SessionLocal, User, Feedback, Question, Answer, AnswerReview

db = SessionLocal()

try:
    # 删除顺序：先删有外键依赖的表
    db.query(Feedback).delete()
    print("已删除所有反馈数据")
    
    db.query(AnswerReview).delete()
    print("已删除所有批改数据")
    
    db.query(Answer).delete()
    print("已删除所有答案数据")
    
    db.query(Question).delete()
    print("已删除所有题目数据")
    
    db.query(User).delete()
    print("已删除所有用户数据")
    
    db.commit()
    print("\n所有数据已清空，可以重新测试了！")
    print("\n注意：题目和答案也需要重新配置")
    
except Exception as e:
    db.rollback()
    print(f"错误: {e}")
finally:
    db.close()
