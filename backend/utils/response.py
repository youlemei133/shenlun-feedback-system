# 统一响应格式
from flask import jsonify
from typing import Any, Optional, Dict, List

def success(data: Any = None, message: str = '操作成功'):
    """成功响应"""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response)

def error(message: str, code: int = 400):
    """错误响应"""
    return jsonify({'success': False, 'message': message}), code

def paginated(items: List, total: int, page: int = 1, page_size: int = 20):
    """分页响应"""
    return jsonify({
        'success': True,
        'data': items,
        'pagination': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'pages': (total + page_size - 1) // page_size if page_size > 0 else 0
        }
    })

def success_with(**kwargs):
    """自定义成功响应"""
    result = {'success': True}
    result.update(kwargs)
    return jsonify(result)
