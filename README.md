# 申论判官反馈系统

收集用户对 AI 批改答案的反馈，帮助优化产品方向。

## 功能特性

- 用户注册与反馈收集
- A/B 答案对比评判
- 批改详情配置（要点统计、遗漏分析、提升建议）
- 管理后台认证登录
- 多管理员支持
- 数据统计与可视化图表
- 答案图片上传
- 反馈数据导出（CSV）

## 项目结构

```
shenlun-feedback-system/
├── backend/
│   ├── app.py                 # 应用入口
│   ├── config.py              # 配置文件
│   ├── models.py              # 数据库模型
│   ├── init_admin.py          # 管理员初始化脚本
│   │
│   ├── routes/                # 路由层
│   │   ├── public.py          # 公开接口
│   │   ├── auth.py            # 认证接口
│   │   ├── admin.py           # 管理后台接口
│   │   ├── admin_manage.py    # 管理员管理接口
│   │   └── upload.py          # 上传接口
│   │
│   ├── services/              # 业务逻辑层
│   │   ├── auth_service.py    # 认证服务
│   │   ├── user_service.py    # 用户服务
│   │   ├── question_service.py# 题目服务
│   │   ├── feedback_service.py# 反馈服务
│   │   └── stats_service.py   # 统计服务
│   │
│   ├── repositories/          # 数据访问层
│   │   ├── base.py            # 基础 Repository
│   │   ├── user_repo.py       # 用户数据访问
│   │   ├── admin_repo.py      # 管理员数据访问
│   │   ├── question_repo.py   # 题目/答案/批改数据访问
│   │   └── feedback_repo.py   # 反馈数据访问
│   │
│   ├── utils/                 # 工具函数
│   │   ├── response.py        # 统一响应格式
│   │   ├── db_session.py      # 数据库会话管理
│   │   ├── exceptions.py      # 异常定义
│   │   └── constants.py       # 常量定义
│   │
│   ├── uploads/               # 上传文件目录
│   └── shenlun_feedback.db    # SQLite 数据库
│
├── frontend/
│   ├── index.html             # 主页面
│   ├── admin.html             # 管理后台
│   └── review-admin.html      # 批改配置页面
│
├── requirements.txt           # Python 依赖
├── start.bat                  # Windows 启动脚本
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建管理员账号

```bash
cd backend
python init_admin.py --username admin --password your_password
```

或交互式创建：

```bash
python init_admin.py
```

### 3. 启动服务

```bash
cd backend
python app.py
```

或使用启动脚本：

```bash
start.bat
```

### 4. 访问

- **主页面**: http://localhost:5000
- **管理后台**: http://localhost:5000/admin

## 页面说明

### 主页面 (`/`)

- 用户注册弹窗（昵称、手机号、申论分数）
- 显示题目、答案对比（A/B 版本）、批改详情
- 用户选择偏好答案、填写反馈原因、参与意愿

### 管理后台 (`/admin`)

需登录后访问，功能包括：

| 模块 | 功能 |
|------|------|
| 数据看板 | 关键指标、趋势图表、题目筛选 |
| 题目管理 | 添加/编辑题目、答案、上传图片 |
| 反馈数据 | 查看用户反馈、导出 CSV |
| 用户管理 | 查看注册用户列表 |
| 统计分析 | 答案偏好分布、分数段分布 |
| 管理员管理 | 添加/删除管理员账号 |

## API 接口

### 用户相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/register` | POST | 用户注册 |

### 题目相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/questions/active` | GET | 获取激活的题目列表 |
| `/api/question/<id>` | GET | 获取单个题目及答案、批改详情 |

### 反馈相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/feedback` | POST | 提交用户反馈 |

