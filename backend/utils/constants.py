# 常量定义

class AnswerSource:
    """答案来源"""
    SHANGANCANG = '上岸仓'
    FENBI = '粉笔'
    UNKNOWN = 'unknown'
    
    ALL = [SHANGANCANG, FENBI]
    CHOICES = [
        (SHANGANCANG, '上岸仓'),
        (FENBI, '粉笔')
    ]

class Willingness:
    """参与意愿"""
    VERY_WILLING = '很想体验'
    WILLING = '愿意尝试'
    NOT_INTERESTED = '没兴趣'
    
    ALL = [VERY_WILLING, WILLING, NOT_INTERESTED]

class ScoreThreshold:
    """分数阈值"""
    LOW = 55  # 低分阈值

class QuestionStatus:
    """题目状态"""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
    ALL = [ACTIVE, INACTIVE]
    CHOICES = [
        (ACTIVE, '激活'),
        (INACTIVE, '未激活')
    ]

class AnswerVersion:
    """答案版本"""
    A = 'A'
    B = 'B'
    
    ALL = [A, B]
