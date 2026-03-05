#!/usr/bin/env python
"""
快速重置管理员密码脚本
使用方法: python reset_admin_password.py
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricultural_platform.settings')

try:
    django.setup()
except Exception as e:
    print(f"Django设置失败: {e}")
    print("请确保在项目根目录执行此脚本")
    sys.exit(1)

from django.contrib.auth.models import User

def reset_password():
    print("=" * 60)
    print("Django Admin 密码重置工具")
    print("=" * 60)
    
    # 查找所有超级用户
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        print("\n没有找到超级用户，正在创建新用户...")
        try:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456'
            )
            print("\n✓ 已创建新超级用户:")
            print("  用户名: admin")
            print("  邮箱: admin@example.com")
            print("  密码: admin123456")
            print("\n⚠️  请尽快登录后修改密码！")
            print("\n登录地址: http://localhost:8000/admin/")
            return
        except Exception as e:
            print(f"\n✗ 创建用户失败: {e}")
            return
    
    print(f"\n找到 {superusers.count()} 个超级用户:\n")
    user_list = list(superusers)
    for i, user in enumerate(user_list, 1):
        print(f"{i}. 用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   最后登录: {user.last_login or '从未登录'}")
        print()
    
    if len(user_list) == 1:
        user = user_list[0]
        print(f"正在重置用户 '{user.username}' 的密码...")
        new_password = 'admin123456'
        user.set_password(new_password)
        user.save()
        print(f"\n✓ 密码重置成功！")
        print(f"  用户名: {user.username}")
        print(f"  新密码: {new_password}")
        print("\n⚠️  请尽快登录后修改密码！")
        print("\n登录地址: http://localhost:8000/admin/")
    else:
        print("请选择要重置的用户（输入序号，或按回车重置第一个）:")
        try:
            choice = input("> ").strip()
            if not choice:
                index = 0
            else:
                index = int(choice) - 1
            
            if 0 <= index < len(user_list):
                user = user_list[index]
                print(f"\n正在重置用户 '{user.username}' 的密码...")
                new_password = 'admin123456'
                user.set_password(new_password)
                user.save()
                print(f"\n✓ 密码重置成功！")
                print(f"  用户名: {user.username}")
                print(f"  新密码: {new_password}")
                print("\n⚠️  请尽快登录后修改密码！")
                print("\n登录地址: http://localhost:8000/admin/")
            else:
                print("✗ 无效的选择")
        except ValueError:
            print("✗ 请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n操作已取消")

if __name__ == '__main__':
    try:
        reset_password()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()

