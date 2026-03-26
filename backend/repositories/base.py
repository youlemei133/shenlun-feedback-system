# 基础 Repository
from utils.db_session import get_db
from typing import Type, TypeVar, List, Optional, Any

T = TypeVar('T')

class BaseRepository:
    """数据访问基类"""
    model: Type[T] = None
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[T]:
        """根据 ID 获取"""
        with get_db() as db:
            return db.query(cls.model).get(id)
    
    @classmethod
    def get_all(cls, order_by=None, limit: int = None) -> List[T]:
        """获取所有"""
        with get_db() as db:
            query = db.query(cls.model)
            if order_by is not None:
                query = query.order_by(order_by)
            if limit:
                query = query.limit(limit)
            return query.all()
    
    @classmethod
    def create(cls, **kwargs) -> T:
        """创建"""
        with get_db() as db:
            instance = cls.model(**kwargs)
            db.add(instance)
            db.flush()
            db.refresh(instance)
            return instance
    
    @classmethod
    def update(cls, id: int, **kwargs) -> Optional[T]:
        """更新"""
        with get_db() as db:
            instance = db.query(cls.model).get(id)
            if not instance:
                return None
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.flush()
            db.refresh(instance)
            return instance
    
    @classmethod
    def delete(cls, id: int) -> bool:
        """删除"""
        with get_db() as db:
            instance = db.query(cls.model).get(id)
            if not instance:
                return False
            db.delete(instance)
            return True
    
    @classmethod
    def count(cls) -> int:
        """计数"""
        with get_db() as db:
            return db.query(cls.model).count()
