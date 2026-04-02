# 公开路由（无需认证）
from flask import Blueprint, request, send_from_directory
from utils.response import success, error
from utils.exceptions import AppException
from services.user_service import UserService
from services.question_service import QuestionService
from services.feedback_service import FeedbackService
from services.stats_service import StatsService

public_bp = Blueprint('public', __name__)

# ==================== 页面路由 ====================

@public_bp.route('/')
def index():
    """主页面"""
    response = send_from_directory('..', 'frontend/index.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@public_bp.route('/admin')
def admin():
    """管理后台页面"""
    response = send_from_directory('..', 'frontend/admin.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@public_bp.route('/review-admin')
def review_admin():
    """批改配置页面"""
    response = send_from_directory('..', 'frontend/review-admin.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# ==================== API 路由 ====================

@public_bp.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    try:
        user = UserService.register(
            nickname=data.get('nickname', '').strip(),
            phone=data.get('phone', '').strip(),
            score=data.get('score', '').strip()
        )
        return success({'user_id': user['id'], 'user': user})
    except AppException as e:
        return error(e.message)

@public_bp.route('/api/questions/active', methods=['GET'])
def get_active_questions():
    """获取激活的题目"""
    try:
        questions = QuestionService.get_active()
        return success({'questions': questions})
    except AppException as e:
        return error(e.message)

@public_bp.route('/api/question/next', methods=['GET'])
def get_next_question():
    """获取下一个题目（反馈数最少的激活题目）"""
    try:
        question = QuestionService.get_next_for_user()
        if not question:
            return error('暂无可用题目')
        return success({'question': question})
    except AppException as e:
        return error(e.message)

@public_bp.route('/api/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """获取题目详情"""
    try:
        data = QuestionService.get_with_answers(question_id)
        return success(data)
    except AppException as e:
        return error(e.message, e.code)

@public_bp.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交反馈"""
    data = request.json
    if not data:
        return error('数据不能为空')
    
    try:
        feedback = FeedbackService.submit(
            user_id=data.get('user_id'),
            question_id=data.get('question_id'),
            prefer=data.get('prefer'),
            ip_address=request.remote_addr,
            answer_prefer=data.get('answer_prefer'),
            review_prefer=data.get('review_prefer'),
            reasons=data.get('reasons', []),
            other_reason=data.get('other_reason'),
            willing_to_train=data.get('willing_to_train'),
            answer_image=data.get('answer_image')
        )
        return success({'feedback_id': feedback['id']})
    except AppException as e:
        return error(e.message)

@public_bp.route('/api/stats', methods=['GET'])
def get_public_stats():
    """获取公开统计数据（主页使用）"""
    try:
        stats = StatsService.get_basic()
        return success({'stats': stats})
    except AppException as e:
        return error(e.message)

@public_bp.route('/api/user/verify', methods=['GET'])
def verify_user():
    """验证用户是否存在"""
    user_id = request.args.get('user_id')
    if not user_id:
        return error('user_id 参数必填')
    
    try:
        user_id = int(user_id)
        exists = UserService.verify_user(user_id)
        return success({'exists': exists, 'user_id': user_id})
    except (ValueError, AppException) as e:
        return error('无效的 user_id')
