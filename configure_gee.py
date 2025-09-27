#!/usr/bin/env python3
"""
Google Earth Engine 真实数据配置脚本
"""

import ee
import os

def configure_gee():
    """配置GEE使用真实数据"""
    
    print("=" * 60)
    print("Google Earth Engine 真实数据配置")
    print("=" * 60)
    
    print("\n📋 配置前准备:")
    print("1. 确保已创建Google Cloud项目")
    print("2. 确保已启用Earth Engine API")
    print("3. 确保已关联Earth Engine项目")
    
    # 获取项目ID
    project_id = input("\n请输入您的Google Cloud项目ID: ").strip()
    
    if not project_id:
        print("❌ 项目ID不能为空")
        return False
    
    try:
        print(f"\n🔄 正在使用项目ID '{project_id}' 初始化GEE...")
        
        # 初始化GEE
        ee.Initialize(project=project_id)
        print("✅ GEE初始化成功！")
        
        # 测试数据访问
        print("\n🧪 测试真实数据访问...")
        point = ee.Geometry.Point([116.4074, 39.9042])  # 北京坐标
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        image = collection.filterBounds(point).first()
        
        if image:
            info = image.getInfo()
            print("✅ 真实数据访问成功！")
            print(f"   图像ID: {info.get('id')}")
            print(f"   获取日期: {info.get('properties', {}).get('DATE_ACQUIRED')}")
            print(f"   云量: {info.get('properties', {}).get('CLOUD_COVER')}%")
            
            # 保存项目ID到配置文件
            with open('.gee_project_id', 'w') as f:
                f.write(project_id)
            print(f"\n✅ 项目ID已保存到配置文件: {project_id}")
            
            # 更新后端代码
            update_backend_code(project_id)
            
            return True
        else:
            print("❌ 无法获取图像数据")
            return False
            
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        print("\n请检查以下几点:")
        print("1. 项目ID是否正确")
        print("2. 是否已启用Earth Engine API")
        print("3. 是否已关联Earth Engine项目")
        print("4. 网络连接是否正常")
        return False

def update_backend_code(project_id):
    """更新后端代码中的项目ID"""
    try:
        # 读取后端代码
        with open('backend/services/satellite_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换项目ID
        old_init = 'ee.Initialize()'
        new_init = f'ee.Initialize(project="{project_id}")'
        
        if old_init in content:
            content = content.replace(old_init, new_init)
            
            # 写回文件
            with open('backend/services/satellite_service.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 后端代码已更新")
        else:
            print("⚠️  后端代码中未找到需要替换的内容")
            
    except Exception as e:
        print(f"⚠️  更新后端代码失败: {e}")

def test_gee_connection():
    """测试GEE连接"""
    print("\n" + "=" * 60)
    print("GEE连接测试")
    print("=" * 60)
    
    try:
        # 读取保存的项目ID
        if os.path.exists('.gee_project_id'):
            with open('.gee_project_id', 'r') as f:
                project_id = f.read().strip()
        else:
            project_id = input("请输入项目ID: ").strip()
        
        if not project_id:
            print("❌ 项目ID不能为空")
            return False
        
        # 初始化GEE
        ee.Initialize(project=project_id)
        print("✅ GEE初始化成功")
        
        # 测试不同地区的数据
        test_locations = [
            ("北京", [116.4074, 39.9042]),
            ("深圳", [114.0579, 22.5431]),
            ("兰州", [103.8343, 36.0611])
        ]
        
        for city_name, coords in test_locations:
            print(f"\n📍 测试 {city_name} 地区数据...")
            point = ee.Geometry.Point(coords)
            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
            image = collection.filterBounds(point).first()
            
            if image:
                info = image.getInfo()
                print(f"   ✅ 成功获取数据")
                print(f"   图像ID: {info.get('id')}")
                print(f"   获取日期: {info.get('properties', {}).get('DATE_ACQUIRED')}")
            else:
                print(f"   ❌ 无法获取数据")
        
        print("\n🎉 GEE连接测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("Google Earth Engine 真实数据配置工具")
    print("适用于数据中心选址系统")
    
    while True:
        print("\n请选择操作:")
        print("1. 配置GEE真实数据")
        print("2. 测试GEE连接")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            if configure_gee():
                print("\n🎉 配置完成！现在可以使用真实卫星数据了。")
                print("启动系统: python backend/main.py")
            else:
                print("\n❌ 配置失败，请检查配置。")
        
        elif choice == '2':
            test_gee_connection()
        
        elif choice == '3':
            print("退出配置工具")
            break
        
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
