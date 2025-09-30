# 🚀 数据中心智能选址与能源优化系统

基于Google Earth Engine (GEE)的智能数据中心选址与能源资源评估系统，集成卫星遥感数据、能源资源分析和多准则决策分析。

## ✨ 主要功能

- 🌍 **卫星图像分析** - 基于GEE的高分辨率卫星图像获取与分析
- ⚡ **能源资源评估** - 太阳能、风能、水能等可再生能源潜力评估
- 🏭 **余热利用分析** - 数据中心余热回收利用潜力分析
- 🌿 **地理环境分析** - 海拔、河流、森林、气候等地理要素分析
- 🔋 **供电方案分析** - 多种供电方案的技术经济性分析
- 💾 **储能布局分析** - 储能系统布局优化分析
- 🎯 **智能决策分析** - 基于PROMETHEE-MCGP的多准则决策分析

## 🛠️ 技术栈

### 后端
- **FastAPI** - 高性能Web框架
- **Google Earth Engine** - 卫星遥感数据处理
- **Python 3.8+** - 核心开发语言
- **Pydantic** - 数据验证
- **Uvicorn** - ASGI服务器

### 前端
- **React 18** - 用户界面框架
- **TypeScript** - 类型安全的JavaScript
- **CSS3** - 现代化样式设计

## 📋 系统要求

- Python 3.8+
- Node.js 16+
- Google Earth Engine账号（必需）
- 8GB+ RAM推荐

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/data-center-location-analysis.git
cd data-center-location-analysis
```

### 2. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 3. 配置GEE认证
```bash
python setup_gee_auth.py
```

### 4. 启动系统
```bash
python start_system.py
```

### 5. 访问系统
- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📖 详细文档

- [快速开始指南](QUICK_START.md)
- [详细安装说明](INSTALLATION.md)
- [GEE认证指南](docs/GEE认证指南.md)
- [API文档](docs/API文档.md)
- [使用指南](docs/使用指南.md)

## 🔧 配置说明

### GEE认证配置
系统必须配置Google Earth Engine认证才能正常运行：

1. 注册Google Earth Engine账号
2. 创建Google Cloud项目
3. 启用Earth Engine API
4. 运行认证脚本

详细步骤请参考 [GEE认证指南](docs/GEE认证指南.md)

### 环境变量
创建 `.env` 文件（可选）：
```env
GEE_PROJECT_ID=your-project-id
DEBUG=False
```

## 📊 系统架构

```
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI主应用
│   └── services/           # 业务服务层
│       ├── energy_assessment.py      # 能源资源评估
│       ├── satellite_service.py      # 卫星图像服务
│       ├── power_supply_analysis.py  # 供电方案分析
│       ├── energy_storage_analysis.py # 储能布局分析
│       └── promethee_mcgp_analysis.py # 决策分析
├── frontend/               # 前端应用
│   ├── src/               # React源码
│   └── build/             # 构建输出
├── docs/                  # 文档
└── notebooks/             # Jupyter示例
```

## 🌟 核心特性

### 卫星图像分析
- 基于Landsat 8/9和Sentinel-2数据
- 自动云量过滤和图像质量优化
- 多数据源备选方案
- 20公里覆盖半径

### 能源资源评估
- 太阳能辐射量计算
- 风能资源评估
- 水能潜力分析
- 可再生能源覆盖率计算

### 智能决策分析
- PROMETHEE多准则决策方法
- 经济因素分析
- 自然因素分析
- 综合评分排序
