# 快速部署指南

## 第一步：安装 Python 依赖

```bash
cd shenlun-feedback-system
pip install -r requirements.txt
```

## 第二步：配置 MySQL

### 2.1 修改数据库配置

编辑 `backend/config.py`：

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的 MySQL 密码',  # ← 修改这里
    'database': 'shenlun_feedback'
}
```

### 2.2 创建数据库

方法一：使用 MySQL 命令行
```bash
mysql -u root -p
```
```sql
CREATE DATABASE shenlun_feedback CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

方法二：运行初始化脚本
```bash
mysql -u root -p < init_db.sql
```

### 2.3 初始化数据表

```bash
cd backend
python models.py
```

看到 "数据库表创建成功！" 即可。

## 第三步：启动服务

### Windows
双击 `start.bat` 或运行：
```bash
cd backend
python app.py
```

### Mac/Linux
```bash
cd backend
python app.py
```

## 第四步：访问系统

- **主页面**: http://localhost:5000
- **管理后台**: http://localhost:5000/admin

## 第五步：添加测试数据

1. 访问管理后台 http://localhost:5000/admin
2. 点击"添加题目"标签
3. 填写题目信息并创建
4. 点击题目列表中的"编辑答案"按钮
5. 分别添加答案 A 和答案 B

## 常见问题

### Q: 提示 "No module named 'flask'"
A: 运行 `pip install -r requirements.txt`

### Q: 数据库连接失败
A: 检查 `config.py` 中的密码是否正确，MySQL 服务是否启动

### Q: 端口 5000 被占用
A: 编辑 `app.py`，修改 `app.run()` 中的 port 参数

### Q: 中文显示乱码
A: 确保数据库使用 utf8mb4 编码，检查 `init_db.sql` 中的字符集设置
