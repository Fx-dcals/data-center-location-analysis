# 🔧 详细安装指南

## 📋 系统要求

### 必需软件
- **Python 3.8+** - 后端运行环境
- **Node.js 16+** - 前端构建工具
- **Git** - 代码版本控制
- **Google Earth Engine账号** - 数据源（必需）

### 推荐软件
- **VSCode** - 代码编辑器
- **Postman** - API测试工具
- **Chrome浏览器** - 前端界面

## 🚀 安装步骤

### 第一步：克隆项目
```bash
# 克隆仓库
git clone https://github.com/yourusername/data-center-location-analysis.git

# 进入项目目录
cd data-center-location-analysis

# 查看项目结构
ls -la
```

### 第二步：安装Python依赖
```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证安装
python -c "import ee, fastapi, uvicorn; print('✅ Python依赖安装成功')"
```

### 第三步：安装前端依赖
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 构建前端
npm run build

# 返回根目录
cd ..

# 验证构建
ls frontend/build/
```

### 第四步：配置GEE认证
```bash
# 运行GEE认证脚本
python setup_gee_auth.py

# 按照提示完成认证
# 1. 访问 https://earthengine.google.com/
# 2. 登录Google账号
# 3. 接受服务条款
# 4. 完成认证
```

### 第五步：启动系统
```bash
# 启动完整系统
python start_system.py

# 或者分别启动
# 后端: python backend/main.py
# 前端: python frontend/start_server.py
```

## 🔍 验证安装

### 检查后端
```bash
# 测试后端API
curl http://localhost:8000/docs
```

### 检查前端
```bash
# 访问前端界面
# 浏览器打开: http://localhost:3000
```

### 检查GEE
```bash
# 测试GEE连接
python -c "import ee; ee.Initialize(); print('✅ GEE连接正常')"
```

## 🛠️ 开发环境设置

### VSCode配置
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/node_modules": true,
        "**/.git": true
    }
}
```

### 环境变量
创建 `.env` 文件：
```env
GEE_PROJECT_ID=your-project-id
GEE_SERVICE_ACCOUNT=your-service-account
DEBUG=True
```

## 🐛 故障排除

### 常见错误及解决方案

#### 1. GEE认证失败
```
错误: GEE认证失败
解决: 运行 python setup_gee_auth.py
```

#### 2. 依赖安装失败
```
错误: ModuleNotFoundError
解决: pip install -r requirements.txt
```

#### 3. 前端构建失败
```
错误: npm error
解决: cd frontend && npm install && npm run build
```

#### 4. 端口占用
```
错误: Address already in use
解决: 检查端口3000和8000是否被占用
```

## 📚 下一步

安装完成后，请阅读：
1. `QUICK_START.md` - 快速使用指南
2. `README_GitHub.md` - 项目功能说明
3. `backend/main.py` - API接口文档
4. `frontend/src/App_simple.tsx` - 前端界面说明
