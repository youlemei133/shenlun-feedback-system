# 应用异常定义

class AppException(Exception):
    """应用异常基类"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(AppException):
    """资源不存在异常"""
    def __init__(self, resource: str = '资源'):
        super().__init__(f'{resource}不存在', 404)

class ValidationError(AppException):
    """数据验证异常"""
    def __init__(self, message: str = '数据验证失败'):
        super().__init__(message, 400)

class AuthError(AppException):
    """认证异常"""
    def __init__(self, message: str = '认证失败'):
        super().__init__(message, 401)

class ForbiddenError(AppException):
    """权限异常"""
    def __init__(self, message: str = '无权限执行此操作'):
        super().__init__(message, 403)

class DuplicateError(AppException):
    """重复数据异常"""
    def __init__(self, message: str = '数据已存在'):
        super().__init__(message, 400)
