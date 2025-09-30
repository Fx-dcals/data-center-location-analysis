"""
数据中心智能选址与能源优化系统 - 后端主程序
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from pathlib import Path

from services.satellite_service import SatelliteService
from services.image_analysis import ImageAnalysisService
from services.energy_assessment import EnergyAssessmentService
from services.decision_analysis import DecisionAnalysisService
from services.power_supply_analysis import PowerSupplyAnalysisService
from services.energy_storage_analysis import EnergyStorageAnalysisService
from services.promethee_mcgp_analysis import PROMETHEEMCGP

# 创建FastAPI应用
app = FastAPI(
    title="数据中心智能选址与能源优化系统",
    description="基于卫星图像和AI的数据中心选址分析系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
satellite_service = SatelliteService()
image_service = ImageAnalysisService()
energy_service = EnergyAssessmentService()
decision_service = DecisionAnalysisService()
power_supply_service = PowerSupplyAnalysisService()
energy_storage_service = EnergyStorageAnalysisService()
promethee_mcgp_service = PROMETHEEMCGP()

# 数据模型
class LocationRequest(BaseModel):
    """位置请求模型"""
    latitude: float
    longitude: float
    radius: float = 1000  # 米
    city_name: Optional[str] = None

class AnalysisResult(BaseModel):
    """分析结果模型"""
    location: Dict[str, float]
    land_analysis: Dict[str, Any]
    energy_assessment: Dict[str, Any]
    decision_recommendation: Dict[str, Any]
    heat_utilization: Dict[str, Any]
    geographic_environment: Dict[str, Any]
    power_supply_analysis: Dict[str, Any]
    energy_storage_analysis: Dict[str, Any]
    promethee_mcgp_analysis: Dict[str, Any]

class CityAnalysisRequest(BaseModel):
    """城市分析请求模型"""
    cities: List[str]

# API路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "数据中心智能选址与能源优化系统API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/analyze/location", response_model=AnalysisResult)
async def analyze_location(request: LocationRequest):
    """
    分析指定位置的数据中心选址可行性
    """
    try:
        # 1. 获取卫星图像
        satellite_data = await satellite_service.get_satellite_data(
            request.latitude, 
            request.longitude, 
            request.radius
        )
        
        # 2. 图像分析
        land_analysis = await image_service.analyze_land_use(satellite_data)
        
        # 3. 能源评估
        energy_assessment = await energy_service.assess_energy_resources(
            request.latitude, 
            request.longitude,
            land_analysis
        )
        
        # 4. 决策分析
        decision_recommendation = await decision_service.analyze_location(
            land_analysis, 
            energy_assessment
        )
        
        # 5. 余热利用分析
        heat_utilization = await energy_service.analyze_heat_utilization(
            request.latitude,
            request.longitude,
            land_analysis
        )
        
        # 6. 地理环境分析
        geographic_environment = await energy_service.analyze_geographic_environment(
            request.latitude,
            request.longitude,
            request.radius
        )
        
        # 7. 供电方案分析
        power_supply_analysis = await power_supply_service.analyze_power_supply_options(
            request.latitude,
            request.longitude,
            power_demand=100  # 默认100MW需求
        )
        
        # 8. 储能布局分析
        energy_storage_analysis = await energy_storage_service.analyze_storage_layout(
            request.latitude,
            request.longitude,
            power_demand=100,
            renewable_ratio=0.7
        )
        
        # 9. PROMETHEE-MCGP决策分析
        promethee_mcgp_analysis = await promethee_mcgp_service.analyze_data_center_site_selection(
            request.latitude,
            request.longitude,
            request.city_name
        )
        
        return AnalysisResult(
            location={"latitude": request.latitude, "longitude": request.longitude},
            land_analysis=land_analysis,
            energy_assessment=energy_assessment,
            decision_recommendation=decision_recommendation,
            heat_utilization=heat_utilization,
            geographic_environment=geographic_environment,
            power_supply_analysis=power_supply_analysis,
            energy_storage_analysis=energy_storage_analysis,
            promethee_mcgp_analysis=promethee_mcgp_analysis
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.post("/analyze/cities")
async def analyze_cities(request: CityAnalysisRequest):
    """
    批量分析多个城市的数据中心选址情况
    """
    try:
        results = {}
        for city in request.cities:
            # 获取城市坐标（这里需要城市坐标数据库）
            city_coords = await satellite_service.get_city_coordinates(city)
            if city_coords:
                analysis = await analyze_location(LocationRequest(
                    latitude=city_coords["latitude"],
                    longitude=city_coords["longitude"],
                    city_name=city
                ))
                results[city] = analysis.dict()
        
        return {"cities_analysis": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"城市分析失败: {str(e)}")

@app.get("/satellite/image/{lat}/{lon}")
async def get_satellite_image(lat: float, lon: float, zoom: int = 15, radius: float = 1000):
    """
    获取指定位置的卫星图像
    """
    try:
        image_data = await satellite_service.get_satellite_image(lat, lon, zoom, radius)
        return {"image_url": image_data["url"], "metadata": image_data["metadata"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取卫星图像失败: {str(e)}")

@app.get("/energy/resources/{lat}/{lon}")
async def get_energy_resources(lat: float, lon: float, radius: float = 1000):
    """
    获取指定位置的能源资源信息
    """
    try:
        resources = await energy_service.get_local_energy_resources(lat, lon, radius)
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取能源资源失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
