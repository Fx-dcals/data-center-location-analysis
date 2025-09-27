#!/usr/bin/env python3
"""
GEE认证修复脚本
解决项目ID缺失问题
"""

import ee
import sys

def fix_gee_auth():
    """修复GEE认证"""
    print("=" * 60)
    print("🔧 GEE认证修复工具")
    print("=" * 60)
    
    # 尝试使用项目ID初始化
    try:
        print("正在尝试使用项目ID初始化GEE...")
        ee.Initialize(project='data-center-location-analysis')
        print("✅ GEE认证成功！")
        return True
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print()
        
        # 尝试认证
        try:
            print("正在尝试GEE认证...")
            ee.Authenticate()
            ee.Initialize(project='data-center-location-analysis')
            print("✅ GEE认证成功！")
            return True
        except Exception as auth_error:
            print(f"❌ 认证失败: {auth_error}")
            print()
            print("请手动完成以下步骤：")
            print("1. 访问 https://code.earthengine.google.com/")
            print("2. 登录您的Google账号")
            print("3. 接受GEE服务条款")
            print("4. 创建项目ID: data-center-location-analysis")
            print("5. 重新运行此脚本")
            return False

if __name__ == "__main__":
    success = fix_gee_auth()
    if success:
        print("\n🎉 GEE认证修复成功！现在可以启动系统了。")
        print("运行: python start_system.py")
    else:
        print("\n❌ GEE认证修复失败，请按照提示手动配置。")
        sys.exit(1)
