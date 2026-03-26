# Flask 主应用
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import Session
from models import init_db, SessionLocal, User, Question, Answer, AnswerReview, Feedback, Admin
from datetime import datetime
from config import SECRET_KEY
import os
import base64
import uuid

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

# Flask-Login 配置
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    try:
        return db.query(Admin).get(int(user_id))
    finally:
        db.close()

# 初始化数据库
init_db()

# 上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'answer_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# ==================== 前端页面路由 ====================

@app.route('/')
def index():
    """主页面 - 批改对比"""
    response = send_from_directory(app.static_folder, 'index.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# @app.route('/register')  # 已改为弹窗形式，不再需要独立页面
# def register():
#     response = send_from_directory(app.static_folder, 'register.html')
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#     return response

@app.route('/admin')
def admin():
    """管理后台页面"""
    response = send_from_directory(app.static_folder, 'admin.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/review-admin')
def review_admin():
    """批改详情配置页面"""
    response = send_from_directory(app.static_folder, 'review-admin.html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# ==================== API 路由 ====================

@app.route('/api/register', methods=['POST'])
def api_register():
    """用户注册"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    nickname = data.get('nickname', '').strip()
    phone = data.get('phone', '').strip()
    score = data.get('score', '').strip()
    
    if not nickname or not phone or not score:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    db = SessionLocal()
    try:
        # 检查手机号是否已存在
        existing = db.query(User).filter(User.phone == phone).first()
        if existing:
            return jsonify({'success': False, 'message': '该手机号已注册'}), 400
        
        # 创建新用户
        user = User(nickname=nickname, phone=phone, score=score)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return jsonify({'success': True, 'user_id': user.id, 'user': user.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/questions/active', methods=['GET'])
def get_active_questions():
    """获取所有激活的题目"""
    db = SessionLocal()
    try:
        questions = db.query(Question).filter(Question.status == 'active').all()
        return jsonify({'success': True, 'questions': [q.to_dict() for q in questions]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """获取单个题目及答案"""
    db = SessionLocal()
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return jsonify({'success': False, 'message': '题目不存在'}), 404
        
        answers = db.query(Answer).filter(Answer.question_id == question_id).all()
        answer_a = next((a.to_dict() for a in answers if a.version == 'A'), None)
        answer_b = next((a.to_dict() for a in answers if a.version == 'B'), None)
        
        # 获取批改详情
        reviews = db.query(AnswerReview).filter(AnswerReview.question_id == question_id).all()
        review_a = next((r.to_dict() for r in reviews if r.answer_version == 'A'), None)
        review_b = next((r.to_dict() for r in reviews if r.answer_version == 'B'), None)
        
        return jsonify({
            'success': True,
            'question': question.to_dict(),
            'answer_a': answer_a,
            'answer_b': answer_b,
            'review_a': review_a,
            'review_b': review_b
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交用户反馈"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    prefer = data.get('prefer')
    answer_prefer = data.get('answer_prefer')
    review_prefer = data.get('review_prefer')
    reasons = data.get('reasons', [])
    other_reason = data.get('other_reason', '')
    willing_to_train = data.get('willing_to_train', '')
    answer_image = data.get('answer_image', '')
    
    if not user_id or not question_id or not prefer:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    
    db = SessionLocal()
    try:
        feedback = Feedback(
            user_id=user_id,
            question_id=question_id,
            prefer=prefer,
            answer_prefer=answer_prefer,
            review_prefer=review_prefer,
            reasons=reasons,
            other_reason=other_reason,
            willing_to_train=willing_to_train,
            ip_address=request.remote_addr,
            answer_image=answer_image
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        
        return jsonify({'success': True, 'feedback_id': feedback.id})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

# ==================== 管理后台 API ====================

# ---------- 认证相关 API ----------

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 400
    
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            return jsonify({'success': False, 'message': '用户名不存在'}), 400
        
        if admin.password != password:
            return jsonify({'success': False, 'message': '密码错误'}), 400
        
        login_user(admin)
        return jsonify({'success': True, 'admin': admin.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    """管理员登出"""
    logout_user()
    return jsonify({'success': True})

@app.route('/api/admin/check-auth', methods=['GET'])
def admin_check_auth():
    """检查登录状态"""
    if current_user.is_authenticated:
        return jsonify({
            'success': True, 
            'authenticated': True, 
            'admin': {
                'id': current_user.id,
                'username': current_user.username,
                'nickname': current_user.nickname
            }
        })
    return jsonify({'success': True, 'authenticated': False})

# ---------- 管理员管理 API ----------

@app.route('/api/admin/admins', methods=['GET'])
@login_required
def get_admins():
    """获取管理员列表"""
    db = SessionLocal()
    try:
        admins = db.query(Admin).order_by(Admin.created_at.desc()).all()
        return jsonify({'success': True, 'admins': [a.to_dict() for a in admins]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/admins', methods=['POST'])
@login_required
def create_admin():
    """创建管理员"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    nickname = data.get('nickname', '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    db = SessionLocal()
    try:
        existing = db.query(Admin).filter(Admin.username == username).first()
        if existing:
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        
        admin = Admin(username=username, password=password, nickname=nickname or username)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        return jsonify({'success': True, 'admin': admin.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/admins/<int:admin_id>', methods=['DELETE'])
@login_required
def delete_admin(admin_id):
    """删除管理员"""
    if admin_id == current_user.id:
        return jsonify({'success': False, 'message': '不能删除当前登录的管理员'}), 400
    
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            return jsonify({'success': False, 'message': '管理员不存在'}), 404
        
        db.delete(admin)
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

# ---------- 题目管理 API ----------

@app.route('/api/admin/questions', methods=['GET'])
@login_required
def admin_get_questions():
    """获取所有题目 (管理后台)"""
    db = SessionLocal()
    try:
        questions = db.query(Question).order_by(Question.created_at.desc()).all()
        return jsonify({'success': True, 'questions': [q.to_dict() for q in questions]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/question', methods=['POST'])
@login_required
def admin_create_question():
    """创建题目"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    db = SessionLocal()
    try:
        question = Question(
            title=data.get('title'),
            material=data.get('material'),
            requirement=data.get('requirement'),
            score=data.get('score', 15),
            status=data.get('status', 'active')
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        return jsonify({'success': True, 'question': question.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/question/<int:question_id>', methods=['PUT'])
@login_required
def admin_update_question(question_id):
    """更新题目"""
    data = request.json
    db = SessionLocal()
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return jsonify({'success': False, 'message': '题目不存在'}), 404
        
        question.title = data.get('title', question.title)
        question.material = data.get('material', question.material)
        question.requirement = data.get('requirement', question.requirement)
        question.score = data.get('score', question.score)
        question.status = data.get('status', question.status)
        question.answer_image = data.get('answer_image', question.answer_image)
        
        db.commit()
        return jsonify({'success': True, 'question': question.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/upload-answer-image/<int:question_id>', methods=['POST'])
@login_required
def admin_upload_answer_image(question_id):
    """上传答案图片"""
    db = SessionLocal()
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return jsonify({'success': False, 'message': '题目不存在'}), 404
        
        data = request.json
        image_data = data.get('image')  # base64 格式的图片数据
        
        if not image_data:
            return jsonify({'success': False, 'message': '图片数据不能为空'}), 400
        
        # 解析 base64 图片
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'success': False, 'message': '图片格式错误'}), 400
        
        # 生成文件名
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存图片
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # 生成访问 URL
        image_url = f"/api/uploads/{filename}"
        
        # 更新题目
        question.answer_image = image_url
        db.commit()
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'question': question.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    """提供上传文件访问"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/admin/answer', methods=['POST'])
@login_required
def admin_create_answer():
    """创建/更新答案"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    question_id = data.get('question_id')
    version = data.get('version')
    content = data.get('content')
    source = data.get('source', '')  # 答案来源：上岸仓、粉笔
    
    if not question_id or not version or not content:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    
    db = SessionLocal()
    try:
        # 检查是否已存在该版本答案
        existing = db.query(Answer).filter(
            Answer.question_id == question_id,
            Answer.version == version
        ).first()
        
        if existing:
            existing.content = content
            existing.source = source
            db.commit()
            return jsonify({'success': True, 'answer': existing.to_dict()})
        else:
            answer = Answer(question_id=question_id, version=version, content=content, source=source)
            db.add(answer)
            db.commit()
            db.refresh(answer)
            return jsonify({'success': True, 'answer': answer.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/review/<int:question_id>', methods=['GET'])
@login_required
def admin_get_reviews(question_id):
    """获取题目的批改详情"""
    db = SessionLocal()
    try:
        reviews = db.query(AnswerReview).filter(AnswerReview.question_id == question_id).all()
        return jsonify({
            'success': True,
            'reviews': [r.to_dict() for r in reviews]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/review', methods=['POST'])
@login_required
def admin_create_review():
    """创建/更新批改详情（新版）"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '数据不能为空'}), 400
    
    question_id = data.get('question_id')
    answer_version = data.get('answer_version')
    
    if not question_id or not answer_version:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    
    db = SessionLocal()
    try:
        # 检查是否已存在
        existing = db.query(AnswerReview).filter(
            AnswerReview.question_id == question_id,
            AnswerReview.answer_version == answer_version
        ).first()
        
        if existing:
            # 更新现有批改
            existing.question_total_score = data.get('question_total_score', existing.question_total_score)
            existing.answer_total_score = data.get('answer_total_score', existing.answer_total_score)
            existing.key_points_stats = data.get('key_points_stats', existing.key_points_stats)
            existing.performance_summary = data.get('performance_summary', existing.performance_summary)
            existing.next_steps = data.get('next_steps', existing.next_steps)
            existing.missing_points = data.get('missing_points', existing.missing_points)
            existing.partial_points = data.get('partial_points', existing.partial_points)
            existing.logic_analysis = data.get('logic_analysis', existing.logic_analysis)
            db.commit()
            return jsonify({'success': True, 'review': existing.to_dict()})
        else:
            # 创建新批改
            review = AnswerReview(
                question_id=question_id,
                answer_version=answer_version,
                question_total_score=data.get('question_total_score', 15),
                answer_total_score=data.get('answer_total_score', 0),
                key_points_stats=data.get('key_points_stats', {
                    "total": 0,
                    "point_score": 0,
                    "fully_scored": 0,
                    "partially_scored": 0,
                    "missing": 0
                }),
                performance_summary=data.get('performance_summary', ''),
                next_steps=data.get('next_steps', ''),
                missing_points=data.get('missing_points', []),
                partial_points=data.get('partial_points', []),
                logic_analysis=data.get('logic_analysis', '')
            )
            db.add(review)
            db.commit()
            db.refresh(review)
            return jsonify({'success': True, 'review': review.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/feedbacks', methods=['GET'])
@login_required
def admin_get_feedbacks():
    """获取所有反馈"""
    db = SessionLocal()
    try:
        feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(100).all()
        return jsonify({'success': True, 'feedbacks': [f.to_dict() for f in feedbacks]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/stats', methods=['GET'])
@login_required
def admin_get_stats():
    """获取统计数据"""
    db = SessionLocal()
    try:
        total_feedbacks = db.query(Feedback).count()
        prefer_a = db.query(Feedback).filter(Feedback.prefer == 'A').count()
        prefer_b = db.query(Feedback).filter(Feedback.prefer == 'B').count()
        total_users = db.query(User).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_feedbacks': total_feedbacks,
                'prefer_a': prefer_a,
                'prefer_b': prefer_b,
                'total_users': total_users,
                'prefer_a_rate': round(prefer_a / total_feedbacks * 100, 2) if total_feedbacks > 0 else 0,
                'prefer_b_rate': round(prefer_b / total_feedbacks * 100, 2) if total_feedbacks > 0 else 0
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/stats/trend', methods=['GET'])
@login_required
def admin_get_stats_trend():
    """获取近 7 天反馈趋势"""
    from datetime import datetime, timedelta
    
    # 获取题目筛选参数
    question_id = request.args.get('question_id', 'all')
    
    db = SessionLocal()
    try:
        # 获取近 7 天的日期范围
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        # 基础查询构建（带题目筛选）
        def get_feedback_query():
            query = db.query(Feedback)
            if question_id != 'all':
                query = query.filter(Feedback.question_id == int(question_id))
            return query
        
        # 统计每天的反馈数量
        trend_data = []
        for date_str in dates:
            start_date = f"{date_str} 00:00:00"
            end_date = f"{date_str} 23:59:59"
            count = get_feedback_query().filter(
                Feedback.created_at >= start_date,
                Feedback.created_at <= end_date
            ).count()
            
            # 统计偏好 A 和 B 的数量
            prefer_a = get_feedback_query().filter(
                Feedback.created_at >= start_date,
                Feedback.created_at <= end_date,
                Feedback.prefer == 'A'
            ).count()
            prefer_b = get_feedback_query().filter(
                Feedback.created_at >= start_date,
                Feedback.created_at <= end_date,
                Feedback.prefer == 'B'
            ).count()
            
            trend_data.append({
                'date': date_str,
                'label': f"{int(date_str[5:7])}/{int(date_str[8:10])}",
                'count': count,
                'prefer_a': prefer_a,
                'prefer_b': prefer_b
            })
        
        return jsonify({
            'success': True,
            'trend': trend_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@app.route('/api/admin/stats/detailed', methods=['GET'])
@login_required
def admin_get_detailed_stats():
    """获取详细统计数据（包含答案来源、批改来源、参与意愿等）"""
    from datetime import datetime, timedelta
    import traceback
    
    # 获取题目筛选参数
    question_id = request.args.get('question_id', 'all')
    
    db = SessionLocal()
    try:
        today = datetime.now().date()
        today_start = f"{today} 00:00:00"
        today_end = f"{today} 23:59:59"
        
        print(f"[Stats] 统计日期范围: {today_start} ~ {today_end}, 题目筛选: {question_id}")
        
        # ========== 基础查询构建（带题目筛选）==========
        def get_feedback_query():
            query = db.query(Feedback)
            if question_id != 'all':
                query = query.filter(Feedback.question_id == int(question_id))
            return query
        
        # ========== 1. 答案来源倾向统计 ==========
        answer_source_stats = {
            'total': {'上岸仓': 0, '粉笔': 0, 'unknown': 0},
            'today': {'上岸仓': 0, '粉笔': 0, 'unknown': 0}
        }
        
        # 获取反馈（带题目筛选）
        feedback_query = get_feedback_query()
        all_feedbacks = feedback_query.all()
        print(f"[Stats] 总反馈数: {len(all_feedbacks)}")
        
        for feedback in all_feedbacks:
            # 查找对应的答案
            answer = db.query(Answer).filter(
                Answer.question_id == feedback.question_id,
                Answer.version == feedback.prefer
            ).first()
            
            source = answer.source if answer and answer.source else 'unknown'
            
            if source in answer_source_stats['total']:
                answer_source_stats['total'][source] += 1
            
            # 今日统计
            feedback_time = feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
            if today_start <= feedback_time <= today_end:
                if source in answer_source_stats['today']:
                    answer_source_stats['today'][source] += 1
        
        # ========== 2. 批改来源倾向统计（A=上岸仓, B=粉笔） ==========
        review_source_stats = {
            'total': {'上岸仓': 0, '粉笔': 0},
            'today': {'上岸仓': 0, '粉笔': 0}
        }
        
        # A = 上岸仓
        review_source_stats['total']['上岸仓'] = get_feedback_query().filter(Feedback.prefer == 'A').count()
        review_source_stats['today']['上岸仓'] = get_feedback_query().filter(
            Feedback.prefer == 'A',
            Feedback.created_at >= today_start,
            Feedback.created_at <= today_end
        ).count()
        
        # B = 粉笔
        review_source_stats['total']['粉笔'] = get_feedback_query().filter(Feedback.prefer == 'B').count()
        review_source_stats['today']['粉笔'] = get_feedback_query().filter(
            Feedback.prefer == 'B',
            Feedback.created_at >= today_start,
            Feedback.created_at <= today_end
        ).count()
        
        print(f"[Stats] 批改来源统计: {review_source_stats}")
        
        # ========== 3. 参与意愿统计 ==========
        willingness_stats = {
            'total': {'很想体验': 0, '愿意尝试': 0, '没兴趣': 0},
            'today': {'很想体验': 0, '愿意尝试': 0, '没兴趣': 0}
        }
        
        for mood in ['很想体验', '愿意尝试', '没兴趣']:
            willingness_stats['total'][mood] = get_feedback_query().filter(
                Feedback.willing_to_train == mood
            ).count()
            willingness_stats['today'][mood] = get_feedback_query().filter(
                Feedback.willing_to_train == mood,
                Feedback.created_at >= today_start,
                Feedback.created_at <= today_end
            ).count()
        
        print(f"[Stats] 参与意愿统计: {willingness_stats}")
        
        # ========== 4. 参与意愿按分数段统计 ==========
        willingness_by_score = {
            'below_55': {'label': '55分以下', '很想体验': 0, '愿意尝试': 0, '没兴趣': 0},
            'above_55': {'label': '55分以上', '很想体验': 0, '愿意尝试': 0, '没兴趣': 0}
        }
        
        print(f"[Stats] 开始按分数段统计...")
        
        # 获取所有用户（分数段统计不受题目筛选影响，因为用户可能有多个题目的反馈）
        all_users = db.query(User).all()
        print(f"[Stats] 总用户数: {len(all_users)}")
        
        for user in all_users:
            # 解析用户分数
            try:
                user_score = float(user.score)
                if user_score < 55:
                    score_range = 'below_55'
                else:
                    score_range = 'above_55'
            except Exception as e:
                continue
            
            # 统计该用户的反馈意愿（带题目筛选）
            user_feedback_query = get_feedback_query().filter(Feedback.user_id == user.id)
            user_feedbacks = user_feedback_query.all()
            
            for feedback in user_feedbacks:
                mood = feedback.willing_to_train or '没兴趣'
                if mood in willingness_by_score[score_range]:
                    willingness_by_score[score_range][mood] += 1
        
        print(f"[Stats] 分数段统计结果: {willingness_by_score}")
        
        # ========== 5. 关键指标统计 ==========
        total_feedbacks = get_feedback_query().count()
        today_feedbacks = get_feedback_query().filter(
            Feedback.created_at >= today_start,
            Feedback.created_at <= today_end
        ).count()
        
        # 倾向于AI答案（上岸仓答案 = 答案A）
        prefer_ai_total = answer_source_stats['total']['上岸仓']
        prefer_ai_today = answer_source_stats['today']['上岸仓']
        
        # 倾向于上岸仓批改（批改A）
        prefer_a_review_total = review_source_stats['total']['上岸仓']
        prefer_a_review_today = review_source_stats['today']['上岸仓']
        
        # 很想+愿意体验
        willing_total = willingness_stats['total']['很想体验'] + willingness_stats['total']['愿意尝试']
        willing_today = willingness_stats['today']['很想体验'] + willingness_stats['today']['愿意尝试']
        
        result = {
            'success': True,
            'stats': {
                # 关键指标
                'summary': {
                    'total_feedbacks': total_feedbacks,
                    'today_feedbacks': today_feedbacks,
                    'prefer_ai_answer': {'total': prefer_ai_total, 'today': prefer_ai_today},
                    'prefer_shangancang_review': {'total': prefer_a_review_total, 'today': prefer_a_review_today},
                    'willing_to_experience': {'total': willing_total, 'today': willing_today}
                },
                # 答案来源分布
                'answer_source': answer_source_stats,
                # 批改来源分布
                'review_source': review_source_stats,
                # 参与意愿分布
                'willingness': willingness_stats,
                # 按分数段的参与意愿
                'willingness_by_score': willingness_by_score
            }
        }
        
        print(f"[Stats] 返回结果: 题目={question_id}, 反馈数={total_feedbacks}")
        return jsonify(result)
        
    except Exception as e:
        print(f"[Stats] 错误: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@app.route('/api/admin/debug/feedbacks', methods=['GET'])
@login_required
def admin_debug_feedbacks():
    """调试接口：查看所有反馈数据"""
    db = SessionLocal()
    try:
        feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(10).all()
        result = []
        for f in feedbacks:
            # 查找对应的答案来源
            answer = db.query(Answer).filter(
                Answer.question_id == f.question_id,
                Answer.version == f.prefer
            ).first()
            
            user = db.query(User).filter(User.id == f.user_id).first()
            
            result.append({
                'feedback_id': f.id,
                'user_id': f.user_id,
                'user_score': user.score if user else None,
                'question_id': f.question_id,
                'prefer': f.prefer,
                'willing_to_train': f.willing_to_train,
                'answer_source': answer.source if answer else None,
                'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'feedbacks': result
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


@app.route('/api/admin/users', methods=['GET'])
@login_required
def admin_get_users():
    """获取所有用户列表（管理后台）"""
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        
        # 统计每个用户的反馈数
        users_with_feedback_count = []
        for user in users:
            feedback_count = db.query(Feedback).filter(Feedback.user_id == user.id).count()
            user_dict = user.to_dict()
            user_dict['feedback_count'] = feedback_count
            users_with_feedback_count.append(user_dict)
        
        return jsonify({
            'success': True,
            'users': users_with_feedback_count
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