### 管理后台（需登录）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/admin/login` | POST | 管理员登录 |
| `/api/admin/logout` | POST | 管理员登出 |
| `/api/admin/check-auth` | GET | 检查登录状态 |
| `/api/admin/questions` | GET | 获取所有题目 |
| `/api/admin/question` | POST | 创建题目 |
| `/api/admin/question/<id>` | PUT | 更新题目 |
| `/api/admin/answer` | POST | 创建/更新答案 |
| `/api/admin/review` | POST | 创建/更新批改详情 |
| `/api/admin/upload-answer-image/<id>` | POST | 上传答案图片 |
| `/api/admin/feedbacks` | GET | 获取反馈列表 |
| `/api/admin/users` | GET | 获取用户列表 |
| `/api/admin/stats` | GET | 获取统计数据 |
| `/api/admin/stats/detailed` | GET | 获取详细统计 |
| `/api/admin/stats/trend` | GET | 获取趋势数据 |
| `/api/admin/admins` | GET | 获取管理员列表 |
| `/api/admin/admins` | POST | 新增管理员 |
| `/api/admin/admins/<id>` | DELETE | 删除管理员 |

## 数据库表结构

### users (用户表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| nickname | String(50) | 昵称 |
| phone | String(20) | 手机号（唯一） |
| score | String(10) | 申论分数 |
| created_at | DateTime | 创建时间 |

### admins (管理员表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名（唯一） |
| password | String(100) | 密码 |
| nickname | String(50) | 昵称 |
| created_at | DateTime | 创建时间 |

### questions (题目表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String(200) | 题目名称 |
| material | Text | 给定资料 |
| requirement | Text | 作答要求 |
| score | Integer | 分值 |
| status | String(20) | 状态（active/inactive） |
| answer_image | Text | 用户作答图片 URL |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### answers (答案表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| question_id | Integer | 关联题目 ID |
| version | String(10) | 版本（A/B） |
| content | Text | 答案内容 |
| source | String(50) | 来源（上岸仓/粉笔） |
| created_at | DateTime | 创建时间 |

### answer_reviews (批改详情表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| question_id | Integer | 关联题目 ID |
| answer_version | String(10) | 答案版本（A/B） |
| question_total_score | Integer | 题目总分 |
| answer_total_score | Integer | 答案得分 |
| key_points_stats | JSON | 要点统计 |
| performance_summary | Text | 本次得分与表现 |
| next_steps | Text | 下一步提升方向 |
| missing_points | JSON | 遗漏要点列表 |
| partial_points | JSON | 部分得分要点列表 |
| logic_analysis | Text | 作答逻辑评价 |

### feedbacks (反馈表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户 ID |
| question_id | Integer | 题目 ID |
| prefer | String(10) | 最终偏好（A/B） |
| answer_prefer | String(10) | 答案偏好 |
| review_prefer | String(10) | 批改偏好 |
| reasons | JSON | 选择原因列表 |
| other_reason | Text | 其他原因 |
| willing_to_train | String(20) | 参与意愿 |
| ip_address | String(50) | IP 地址 |
| answer_image | Text | 用户作答图片 URL |
| created_at | DateTime | 创建时间 |

## 使用流程

1. **管理员**登录后台，添加题目、答案（A/B）、批改详情
2. **用户**访问主页，注册后查看题目并评判
3. 用户选择偏好答案、填写反馈原因和参与意愿
4. **管理员**查看统计数据，分析产品优化方向

## 技术栈

- **前端**: HTML5 + CSS3 + Vanilla JavaScript + Chart.js
- **后端**: Python Flask + Flask-Login
- **数据库**: SQLite + SQLAlchemy

## 注意事项

1. 默认管理员账号需通过 `init_admin.py` 脚本创建
2. 数据库文件 `shenlun_feedback.db` 首次运行自动创建
3. 建议定期备份数据库文件
4. 生产环境请关闭 Flask debug 模式
5. 密码明文存储，生产环境建议加密

## 管理员账号管理

```bash
# 查看所有管理员
python init_admin.py --list

# 创建管理员
python init_admin.py --username <用户名> --password <密码>

# 交互式创建
python init_admin.py
```
