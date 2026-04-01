# 申论判官反馈系统

收集用户对 AI 批改答案的反馈，帮助优化产品方向。

## 功能特性

### 核心功能
- 用户注册与反馈收集
- A/B 参考答案对比评判（来源可配置：上岸仓/粉笔）
- 批改详情配置（针对用户作答，分上岸仓/粉笔两种批改风格）
- 管理后台认证登录
- 多管理员支持
- 数据统计与可视化图表
- 用户作答图片上传及文字版录入
- 反馈数据导出（CSV）

### 上岸仓批改功能
- **我的作答**：高亮显示得分点，橙色文字 + 下划线 + 分数标签
- **得分卡片**：题目总分、答案得分、要点统计（完全得分/部分得分/遗漏作答）
- **整体点评**：本次得分与表现、下一步提升方向
- **详细点评**：
  - 遗漏要点列表（要点标题、原因分析、改进建议）
  - 部分得分要点列表
  - 作答逻辑评价

### 粉笔批改功能
- **折叠面板 UI**：4 个模块（我的作答、参考答案、得分分析、答题演示）
- **我的作答**：得分点高亮显示 + 优缺点诊断
- **参考答案**：展示答案 A 和答案 B
- **得分分析**：
  - 左侧虚线 + 圆点标记
  - 按维度分析得分
  - 卡片点击弹出详细分析（富文本）
  - 右下角圆形箭头图标
- **答题演示**：富文本展示答题步骤

### 管理后台功能
- **批改配置弹窗**：
  - 左右分栏布局（左侧用户作答，右侧配置项）
  - 折叠面板分组（可展开/收起）
  - 所见即所得富文本编辑器
  - 实时预览效果

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
│   ├── index.html             # 主页面（用户界面）
│   └── admin.html             # 管理后台
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
- 批改详情弹窗：
  - 上岸仓批改：加载动画 + 得分卡片 + 整体点评 + 详细点评
  - 粉笔批改：折叠面板 + 得分分析卡片点击弹窗

### 管理后台 (`/admin`)

需登录后访问，功能包括：

| 模块 | 功能 |
|------|------|
| 数据看板 | 关键指标、趋势图表、题目筛选 |
| 题目管理 | 添加/编辑题目、答案、上传图片 |
| 批改配置 | 上岸仓批改配置、粉笔批改配置（富文本编辑器） |
| 反馈数据 | 查看用户反馈、导出 CSV |
| 用户管理 | 查看注册用户列表 |
| 统计分析 | 答案偏好分布、分数段分布 |
| 管理员管理 | 添加/删除管理员账号 |

### 批改配置弹窗

**布局结构**：
- 左侧：用户作答文字版（固定显示）
- 右侧：配置项（可滚动）

**配置区域**（折叠面板）：
- 基本信息：题目总分、答案得分
- 得分点高亮：添加得分点及分数
- 优缺点诊断：富文本编辑器
- 得分分析：按维度添加分析项
- 答题演示：富文本编辑器

**富文本编辑器功能**：
| 按钮 | 功能 |
|------|------|
| **B** | 加粗 |
| *I* | 斜体 |
| <u>U</u> | 下划线 |
| •≡ | 无序列表 |
| H | 标题 |
| 🅰(橙) | 橙色加粗重点 |
| 🅰(蓝) | 蓝色加粗标注 |
| 🅰(绿) | 绿色加粗标注 |
| ✕ | 清除格式 |
| 📝 | 步骤模板（自动插入审题、找点、加工三个步骤） |

## API 接口

### 用户相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/register` | POST | 用户注册 |

### 题目相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/question/next` | GET | 获取下一个待反馈的题目 |
| `/api/question/<id>` | GET | 获取单个题目及答案、批改详情 |

### 反馈相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/feedback` | POST | 提交用户反馈 |
| `/api/stats` | GET | 获取统计数据 |

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
| `/api/admin/review/<id>` | GET | 获取批改详情 |
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
| user_answer_text | Text | 用户作答文字版 |
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
| review_style | String(20) | 批改风格（shangancang/fenbi） |
| question_total_score | Integer | 题目总分 |
| answer_total_score | Integer | 答案得分 |
| key_points_stats | JSON | 要点统计 |
| performance_summary | Text | 本次得分与表现 |
| next_steps | Text | 下一步提升方向 |
| missing_points | JSON | 遗漏要点列表 |
| partial_points | JSON | 部分得分要点列表 |
| logic_analysis | Text | 作答逻辑评价 |
| fenbi_review_data | JSON | 粉笔批改数据（得分点高亮、优缺点诊断、得分分析、答题演示） |
| shangancang_review_data | JSON | 上岸仓批改数据（得分点高亮） |
| points_description | Text | 要点描述文案 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### feedbacks (反馈表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户 ID |
| question_id | Integer | 题目 ID |
| prefer | String(10) | 最终偏好（A/B） |
| answer_prefer | String(10) | 答案偏好 |
| review_prefer | String(10) | 批改偏好（shangancang/fenbi） |
| reasons | JSON | 选择原因列表 |
| other_reason | Text | 其他原因 |
| willing_to_train | String(20) | 参与意愿 |
| ip_address | String(50) | IP 地址 |
| answer_image | Text | 用户作答图片 URL |
| created_at | DateTime | 创建时间 |

