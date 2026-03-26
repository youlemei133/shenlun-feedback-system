"""修复图片 URL 路径"""

import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'shenlun_feedback.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # 更新 questions 表的图片 URL
    cursor.execute("""
        UPDATE questions 
        SET answer_image = REPLACE(answer_image, '/api/uploads/answer_images/', '/api/uploads/')
        WHERE answer_image LIKE '/api/uploads/answer_images/%'
    """)
    updated = cursor.rowcount
    print(f"[OK] 已更新 {updated} 条 questions 记录")
    
    conn.commit()
    print("\n[SUCCESS] URL 修复完成！")
    
except Exception as e:
    print(f"[ERROR] 修复失败：{e}")
    conn.rollback()
finally:
    conn.close()
