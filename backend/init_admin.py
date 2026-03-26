#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化管理员账号脚本

使用方法:
    python init_admin.py                           # 交互式创建
    python init_admin.py --username admin --password admin123  # 命令行创建
    python init_admin.py --list                    # 列出所有管理员
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db, SessionLocal, Admin

def create_admin(username, password, nickname=None):
    """创建管理员"""
    db = SessionLocal()
    try:
        existing = db.query(Admin).filter(Admin.username == username).first()
        if existing:
            print(f"错误: 用户名 '{username}' 已存在")
            return False
        
        admin = Admin(
            username=username, 
            password=password, 
            nickname=nickname or username
        )
        db.add(admin)
        db.commit()
        print(f"成功: 管理员 '{username}' 创建成功")
        return True
    except Exception as e:
        db.rollback()
        print(f"错误: {e}")
        return False
    finally:
        db.close()

def list_admins():
    """列出所有管理员"""
    db = SessionLocal()
    try:
        admins = db.query(Admin).order_by(Admin.created_at).all()
        if not admins:
            print("暂无管理员账号")
            return
        
        print("\n管理员列表:")
        print("-" * 50)
        for admin in admins:
            print(f"  ID: {admin.id}")
            print(f"  用户名: {admin.username}")
            print(f"  昵称: {admin.nickname or '-'}")
            print(f"  创建时间: {admin.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)
    finally:
        db.close()

def interactive_create():
    """交互式创建管理员"""
    print("\n=== 创建管理员账号 ===\n")
    username = input("请输入用户名: ").strip()
    if not username:
        print("错误: 用户名不能为空")
        return
    
    password = input("请输入密码: ").strip()
    if not password:
        print("错误: 密码不能为空")
        return
    
    nickname = input("请输入昵称 (可选，直接回车跳过): ").strip()
    
    create_admin(username, password, nickname if nickname else None)

def main():
    parser = argparse.ArgumentParser(description='管理后台账号管理工具')
    parser.add_argument('--username', '-u', help='用户名')
    parser.add_argument('--password', '-p', help='密码')
    parser.add_argument('--nickname', '-n', help='昵称')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有管理员')
    
    args = parser.parse_args()
    
    init_db()
    
    if args.list:
        list_admins()
        return
    
    if args.username and args.password:
        create_admin(args.username, args.password, args.nickname)
    elif args.username or args.password:
        print("错误: 用户名和密码必须同时提供")
        sys.exit(1)
    else:
        interactive_create()

if __name__ == '__main__':
    main()
