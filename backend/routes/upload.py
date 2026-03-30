# 上传路由
from flask import Blueprint, request, send_from_directory
from flask_login import login_required
from utils.response import success, error
from utils.exceptions import AppException
from services.question_service import QuestionService
import os

upload_bp = Blueprint('upload', __name__, url_prefix='/api')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'answer_images')

@upload_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    """提供上传文件访问"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@upload_bp.route('/admin/upload-answer-image/<int:question_id>', methods=['POST'])
@login_required
def upload_answer_image(question_id):
    """上传答案图片和用户作答文字版"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    image_data = data.get('image', '')
    user_answer_text = data.get('user_answer_text', '')
    
    try:
        image_url = QuestionService.upload_answer_image(question_id, image_data, user_answer_text)
        return success({'image_url': image_url})
    except AppException as e:
        return error(e.message, e.code)
