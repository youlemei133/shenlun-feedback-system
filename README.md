# 申论判官反馈系统

收集用户对 AI 批改答案的反馈，帮助优化产品方向。

## 📁 项目结构

```
shenlun-feedback-system/
├── backend/
│   ├── app.py              # Flask 主应用
│   ├── config.py           # 配置文件
│   ├── models.py           # 数据库模型
│   ── uploads/            # 上传文件目录
├── frontend/
│   ├── index.html          # 主页面（批改对比）
│   ├── register.html       # 用户注册页面
│   ├── admin.html          # 管理后台
│   ├── css/                # 样式文件
│   ├── js/                 # JavaScript 文件
│   └── components/         # Vue 组件（预留）
── requirements.txt        # Python 依赖
└── README.md              # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd shenlun-feedback-system
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `backend/config.py`，修改 MySQL 配置：

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',  # 修改为你的密码
    'database': 'shenlun_feedback'
}
```

### 3. 创建数据库

```sql
CREATE DATABASE shenlun_feedback CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库表

```bash
cd backend
python models.py
```

### 5. 启动服务

```bash
cd backend
python app.py
```

访问：
- **主页面**: http://localhost:5000
- **管理后台**: http://localhost:5000/admin

## 📱 页面说明

### 用户注册页 (`/register`)
- 收集用户昵称、手机号、申论分数
- 注册后自动跳转到主页面

### 主页面 (`/`)
- 显示随机题目和两个版本的答案（A/B）
- 用户选择更认可的答案
- 填写反馈原因和参与意愿

### 管理后台 (`/admin`)
- **统计概览**: 总反馈数、偏好分布、用户数
- **题目管理**: 添加/编辑题目和答案
- **反馈数据**: 查看所有用户反馈

##  API 接口

### 用户相关
- `POST /api/register` - 用户注册

### 题目相关
- `GET /api/questions/active` - 获取激活的题目列表
- `GET /api/question/<id>` - 获取单个题目及答案

### 反馈相关
- `POST /api/feedback` - 提交用户反馈

### 管理后台
- `GET /api/admin/questions` - 获取所有题目
- `POST /api/admin/question` - 创建题目
- `PUT /api/admin/question/<id>` - 更新题目
- `POST /api/admin/answer` - 创建/更新答案
- `GET /api/admin/feedbacks` - 获取反馈列表
- `GET /api/admin/stats` - 获取统计数据

##  数据库表结构

### users (用户表)
- id, nickname, phone, score, created_at

### questions (题目表)
- id, title, material, requirement, score, status, created_at, updated_at

### answers (答案表)
- id, question_id, version, content, created_at

### feedbacks (反馈表)
- id, user_id, question_id, prefer, reasons, other_reason, willing_to_train, ip_address, created_at

## 🎯 使用流程

1. **管理员**在后台添加题目和答案（A/B 两个版本）
2. **用户**访问主页，注册后开始评判
3. 用户选择更认可的答案并填写反馈
4. **管理员**在后台查看统计数据，分析产品方向

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **后端**: Python Flask
- **数据库**: MySQL + SQLAlchemy
- **部署**: 本地运行 / 云服务器

## 📝 注意事项

1. 首次使用前请确保 MySQL 服务已启动
2. 管理后台没有登录验证，部署到公网时需添加认证
3. 建议定期备份数据库
4. 生产环境请关闭 Flask debug 模式

## 🔄 后续优化

- [ ] 添加管理后台登录认证
- [ ] 支持题目批量导入
- [ ] 添加数据导出功能
- [ ] 优化移动端体验
- [ ] 添加更多统计图表
