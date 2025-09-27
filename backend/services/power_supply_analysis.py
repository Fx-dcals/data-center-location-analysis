"""
供电方案分析服务 - 基于地理位置和能源资源分析供电方案
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PowerSupplyOption:
    """供电方案选项"""
    name: str
    capacity: float  # 装机容量 (MW)
    efficiency: float  # 效率
    cost_per_mw: float  # 每MW成本 (万元)
    land_requirement: float  # 土地需求 (km²)
    suitability_score: float  # 适用性评分
    description: str

class PowerSupplyAnalysisService:
    """供电方案分析服务类"""
    
    def __init__(self):
        """初始化供电方案分析服务"""
        self.power_options = {
            "solar_pv": {
                "name": "太阳能光伏",
                "efficiency": 0.20,
                "cost_per_mw": 600,  # 万元/MW
                "land_per_mw": 0.02,  # km²/MW
                "suitable_regions": ["西北", "华北", "东北"]
            },
            "wind_onshore": {
                "name": "陆上风电",
                "efficiency": 0.35,
                "cost_per_mw": 800,
                "land_per_mw": 0.05,
                "suitable_regions": ["西北", "华北", "东北", "内蒙古"]
            },
            "wind_offshore": {
                "name": "海上风电",
                "efficiency": 0.40,
                "cost_per_mw": 1200,
                "land_per_mw": 0.01,  # 海上面积
                "suitable_regions": ["华东", "华南", "渤海湾"]
            },
            "hydro": {
                "name": "水力发电",
                "efficiency": 0.85,
                "cost_per_mw": 1000,
                "land_per_mw": 0.1,
                "suitable_regions": ["西南", "华中", "华南"]
            },
            "nuclear": {
                "name": "核能发电",
                "efficiency": 0.90,
                "cost_per_mw": 1500,
                "land_per_mw": 0.5,
                "suitable_regions": ["沿海地区"]
            }
        }
    
    async def analyze_power_supply_options(self, lat: float, lon: float, 
                                         power_demand: float = 100) -> Dict[str, Any]:
        """
        分析供电方案选项
        
        Args:
            lat: 纬度
            lon: 经度
            power_demand: 电力需求 (MW)
            
        Returns:
            供电方案分析结果
        """
        try:
            # 获取区域特征
            region_type = self._get_region_type(lat, lon)
            solar_potential = self._calculate_solar_potential(lat, lon)
            wind_potential = self._calculate_wind_potential(lat, lon)
            water_resources = self._assess_water_resources(lat, lon)
            
            # 分析各种供电方案
            power_options = []
            
            # 太阳能光伏分析
            if solar_potential > 1200:  # kWh/m²/year
                solar_option = self._analyze_solar_option(
                    solar_potential, power_demand, region_type
                )
                power_options.append(solar_option)
            
            # 陆上风电分析
            if wind_potential > 4.0:  # m/s
                wind_onshore_option = self._analyze_wind_onshore_option(
                    wind_potential, power_demand, region_type
                )
                power_options.append(wind_onshore_option)
            
            # 海上风电分析
            if self._is_coastal_region(lat, lon) and wind_potential > 5.0:
                wind_offshore_option = self._analyze_wind_offshore_option(
                    wind_potential, power_demand, region_type
                )
                power_options.append(wind_offshore_option)
            
            # 水力发电分析
            if water_resources > 0.5:  # 水资源丰富度
                hydro_option = self._analyze_hydro_option(
                    water_resources, power_demand, region_type
                )
                power_options.append(hydro_option)
            
            # 核能发电分析
            if self._is_suitable_for_nuclear(lat, lon):
                nuclear_option = self._analyze_nuclear_option(
                    power_demand, region_type
                )
                power_options.append(nuclear_option)
            
            # 排序推荐方案
            power_options.sort(key=lambda x: x.suitability_score, reverse=True)
            
            return {
                "region_type": region_type,
                "solar_potential": solar_potential,
                "wind_potential": wind_potential,
                "water_resources": water_resources,
                "power_demand": power_demand,
                "recommended_options": [
                    {
                        "name": option.name,
                        "capacity": option.capacity,
                        "efficiency": option.efficiency,
                        "cost_per_mw": option.cost_per_mw,
                        "land_requirement": option.land_requirement,
                        "suitability_score": option.suitability_score,
                        "description": option.description
                    }
                    for option in power_options
                ],
                "total_land_requirement": sum(opt.land_requirement for opt in power_options),
                "total_cost": sum(opt.cost_per_mw * opt.capacity for opt in power_options)
            }
            
        except Exception as e:
            print(f"供电方案分析失败: {e}")
            return {
                "error": str(e),
                "recommended_options": []
            }
    
    def _get_region_type(self, lat: float, lon: float) -> str:
        """获取区域类型"""
        if 35 <= lat <= 50 and 110 <= lon <= 125:
            return "华北"
        elif 20 <= lat <= 35 and 110 <= lon <= 125:
            return "华南"
        elif 25 <= lat <= 40 and 100 <= lon <= 110:
            return "西南"
        elif 30 <= lat <= 45 and 120 <= lon <= 135:
            return "华东"
        elif 40 <= lat <= 55 and 80 <= lon <= 100:
            return "西北"
        else:
            return "其他"
    
    def _calculate_solar_potential(self, lat: float, lon: float) -> float:
        """计算太阳能潜力"""
        # 基于纬度的基础辐射量
        base_irradiance = 1000 + (90 - abs(lat)) * 20
        
        # 经度调整
        if lon > 100:
            base_irradiance += 200
        elif lon < 110:
            base_irradiance -= 100
        
        # 城市调整
        city_adjustments = {
            (39.9042, 116.4074): 1500,  # 北京
            (31.2304, 121.4737): 1200,  # 上海
            (22.5431, 114.0579): 1300,  # 深圳
            (30.2741, 120.1551): 1400,  # 杭州
            (37.5149, 105.1967): 2000,  # 中卫
            (26.647, 106.6302): 1200,   # 贵阳
        }
        
        min_distance = float('inf')
        closest_irradiance = base_irradiance
        for (city_lat, city_lon), irradiance in city_adjustments.items():
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_irradiance = irradiance
        
        return closest_irradiance
    
    def _calculate_wind_potential(self, lat: float, lon: float) -> float:
        """计算风能潜力"""
        # 基于纬度的基础风速
        base_wind = 3.0 + (90 - abs(lat)) * 0.1
        
        # 经度调整
        if lon > 100:
            base_wind += 1.0
        elif lon < 110:
            base_wind -= 0.5
        
        # 城市调整
        city_adjustments = {
            (39.9042, 116.4074): 4.0,   # 北京
            (31.2304, 121.4737): 3.5,   # 上海
            (22.5431, 114.0579): 4.5,   # 深圳
            (30.2741, 120.1551): 3.8,   # 杭州
            (37.5149, 105.1967): 5.5,   # 中卫
            (26.647, 106.6302): 3.2,    # 贵阳
        }
        
        min_distance = float('inf')
        closest_wind = base_wind
        for (city_lat, city_lon), wind in city_adjustments.items():
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_wind = wind
        
        return closest_wind
    
    def _assess_water_resources(self, lat: float, lon: float) -> float:
        """评估水资源丰富度"""
        # 基于地理位置的简单评估
        if 20 <= lat <= 35 and 110 <= lon <= 125:  # 华南
            return 0.8
        elif 25 <= lat <= 40 and 100 <= lon <= 110:  # 西南
            return 0.9
        elif 30 <= lat <= 45 and 120 <= lon <= 135:  # 华东
            return 0.7
        elif 35 <= lat <= 50 and 110 <= lon <= 125:  # 华北
            return 0.3
        elif 40 <= lat <= 55 and 80 <= lon <= 100:  # 西北
            return 0.2
        else:
            return 0.5
    
    def _is_coastal_region(self, lat: float, lon: float) -> bool:
        """判断是否为沿海地区"""
        # 简化的沿海地区判断
        coastal_regions = [
            (20, 35, 110, 125),  # 华南沿海
            (30, 45, 120, 135),  # 华东沿海
            (35, 50, 115, 125),  # 华北沿海
        ]
        
        for min_lat, max_lat, min_lon, max_lon in coastal_regions:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                return True
        return False
    
    def _is_suitable_for_nuclear(self, lat: float, lon: float) -> bool:
        """判断是否适合核能发电"""
        # 核电站选址要求：沿海、地质稳定、人口密度低
        return (self._is_coastal_region(lat, lon) and 
                abs(lat) < 50 and  # 避免高纬度
                self._assess_water_resources(lat, lon) > 0.6)
    
    def _analyze_solar_option(self, solar_potential: float, power_demand: float, 
                            region_type: str) -> PowerSupplyOption:
        """分析太阳能光伏方案"""
        config = self.power_options["solar_pv"]
        
        # 计算装机容量
        capacity = power_demand * 1.2  # 考虑效率损失
        
        # 计算适用性评分
        suitability_score = min(solar_potential / 2000, 1.0) * 0.8  # 基础评分
        
        if region_type in ["西北", "华北", "东北"]:
            suitability_score += 0.2  # 区域优势
        
        return PowerSupplyOption(
            name=config["name"],
            capacity=capacity,
            efficiency=config["efficiency"],
            cost_per_mw=config["cost_per_mw"],
            land_requirement=capacity * config["land_per_mw"],
            suitability_score=suitability_score,
            description=f"基于年辐射量{solar_potential:.0f}kWh/m²的太阳能光伏方案"
        )
    
    def _analyze_wind_onshore_option(self, wind_potential: float, power_demand: float,
                                   region_type: str) -> PowerSupplyOption:
        """分析陆上风电方案"""
        config = self.power_options["wind_onshore"]
        
        capacity = power_demand * 1.1
        suitability_score = min(wind_potential / 6.0, 1.0) * 0.7
        
        if region_type in ["西北", "华北", "东北", "内蒙古"]:
            suitability_score += 0.3
        
        return PowerSupplyOption(
            name=config["name"],
            capacity=capacity,
            efficiency=config["efficiency"],
            cost_per_mw=config["cost_per_mw"],
            land_requirement=capacity * config["land_per_mw"],
            suitability_score=suitability_score,
            description=f"基于平均风速{wind_potential:.1f}m/s的陆上风电方案"
        )
    
    def _analyze_wind_offshore_option(self, wind_potential: float, power_demand: float,
                                    region_type: str) -> PowerSupplyOption:
        """分析海上风电方案"""
        config = self.power_options["wind_offshore"]
        
        capacity = power_demand * 1.05
        suitability_score = min(wind_potential / 7.0, 1.0) * 0.6
        
        if region_type in ["华东", "华南", "渤海湾"]:
            suitability_score += 0.4
        
        return PowerSupplyOption(
            name=config["name"],
            capacity=capacity,
            efficiency=config["efficiency"],
            cost_per_mw=config["cost_per_mw"],
            land_requirement=capacity * config["land_per_mw"],
            suitability_score=suitability_score,
            description=f"基于海上风速{wind_potential:.1f}m/s的海上风电方案"
        )
    
    def _analyze_hydro_option(self, water_resources: float, power_demand: float,
                            region_type: str) -> PowerSupplyOption:
        """分析水力发电方案"""
        config = self.power_options["hydro"]
        
        capacity = power_demand * 0.8  # 水电作为基础负荷
        suitability_score = water_resources * 0.8
        
        if region_type in ["西南", "华中", "华南"]:
            suitability_score += 0.2
        
        return PowerSupplyOption(
            name=config["name"],
            capacity=capacity,
            efficiency=config["efficiency"],
            cost_per_mw=config["cost_per_mw"],
            land_requirement=capacity * config["land_per_mw"],
            suitability_score=suitability_score,
            description=f"基于水资源丰富度{water_resources:.1f}的水力发电方案"
        )
    
    def _analyze_nuclear_option(self, power_demand: float, region_type: str) -> PowerSupplyOption:
        """分析核能发电方案"""
        config = self.power_options["nuclear"]
        
        capacity = power_demand * 2.0  # 核电站规模较大
        suitability_score = 0.6  # 基础评分
        
        if region_type in ["华东", "华南"]:
            suitability_score += 0.3
        
        return PowerSupplyOption(
            name=config["name"],
            capacity=capacity,
            efficiency=config["efficiency"],
            cost_per_mw=config["cost_per_mw"],
            land_requirement=capacity * config["land_per_mw"],
            suitability_score=suitability_score,
            description="基于沿海地理优势的核能发电方案"
        )
