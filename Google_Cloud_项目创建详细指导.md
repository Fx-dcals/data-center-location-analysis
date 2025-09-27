# Google Cloud 项目创建详细指导

## 🎯 目标
创建Google Cloud项目并启用Earth Engine API，以便在数据中心选址系统中使用真实卫星数据。

## 📋 前置条件
- Google账号（已注册Earth Engine非商用账号）
- 网络连接正常
- 浏览器（推荐Chrome或Edge）

## 🚀 详细步骤

### 步骤1: 访问Google Cloud Console

1. **打开浏览器**
2. **访问**: https://console.cloud.google.com/
3. **使用Google账号登录**

**注意**: 确保使用已注册Earth Engine的Google账号

### 步骤2: 创建新项目

#### 2.1 找到项目选择器
- 在页面顶部，您会看到当前项目名称
- 点击项目名称旁边的下拉箭头

#### 2.2 点击"新建项目"
- 在弹出的菜单中，点击"新建项目"按钮
- 按钮通常是蓝色的，显示"NEW PROJECT"

#### 2.3 填写项目信息
```
项目名称: data-center-location-analysis
组织: 无组织
位置: 无组织
```

#### 2.4 创建项目
- 点击"创建"按钮
- 等待项目创建完成（通常几秒钟）

### 步骤3: 记录项目ID

项目创建完成后，您会看到：
```
项目名称: data-center-location-analysis
项目ID: data-center-location-analysis-xxxxx
```

**重要**: 请记录下项目ID，稍后配置代码时需要用到。

### 步骤4: 启用Earth Engine API

#### 4.1 导航到API库
1. 在Google Cloud Console左侧菜单中
2. 找到"API和服务"
3. 点击"库"

#### 4.2 搜索Earth Engine API
1. 在搜索框中输入: `Earth Engine API`
2. 点击搜索结果中的"Earth Engine API"

#### 4.3 启用API
1. 点击"启用"按钮
2. 等待启用完成（通常1-2分钟）
3. 看到"API已启用"的确认消息

### 步骤5: 关联Earth Engine

#### 5.1 访问Earth Engine
1. 打开新标签页
2. 访问: https://earthengine.google.com/
3. 使用相同Google账号登录

#### 5.2 选择项目
1. 在Earth Engine界面中，找到项目选择器
2. 选择您刚创建的Google Cloud项目
3. 确认关联

## 🔧 配置代码

完成上述步骤后，运行配置脚本：

```bash
python configure_gee.py
```

选择选项1，输入您的项目ID。

## 🧪 验证配置

运行测试验证配置是否正确：

```bash
python configure_gee.py
```

选择选项2进行测试。

## ❓ 常见问题

### Q1: 找不到"API和服务"菜单
**解决**: 确保已选择正确的项目，菜单在左侧导航栏中

### Q2: 搜索不到Earth Engine API
**解决**: 尝试搜索"Earth Engine"或"earthengine"

### Q3: 启用API失败
**解决**: 等待几分钟后重试，或检查网络连接

### Q4: Earth Engine无法关联项目
**解决**: 确保项目ID正确，且API已启用

## 📞 需要帮助？

如果遇到问题，请提供：
1. 当前操作步骤
2. 错误信息截图
3. 项目ID（如果已创建）

我会帮您逐步解决！
