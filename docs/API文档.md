# 数据中心智能选址与能源优化系统 API 文档

## 概述

本系统提供基于卫星图像和AI的数据中心选址分析服务，包括土地利用分析、能源资源评估、决策分析等功能。

## 基础信息

- **基础URL**: `http://localhost:8000`
- **API版本**: v1.0.0
- **数据格式**: JSON

## API 端点

### 1. 健康检查

**GET** `/health`

检查服务状态。

**响应示例:**
```json
{
  "status": "healthy"
}
```

### 2. 位置分析

**POST** `/analyze/location`

分析指定位置的数据中心选址可行性。

**请求参数:**
```json
{
  "latitude": 39.9042,
  "longitude": 116.4074,
  "radius": 1000,
  "city_name": "北京"
}
```

**参数说明:**
- `latitude`: 纬度 (必需)
- `longitude`: 经度 (必需)
- `radius`: 搜索半径，单位米 (可选，默认1000)
- `city_name`: 城市名称 (可选)

**响应示例:**
```json
{
  "location": {
    "latitude": 39.9042,
    "longitude": 116.4074
  },
  "land_analysis": {
    "total_area": 1000000,
    "land_use_distribution": {
      "水体": 0.05,
      "植被": 0.25,
      "裸地": 0.35,
      "建筑": 0.35
    },
    "suitable_areas": [
      {
        "type": "裸地",
        "area_ratio": 0.35,
        "suitability_score": 0.7
      }
    ],
    "constraints": ["建筑密度较高", "需要考虑电网负荷"],
    "recommendations": ["建议选择郊区裸地区域", "需要评估电网承载能力"]
  },
  "energy_assessment": {
    "solar_data": {
      "annual_irradiance": 1500,
      "solar_zone": "二类地区",
      "solar_potential": "中等"
    },
    "wind_data": {
      "wind_zone": "三类风区",
      "average_speed": 6.5,
      "wind_potential": "中等"
    },
    "renewable_potential": {
      "total_renewable_potential": {
        "annual_generation_mwh": 50000
      }
    },
    "storage_assessment": {
      "renewable_coverage": 0.5
    },
    "grid_assessment": {
      "available_capacity": 100,
      "voltage_level": "220kV",
      "grid_stability": "良好"
    },
    "recommendations": ["建议进行详细能源评估"]
  },
  "decision_recommendation": {
    "overall_score": {
      "score": 75,
      "level": "良好"
    },
    "detailed_scores": {
      "land_suitability": {"score": 80, "level": "良好"},
      "energy_resources": {"score": 70, "level": "良好"},
      "grid_capacity": {"score": 75, "level": "良好"},
      "economic_feasibility": {"score": 70, "level": "良好"},
      "environmental_impact": {"score": 80, "level": "良好"}
    },
    "recommendations": ["该位置适合建设数据中心"],
    "risk_assessment": {
      "risk_level": "低",
      "risks": []
    },
    "decision_level": "推荐"
  },
  "heat_utilization": {
    "recoverable_heat_mw": 60,
    "utilization_options": [
      {
        "type": "区域供热",
        "capacity_mw": 60,
        "target_users": "居民区、学校、医院",
        "economic_value": 60000000
      }
    ],
    "economic_benefits": {
      "annual_revenue": 60000000,
      "payback_period": 3,
      "co2_reduction": 262800
    },
    "recommendations": ["推荐建设区域供热系统"]
  }
}
```

### 3. 批量城市分析

**POST** `/analyze/cities`

批量分析多个城市的数据中心选址情况。

**请求参数:**
```json
{
  "cities": ["北京", "深圳", "兰州"]
}
```

**响应示例:**
```json
{
  "cities_analysis": {
    "北京": {
      // 北京分析结果，格式同单个位置分析
    },
    "深圳": {
      // 深圳分析结果，格式同单个位置分析
    },
    "兰州": {
      // 兰州分析结果，格式同单个位置分析
    }
  }
}
```

### 4. 获取卫星图像

**GET** `/satellite/image/{lat}/{lon}`

获取指定位置的卫星图像。

**路径参数:**
- `lat`: 纬度
- `lon`: 经度

**查询参数:**
- `zoom`: 缩放级别 (可选，默认15)

**响应示例:**
```json
{
  "image_url": "https://example.com/satellite-image.jpg",
  "metadata": {
    "acquisition_date": "2023-06-15",
    "cloud_cover": 5.2,
    "resolution": "medium"
  }
}
```

### 5. 获取能源资源信息

**GET** `/energy/resources/{lat}/{lon}`

获取指定位置的能源资源信息。

**路径参数:**
- `lat`: 纬度
- `lon`: 经度

**响应示例:**
```json
{
  "solar": {
    "annual_irradiance": 1500,
    "solar_zone": "二类地区",
    "solar_potential": "中等"
  },
  "wind": {
    "wind_zone": "三类风区",
    "average_speed": 6.5,
    "wind_potential": "中等"
  },
  "location": {
    "latitude": 39.9042,
    "longitude": 116.4074
  },
  "assessment_date": "2023-12-01T10:00:00"
}
```

## 错误处理

所有API端点都可能返回以下错误响应：

**400 Bad Request**
```json
{
  "detail": "请求参数错误"
}
```

**500 Internal Server Error**
```json
{
  "detail": "服务器内部错误"
}
```

## 使用示例

### Python 示例

```python
import requests

# 分析北京地区
response = requests.post('http://localhost:8000/analyze/location', json={
    "latitude": 39.9042,
    "longitude": 116.4074,
    "radius": 1000,
    "city_name": "北京"
})

if response.status_code == 200:
    analysis = response.json()
    print(f"综合评分: {analysis['decision_recommendation']['overall_score']['score']}")
    print(f"决策等级: {analysis['decision_recommendation']['decision_level']}")
else:
    print(f"分析失败: {response.status_code}")
```

### JavaScript 示例

```javascript
// 分析深圳地区
fetch('http://localhost:8000/analyze/location', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        latitude: 22.5431,
        longitude: 114.0579,
        radius: 1000,
        city_name: "深圳"
    })
})
.then(response => response.json())
.then(data => {
    console.log('综合评分:', data.decision_recommendation.overall_score.score);
    console.log('决策等级:', data.decision_recommendation.decision_level);
})
.catch(error => {
    console.error('分析失败:', error);
});
```

## 注意事项

1. 所有坐标使用WGS84坐标系
2. 距离单位统一使用米
3. 时间格式使用ISO 8601标准
4. 评分范围为0-100分
5. 建议在生产环境中使用HTTPS
6. 请合理控制API调用频率，避免对服务器造成过大压力
