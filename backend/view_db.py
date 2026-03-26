#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SQLite 数据库查看工具"""

import sqlite3
from datetime import datetime
import sys

# 修复 Windows 控制台编码
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = 'shenlun_feedback.db'

def view_table(cursor, table_name):
    """查看单个表的内容"""
    print(f"\n{'='*60}")
    print(f"📊 表：{table_name}")
    print('='*60)
    
    # 获取表结构
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    col_names = [col[1] for col in columns]
    print(f"列：{', '.join(col_names)}")
    
    # 获取数据
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️  暂无数据")
        return
    
    print(f"记录数：{len(rows)}\n")
    
    for i, row in enumerate(rows, 1):
        print(f"[{i}] ", end='')
        for j, val in enumerate(row):
            # 截断长文本
            if isinstance(val, str) and len(val) > 50:
                val = val[:50] + '...'
            print(f"{col_names[j]}={val}", end='  ')
        print()

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [t[0] for t in cursor.fetchall()]
    
    print(f"📁 数据库：{DB_PATH}")
    print(f"📊 表数量：{len(tables)}")
    print(f"📋 表列表：{', '.join(tables)}")
    
    # 查看每个表
    for table in tables:
        view_table(cursor, table)
    
    conn.close()
    print(f"\n{'='*60}")
    print("✅ 查看完成")
    print('='*60)

if __name__ == '__main__':
    main()
