"""数据库迁移脚本 - 为 questions 表添加 answer_image 字段"""

import sqlite3
import os
import sys

# 修复 Windows 控制台编码
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'shenlun_feedback.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(questions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'answer_image' in columns:
            print("[OK] answer_image 字段已存在")
        else:
            # 添加字段
            cursor.execute('ALTER TABLE questions ADD COLUMN answer_image TEXT')
            print("[OK] 已添加 answer_image 字段到 questions 表")
        
        # 为 feedbacks 表添加 answer_image 字段（如果不存在）
        cursor.execute("PRAGMA table_info(feedbacks)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'answer_image' in columns:
            print("[OK] answer_image 字段已存在于 feedbacks 表")
        else:
            cursor.execute('ALTER TABLE feedbacks ADD COLUMN answer_image TEXT')
            print("[OK] 已添加 answer_image 字段到 feedbacks 表")
        
        conn.commit()
        print("\n[SUCCESS] 数据库迁移完成！")
        
    except Exception as e:
        print(f"[ERROR] 迁移失败：{e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
