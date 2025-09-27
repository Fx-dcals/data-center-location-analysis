# 数据中心智能选址与能源优化系统

基于Google Earth Engine卫星图像和AI的数据中心选址分析系统，集成了PROMETHEE-MCGP决策方法。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- **Google Earth Engine账号（必需）**

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/data-center-location-analysis.git
cd data-center-location-analysis
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **安装前端依赖**
```bash
cd frontend
npm install
npm run build
cd ..
```

4. **配置GEE（必需）**
```bash
python setup_gee_auth.py
```

5. **启动系统**
```bash
python start_system.py
```

6. **访问系统**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📊 功能特性

- 🌍 **GEE卫星图像分析** - 基于Google Earth Engine高分辨率卫星数据
- 🏗️ **土地利用分析** - 智能空地识别和土地适宜性评估
- ⚡ **供电方案分析** - 太阳能、风能、水电等可再生能源评估
- 🔋 **储能布局分析** - 多种储能技术方案优化
- 🔥 **余热利用方案** - 北方供热、南方工业用热
- 📈 **PROMETHEE-MCGP决策** - 科学的多准则决策分析

## 🔧 配置说明

### GEE配置（必需）
⚠️ **重要：本系统必须使用GEE数据！**

1. 访问 https://earthengine.google.com/
2. 注册Google账号并申请GEE访问权限
3. 创建Google Cloud项目
4. 启用Earth Engine API
5. 运行 `python setup_gee_auth.py` 完成认证

### 环境变量
创建 `.env` 文件（可选）：
```
GEE_PROJECT_ID=your-project-id
GEE_SERVICE_ACCOUNT=your-service-account
```

## 📚 使用指南

1. 输入经纬度坐标或选择城市
2. 系统自动分析：
   - 土地利用情况
   - 能源资源评估
   - 供电方案建议
   - 储能布局分析
   - 余热利用方案
   - 综合决策评分

## 🛠️ 开发说明

### 项目结构
```
├── backend/                 # 后端API服务
│   ├── services/           # 分析服务模块
│   └── main.py            # FastAPI应用
├── frontend/              # 前端React应用
│   ├── src/               # 源代码
│   └── build/             # 构建文件
└── docs/                  # 文档
```

### API接口
- `POST /analyze/location` - 位置分析
- `POST /analyze/cities` - 城市对比分析
- `GET /satellite/image/{lat}/{lon}` - 获取卫星图像

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题，请提交Issue或联系开发者。
