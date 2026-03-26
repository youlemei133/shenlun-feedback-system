# 批改详情配置功能

## 📋 功能说明

为每个题目的答案 A/B 配置详细的批改信息，包括：
- 得分和满分
- 维度评分（要点覆盖度、逻辑结构、语言表达等）
- 亮点总结（标签 + 描述）
- 提升空间（标签 + 描述）
- 专业建议（多条）
- 参考优化范文

## 🚀 使用步骤

### 1. 执行数据库迁移

```bash
# 编辑 migrate_add_reviews.py，修改 MySQL 密码
python migrate_add_reviews.py
```

### 2. 访问配置页面

```
http://localhost:5000/review-admin
```

或从管理后台点击"📝 批改配置"按钮。

### 3. 配置批改详情

1. **选择题目**：从下拉列表选择要配置的题目
2. **切换版本**：点击"答案 A 批改"或"答案 B 批改"标签
3. **填写信息**：
   - 基本信息：得分/满分
   - 维度评分：添加/编辑评分维度
   - 亮点总结：添加标签和描述
   - 提升空间：添加标签和描述
   - 专业建议：添加多条建议
   - 参考优化：填写优化后的范文
4. **保存配置**：点击"💾 保存配置"按钮

### 4. 前端展示

用户在主页面点击"体验批改 A/B"按钮时，会动态加载配置的批改详情。

## 📊 数据结构

```json
{
  "question_id": 1,
  "answer_version": "A",
  "score": 13,
  "max_score": 15,
  "dimensions": [
    {"name": "要点覆盖度", "score": 4.5, "max": 5},
    {"name": "逻辑结构", "score": 4.5, "max": 5},
    {"name": "语言表达", "score": 4, "max": 5}
  ],
  "highlights": {
    "tags": ["要点全面", "逻辑清晰"],
    "content": "该答案紧扣材料..."
  },
  "improvements": {
    "tags": ["字数可精简"],
    "content": "第 2 点内容较为冗长..."
  },
  "suggestions": [
    "要点提炼：第 2 点可进一步精简...",
    "语言表达：获得分红建议改为...",
    "字数控制：当前 195 字...",
    "结构优化：建议调整各要点..."
  ],
  "reference_answer": "1.科学规划种植..."
}
```

## 🎨 配置页面功能

### 维度评分
- ✅ 默认 3 个维度
- ✅ 可添加/删除维度
- ✅ 每个维度包含：名称、得分、满分

### 标签管理
- ✅ 输入标签后按回车或点击"添加"
- ✅ 点击标签上的"×"删除
- ✅ 支持多个标签

### 专业建议
- ✅ 默认 1 条建议
- ✅ 可添加/删除多条
- ✅ 每条独立编辑

### 实时预览
- ✅ 点击"👁️ 预览效果"查看实际展示效果
- ✅ 在新窗口打开弹窗预览

## 📝 配置建议

### 得分设置
- 建议设置为整数或 0.5 的倍数
- 得分率建议在 70%-90% 之间

### 维度评分
- 维度名称要简洁明确
- 各维度满分建议统一为 5 分
- 得分要有区分度

### 亮点/提升标签
- 标签要简短（2-6 个字）
- 每个部分 3-5 个标签为宜
- 标签要有针对性

### 专业建议
- 建议 3-5 条
- 每条针对一个具体方面
- 建议要可操作、具体

### 参考优化
- 字数控制在题目要求范围内
- 结构清晰，分点作答
- 语言规范、精炼

## 🔧 技术实现

### 后端 API
- `GET /api/admin/review/<question_id>` - 获取批改详情
- `POST /api/admin/review` - 创建/更新批改详情

### 数据库表
```sql
CREATE TABLE answer_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT NOT NULL,
    answer_version VARCHAR(10) NOT NULL,
    score INT DEFAULT 13,
    max_score INT DEFAULT 15,
    dimensions JSON,
    highlights JSON,
    improvements JSON,
    suggestions JSON,
    reference_answer TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_question_version (question_id, answer_version)
);
```

### 前端展示
- 点击"体验批改 A/B"时动态加载
- 支持动画效果
- 数据为空时显示默认内容

## 💡 扩展建议

1. **批量导入**：支持 Excel 批量导入批改详情
2. **AI 生成**：接入 AI 自动生成批改建议
3. **版本历史**：记录批改详情的修改历史
4. **评分模板**：预设常用评分模板，快速配置
