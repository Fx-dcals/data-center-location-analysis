# 🚀 快速启动指南

## 📋 前置要求

- Python 3.8+
- Node.js 16+
- **Google Earth Engine账号（必需）**

## 🔧 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/data-center-location-analysis.git
cd data-center-location-analysis
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 安装前端依赖
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. 配置GEE认证
```bash
python setup_gee_auth.py
```

### 5. 启动系统
```bash
python start_system.py
```

## 🌐 访问系统

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 📚 文档说明

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `README_GitHub.md` | 项目概述和功能说明 | ⭐⭐⭐ |
| `QUICK_START.md` | 快速启动指南（本文件） | ⭐⭐⭐ |
| `requirements.txt` | Python依赖包列表 | ⭐⭐ |
| `setup_gee_auth.py` | GEE认证配置脚本 | ⭐⭐⭐ |
| `start_system.py` | 系统启动脚本 | ⭐⭐⭐ |

## ⚠️ 常见问题

### Q: GEE认证失败怎么办？
A: 请确保：
1. 已注册Google账号
2. 已申请GEE访问权限
3. 已创建Google Cloud项目
4. 已启用Earth Engine API

### Q: 依赖安装失败？
A: 请检查：
1. Python版本是否为3.8+
2. 网络连接是否正常
3. 是否使用了正确的pip版本

### Q: 前端构建失败？
A: 请检查：
1. Node.js版本是否为16+
2. 是否在frontend目录下运行npm命令
3. 网络连接是否正常

## 🆘 获取帮助

如果遇到问题，请：
1. 查看错误信息
2. 检查依赖是否正确安装
3. 确认GEE认证是否成功
4. 提交Issue到GitHub仓库

## 📞 联系方式

- GitHub Issues: 提交问题
- 开发者邮箱: your-email@example.com
