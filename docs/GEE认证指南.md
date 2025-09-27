# Google Earth Engine 认证配置指南

## 概述

本指南将帮助您配置Google Earth Engine (GEE)非商用账号，以便在数据中心选址系统中使用真实的卫星数据。

## 前置条件

1. **Google账号**: 需要一个Google账号
2. **GEE账号**: 已注册Google Earth Engine非商用账号
3. **网络连接**: 能够访问Google服务
4. **Python环境**: 已安装Python 3.8+

## 快速配置

### 方法1: 使用自动配置脚本（推荐）

```bash
# 运行认证配置脚本
python setup_gee_auth.py
```

脚本会自动：
1. 检查当前GEE状态
2. 打开浏览器进行认证
3. 完成初始化配置
4. 测试连接

### 方法2: 手动配置

#### 步骤1: 安装GEE Python API

```bash
pip install earthengine-api
```

#### 步骤2: 启动认证流程

```python
import ee

# 启动认证（会打开浏览器）
ee.Authenticate()

# 初始化GEE
ee.Initialize()
```

#### 步骤3: 测试连接

```python
# 测试基本功能
point = ee.Geometry.Point([116.4074, 39.9042])  # 北京坐标
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(point).limit(1)
image = collection.first()
print(image.getInfo())
```

## 详细配置步骤

### 1. 注册GEE账号

1. 访问 [Google Earth Engine](https://earthengine.google.com/)
2. 点击 "Sign up for Earth Engine"
3. 使用Google账号登录
4. 选择 "Non-commercial use"（非商用）
5. 填写申请表格
6. 等待审核通过（通常1-2个工作日）

### 2. 认证配置

#### 浏览器认证流程

1. **运行认证命令**:
   ```python
   import ee
   ee.Authenticate()
   ```

2. **浏览器会自动打开**，显示认证页面

3. **选择Google账号**（确保是已注册GEE的账号）

4. **授权应用访问**:
   - 点击 "Allow"
   - 复制生成的认证令牌

5. **粘贴令牌**到命令行

6. **完成认证**

#### 认证文件位置

认证完成后，会在以下位置创建认证文件：

- **Windows**: `C:\Users\用户名\.config\earthengine\credentials`
- **Linux/Mac**: `~/.config/earthengine/credentials`

### 3. 初始化GEE

```python
import ee

try:
    ee.Initialize()
    print("GEE初始化成功！")
except Exception as e:
    print(f"初始化失败: {e}")
```

### 4. 测试数据访问

```python
# 测试Landsat数据访问
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
print(f"Landsat图像数量: {collection.size().getInfo()}")

# 测试特定区域数据
point = ee.Geometry.Point([116.4074, 39.9042])  # 北京
image = collection.filterBounds(point).first()
print(f"图像ID: {image.getInfo()['id']}")
```

## 常见问题解决

### 问题1: 认证失败

**错误信息**: `Authentication failed`

**解决方案**:
1. 确保已注册GEE账号
2. 检查网络连接
3. 清除浏览器缓存
4. 重新运行认证流程

### 问题2: 配额超限

**错误信息**: `Quota exceeded`

**解决方案**:
1. 非商用账号有使用限制
2. 等待配额重置（通常24小时）
3. 优化查询减少数据量
4. 考虑升级到商用账号

### 问题3: 网络连接问题

**错误信息**: `Connection timeout`

**解决方案**:
1. 检查网络连接
2. 使用VPN（如果在某些地区）
3. 检查防火墙设置
4. 尝试不同的网络环境

### 问题4: 权限不足

**错误信息**: `Permission denied`

**解决方案**:
1. 确保账号已通过GEE审核
2. 检查账号状态
3. 联系GEE支持团队

## 使用限制

### 非商用账号限制

1. **数据量限制**: 每月有数据下载限制
2. **计算限制**: 有计算配额限制
3. **存储限制**: 有存储空间限制
4. **API调用限制**: 有API调用频率限制

### 优化建议

1. **缓存结果**: 避免重复查询相同数据
2. **批量处理**: 合并多个查询请求
3. **数据压缩**: 使用适当的数据格式
4. **错误处理**: 实现重试机制

## 验证配置

运行以下代码验证配置是否正确：

```python
import ee

def verify_gee_setup():
    """验证GEE配置"""
    try:
        # 初始化
        ee.Initialize()
        print("✅ GEE初始化成功")
        
        # 测试数据访问
        point = ee.Geometry.Point([116.4074, 39.9042])
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        image = collection.filterBounds(point).first()
        
        if image:
            info = image.getInfo()
            print(f"✅ 数据访问成功")
            print(f"   图像ID: {info.get('id')}")
            print(f"   获取日期: {info.get('properties', {}).get('DATE_ACQUIRED')}")
            return True
        else:
            print("❌ 无法获取数据")
            return False
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

# 运行验证
if verify_gee_setup():
    print("\n🎉 GEE配置验证成功！可以开始使用数据中心选址系统。")
else:
    print("\n❌ GEE配置验证失败，请检查配置。")
```

## 启动系统

配置完成后，启动数据中心选址系统：

```bash
# 启动后端服务
python backend/main.py

# 启动前端服务（新终端）
cd frontend
npm start
```

访问 `http://localhost:3000` 开始使用系统。

## 技术支持

如果遇到问题：

1. 查看GEE官方文档
2. 检查GEE状态页面
3. 联系GEE支持团队
4. 查看项目GitHub Issues

## 更新日志

- **v1.0**: 初始版本，支持非商用GEE账号认证
- **v1.1**: 添加自动配置脚本
- **v1.2**: 优化错误处理和用户提示
