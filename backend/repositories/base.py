# 基础 Repository
from utils.db_session import get_db
from typing import Type, TypeVar, List, Optional, Any, Dict
from sqlalchemy import desc

T = TypeVar('T')

class BaseRepository:
    """数据访问基类"""
    model: Type[T] = None
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        """根据 ID 获取（返回 dict）"""
        with get_db() as db:
            instance = db.query(cls.model).get(id)
            return instance.to_dict() if instance else None
    
    @classmethod
    def get_all(cls, order_by=None, limit: int = None) -> List[Dict]:
        """获取所有（返回 dict 列表）
        
        Args:
            order_by: 排序字段，支持以下格式：
                - None: 不排序
                - 字符串 'field': 升序
                - 字符串 'field.desc': 降序
                - SQLAlchemy 列对象
        """
        with get_db() as db:
            query = db.query(cls.model)
            if order_by is not None:
                order_clause = cls._parse_order_by(order_by)
                if order_clause is not None:
                    query = query.order_by(order_clause)
            if limit:
                query = query.limit(limit)
            instances = query.all()
            return [i.to_dict() for i in instances]
    
    @classmethod
    def _parse_order_by(cls, order_by):
        """解析 order_by 参数"""
        if isinstance(order_by, str):
            if order_by.endswith('.desc'):
                field_name = order_by[:-5]
                if hasattr(cls.model, field_name):
                    return desc(getattr(cls.model, field_name))
            else:
                if hasattr(cls.model, order_by):
                    return getattr(cls.model, order_by)
            return None
        return order_by
    
    @classmethod
    def get_all_objects(cls, order_by=None, limit: int = None) -> List[T]:
        """获取所有（返回对象列表，用于需要访问关系的场景）"""
        with get_db() as db:
            query = db.query(cls.model)
            if order_by is not None:
                order_clause = cls._parse_order_by(order_by)
                if order_clause is not None:
                    query = query.order_by(order_clause)
            if limit:
                query = query.limit(limit)
            instances = query.all()
            for i in instances:
                db.expunge(i)
            return instances
    
    @classmethod
    def create(cls, **kwargs) -> Dict:
        """创建（返回 dict）"""
        with get_db() as db:
            instance = cls.model(**kwargs)
            db.add(instance)
            db.flush()
            db.refresh(instance)
            return instance.to_dict()
    
    @classmethod
    def update(cls, id: int, **kwargs) -> Optional[Dict]:
        """更新（返回 dict）"""
        with get_db() as db:
            instance = db.query(cls.model).get(id)
            if not instance:
                return None
            for key, value in kwargs.items():
                if hasattr(instance, key) and value is not None:
                    setattr(instance, key, value)
            db.flush()
            db.refresh(instance)
            return instance.to_dict()
    
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