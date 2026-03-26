# 数据库迁移脚本 - 添加批改详情表
import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'hudawei',  # 请修改为你的 MySQL 密码
    'database': 'shenlun_feedback'
}

def migrate():
    """执行迁移"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 创建批改详情表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer_reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
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
            UNIQUE KEY unique_question_version (question_id, answer_version),
            INDEX idx_question_id (question_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        conn.commit()
        print("OK: 数据库迁移成功！")
        print("OK: 已创建 answer_reviews 表")
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR: 迁移失败：{e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate()
