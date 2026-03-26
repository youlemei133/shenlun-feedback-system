# 数据库会话管理
from contextlib import contextmanager
from models import SessionLocal

@contextmanager
def get_db():
    """数据库会话上下文管理器
    
    使用方式:
        with get_db() as db:
            user = db.query(User).first()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def db_transaction(func):
    """数据库事务装饰器"""
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(db, *args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    return wrapper
