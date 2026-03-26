# 管理后台路由
from flask import Blueprint, request
from flask_login import login_required, current_user
from utils.response import success, error
from utils.exceptions import AppException
from repositories.question_repo import QuestionRepository
from repositories.user_repo import UserRepository
from services.question_service import QuestionService, AnswerService, AnswerReviewService
from services.feedback_service import FeedbackService
from services.stats_service import StatsService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ==================== 题目管理 ====================

@admin_bp.route('/questions', methods=['GET'])
@login_required
def get_questions():
    """获取所有题目"""
    try:
        questions = QuestionRepository.get_all(order_by='created_at.desc')
        return success({'questions': [q.to_dict() for q in questions]})
    except AppException as e:
        return error(e.message)

@admin_bp.route('/question', methods=['POST'])
@login_required
def create_question():
    """创建题目"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    try:
        question = QuestionService.create(
            title=data.get('title'),
            material=data.get('material'),
            requirement=data.get('requirement'),
            score=data.get('score', 15),
            status=data.get('status', 'active')
        )
        return success({'question': question.to_dict()})
    except AppException as e:
        return error(e.message)

@admin_bp.route('/question/<int:question_id>', methods=['PUT'])
@login_required
def update_question(question_id):
    """更新题目"""
    data = request.json
    try:
        question = QuestionService.update(question_id, **data)
        return success({'question': question.to_dict()})
    except AppException as e:
        return error(e.message, e.code)

@admin_bp.route('/question/<int:question_id>/toggle-status', methods=['POST'])
@login_required
def toggle_question_status(question_id):
    """切换题目状态"""
    try:
        question = QuestionService.toggle_status(question_id)
        return success({'question': question.to_dict()})
    except AppException as e:
        return error(e.message, e.code)

# ==================== 答案管理 ====================

@admin_bp.route('/answer', methods=['POST'])
@login_required
def create_or_update_answer():
    """创建/更新答案"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    try:
        answer = AnswerService.create_or_update(
            question_id=data.get('question_id'),
            version=data.get('version'),
            content=data.get('content'),
            source=data.get('source', '')
        )
        return success({'answer': answer.to_dict()})
    except AppException as e:
        return error(e.message)

# ==================== 批改管理 ====================

@admin_bp.route('/review/<int:question_id>', methods=['GET'])
@login_required
def get_reviews(question_id):
    """获取批改"""
    try:
        reviews = AnswerReviewService.get_by_question(question_id)
        return success({'reviews': reviews})
    except AppException as e:
        return error(e.message)

@admin_bp.route('/review', methods=['POST'])
@login_required
def create_or_update_review():
    """创建/更新批改"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    try:
        review = AnswerReviewService.create_or_update(
            question_id=data.get('question_id'),
            answer_version=data.get('answer_version'),
            **data
        )
        return success({'review': review.to_dict()})
    except AppException as e:
        return error(e.message)

# ==================== 反馈管理 ====================

@admin_bp.route('/feedbacks', methods=['GET'])
@login_required
def get_feedbacks():
    """获取反馈列表"""
    try:
        feedbacks = FeedbackService.get_recent(100)
        return success({'feedbacks': feedbacks})
    except AppException as e:
        return error(e.message)

# ==================== 用户管理 ====================

@admin_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """获取用户列表"""
    try:
        users = UserService.get_all_with_feedback_count()
        return success({'users': users})
    except AppException as e:
        return error(e.message)

# ==================== 统计 ====================

@admin_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """获取基础统计"""
    try:
        stats = StatsService.get_basic()
        return success({'stats': stats})
    except AppException as e:
        return error(e.message)

@admin_bp.route('/stats/trend', methods=['GET'])
@login_required
def get_stats_trend():
    """获取趋势统计"""
    question_id = request.args.get('question_id', 'all')
    question_id = None if question_id == 'all' else int(question_id)
    
    try:
        trend = StatsService.get_trend(7, question_id)
        return success({'trend': trend})
    except AppException as e:
        return error(e.message)

@admin_bp.route('/stats/detailed', methods=['GET'])
@login_required
def get_detailed_stats():
    """获取详细统计"""
    question_id = request.args.get('question_id', 'all')
    question_id = None if question_id == 'all' else int(question_id)
    
    try:
        stats = StatsService.get_detailed(question_id)
        return success({'stats': stats})
    except AppException as e:
        return error(e.message)