## 使用流程

### 数据配置流程

1. **管理员**登录后台，添加题目
2. 配置参考答案 A 和 B（每个答案需选择来源：上岸仓或粉笔，两者不能相同）
3. 上传用户作答图片和文字版
4. 配置批改详情：
   - **上岸仓批改**：得分点高亮、要点统计、整体点评、遗漏要点、部分得分要点、作答逻辑评价
   - **粉笔批改**：得分点高亮、优缺点诊断、得分分析（含详细分析）、答题演示

### 用户反馈流程

1. **用户**访问主页，注册后查看题目
2. 对比参考答案 A 和 B，选择更认可的答案
3. 查看两种批改风格：
   - 上岸仓批改：加载动画 → 得分卡片 → 整体点评 → 详细点评
   - 粉笔批改：折叠面板 → 我的作答/参考答案/得分分析/答题演示
4. 点击粉笔批改的得分分析卡片，查看详细分析
5. 选择更喜欢的批改风格
6. 填写反馈原因和参与意愿
7. **管理员**查看统计数据，分析产品优化方向

## 业务逻辑说明

### 数据结构

```
题目
├── 参考答案A（来源：上岸仓/粉笔，可配置）
├── 参考答案B（来源：上岸仓/粉笔，可配置，与A不同）
├── 用户作答图片（answer_image）
├── 用户作答文字版（user_answer_text）
├── 批改_上岸仓风格（针对用户作答）
│   ├── 得分点高亮
│   ├── 要点统计
│   ├── 整体点评
│   ├── 遗漏要点
│   ├── 部分得分要点
│   └── 作答逻辑评价
└── 批改_粉笔风格（针对用户作答）
    ├── 得分点高亮
    ├── 优缺点诊断（富文本）
    ├── 得分分析（含详细分析，富文本）
    └── 答题演示（富文本）
```

### 关键规则

- 参考答案 A 和 B 的来源必须不同（一个上岸仓，一个粉笔）
- 批改是针对用户作答的，不针对参考答案
- 每个题目只有 2 个批改配置：上岸仓风格、粉笔风格
- 富文本字段支持 HTML 格式（加粗、颜色、列表等）

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
6. SECRET_KEY 在 `config.py` 中配置，生产环境请使用随机值

## 管理员账号管理

```bash
# 查看所有管理员
python init_admin.py --list

# 创建管理员
python init_admin.py --username <用户名> --password <密码>

# 交互式创建
python init_admin.py
```

## 更新日志

### v1.3.0
- **视觉设计全面优化**
  - 统一配色方案：薄荷青色系（主色 `#14b8a6`，浅色背景 `#f0fdfa`）
  - 移除 AI slop 特征：渐变背景、渐变边框、渐变文字
  - 卡片风格：纯白底 + 浅灰边框，简洁克制
  - 图标背景统一为浅薄荷青
- **后台看板优化**
  - KPI 数字放大至 48px，使用 font-black 字重
  - 移除卡片顶部渐变条，改用边框区分
  - 添加入场动画（卡片依次滑入）
  - Tab 激活态改为药丸形状
- **批改弹窗优化**
  - 得分数字使用薄荷青强调
  - 时间线圆点使用薄荷青边框
  - 高亮文字使用薄荷青
  - 折叠面板箭头激活态使用薄荷青背景
- **配置弹窗优化**
  - 移除面板左侧颜色条
  - 统一配置区背景色
  - 粉笔配置工具栏颜色改为薄荷青系
- **代码质量优化**
  - 清理所有调试用 console.log 语句
  - 仅保留 console.error 用于错误处理

### v1.2.0
- 新增粉笔批改得分分析卡片点击弹窗功能
- 新增富文本详细分析内容（后台可配置）
- 优化后台批改配置界面（左右分栏、折叠面板）
- 新增所见即所得富文本编辑器

### v1.1.0
- 新增粉笔批改功能（折叠面板、得分点高亮、优缺点诊断、得分分析、答题演示）
- 新增上岸仓批改功能（我的作答高亮、得分卡片、整体点评、详细点评）
- 优化批改弹窗标题栏固定定位
- 新增得分分析左侧虚线 + 圆点标记

### v1.0.0
- 初始版本
- 用户注册与反馈收集
- A/B 参考答案对比评判
- 管理后台基础功能