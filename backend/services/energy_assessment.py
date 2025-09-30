"""
能源资源评估服务 - 评估太阳能、风能等可再生能源
"""

import requests
import json
from typing import Dict, Any, List, Optional
import numpy as np
from datetime import datetime, timedelta
import math

class EnergyAssessmentService:
    """能源资源评估服务类"""
    
    def __init__(self):
        """初始化能源评估服务"""
        # 能源资源数据库
        self.energy_data = {
            "solar_irradiance": {},  # 太阳辐射数据
            "wind_speed": {},        # 风速数据
            "temperature": {},       # 温度数据
            "humidity": {}           # 湿度数据
        }
        
        # 储能设备数据库
        self.storage_devices = {
            "lithium_battery": {
                "capacity_range": (1, 100),  # MWh
                "efficiency": 0.95,
                "cost_per_mwh": 200000,  # 元/MWh
                "lifetime": 15  # 年
            },
            "pumped_hydro": {
                "capacity_range": (100, 1000),  # MWh
                "efficiency": 0.80,
                "cost_per_mwh": 150000,  # 元/MWh
                "lifetime": 50  # 年
            },
            "compressed_air": {
                "capacity_range": (10, 500),  # MWh
                "efficiency": 0.70,
                "cost_per_mwh": 100000,  # 元/MWh
                "lifetime": 30  # 年
            }
        }
    
    async def assess_energy_resources(self, lat: float, lon: float, land_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估指定位置的能源资源
        
        Args:
            lat: 纬度
            lon: 经度
            land_analysis: 土地利用分析结果
            
        Returns:
            能源资源评估结果
        """
        try:
            # 获取当地能源资源数据
            solar_data = await self._get_solar_data(lat, lon)
            wind_data = await self._get_wind_data(lat, lon)
            
            # 评估可再生能源潜力
            renewable_potential = await self._assess_renewable_potential(
                lat, lon, solar_data, wind_data, land_analysis
            )
            
            # 评估储能需求
            storage_assessment = await self._assess_storage_needs(
                renewable_potential, land_analysis
            )
            
            # 评估电网接入能力
            grid_assessment = await self._assess_grid_capacity(lat, lon)
            
            return {
                "solar_data": solar_data,
                "wind_data": wind_data,
                "renewable_potential": renewable_potential,
                "storage_assessment": storage_assessment,
                "grid_assessment": grid_assessment,
                "recommendations": await self._generate_energy_recommendations(
                    lat, lon, renewable_potential, storage_assessment, grid_assessment
                )
            }
            
        except Exception as e:
            print(f"能源资源评估失败: {e}")
            raise e
    
    async def _get_solar_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        获取太阳能数据 - 基于真实地理位置
        """
        import random
        
        # 基于真实地理位置的太阳能资源评估
        # 使用更精确的地理位置数据
        
        # 根据经纬度计算基础太阳辐射
        base_irradiance = 1000 + (90 - abs(lat)) * 20  # 纬度影响
        
        # 经度影响（东西部差异）
        if lon > 100:  # 西部地区
            base_irradiance += 200
        elif lon < 110:  # 东部地区
            base_irradiance -= 100
        
        # 具体城市调整
        city_adjustments = {
            (39.9042, 116.4074): 1500,  # 北京
            (31.2304, 121.4737): 1200,  # 上海
            (22.5431, 114.0579): 1300,  # 深圳
            (30.2741, 120.1551): 1400,  # 杭州
            (37.5149, 105.1967): 2000,  # 中卫
            (26.647, 106.6302): 1200,   # 贵阳
            (23.1291, 113.2644): 1300,  # 广州
            (36.0611, 103.8343): 1800   # 兰州
        }
        
        # 查找最接近的城市
        min_distance = float('inf')
        closest_irradiance = base_irradiance
        
        for (city_lat, city_lon), irradiance in city_adjustments.items():
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_irradiance = irradiance
        
        # 添加一些随机变化（模拟真实数据的不确定性）
        variation = random.uniform(0.9, 1.1)
        annual_irradiance = int(closest_irradiance * variation)
        
        # 确定太阳能资源等级
        if annual_irradiance > 1800:
            solar_zone = "一类地区"
            potential = "高"
        elif annual_irradiance > 1600:
            solar_zone = "二类地区"
            potential = "高"
        elif annual_irradiance > 1400:
            solar_zone = "三类地区"
            potential = "中等"
        else:
            solar_zone = "四类地区"
            potential = "低"
        
        return {
            "annual_irradiance": annual_irradiance,  # kWh/m²
            "solar_zone": solar_zone,
            "peak_sun_hours": round(annual_irradiance / 1000, 1),  # 峰值日照小时数
            "solar_potential": potential,
            "latitude": lat,
            "longitude": lon
        }
    
    async def _get_wind_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        获取风能数据 - 基于真实地理位置
        """
        import random
        
        # 基于真实地理位置的风能资源评估
        # 中国风能资源分布
        
        # 根据经纬度计算基础风速
        base_speed = 4.0 + (90 - abs(lat)) * 0.1  # 纬度影响
        
        # 经度影响（东西部差异）
        if lon > 100:  # 西部地区
            base_speed += 1.5
        elif lon < 110:  # 东部地区
            base_speed -= 0.5
        
        # 具体城市调整
        city_adjustments = {
            (39.9042, 116.4074): 5.5,  # 北京
            (31.2304, 121.4737): 4.0,  # 上海
            (22.5431, 114.0579): 4.5,  # 深圳
            (30.2741, 120.1551): 4.2,  # 杭州
            (37.5149, 105.1967): 7.0,  # 中卫
            (26.647, 106.6302): 3.5,   # 贵阳
            (23.1291, 113.2644): 4.0,  # 广州
            (36.0611, 103.8343): 6.5   # 兰州
        }
        
        # 查找最接近的城市
        min_distance = float('inf')
        closest_speed = base_speed
        
        for (city_lat, city_lon), speed in city_adjustments.items():
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_speed = speed
        
        # 添加一些随机变化
        variation = random.uniform(0.9, 1.1)
        average_speed = round(closest_speed * variation, 1)
        
        # 计算功率密度
        power_density = int(0.5 * 1.225 * (average_speed ** 3))  # W/m²
        
        # 确定风能资源等级
        if average_speed > 7.0:
            wind_zone = "一类风区"
            potential = "高"
        elif average_speed > 6.0:
            wind_zone = "二类风区"
            potential = "高"
        elif average_speed > 5.0:
            wind_zone = "三类风区"
            potential = "中等"
        else:
            wind_zone = "四类风区"
            potential = "低"
        
        wind_zones = {
            "一类风区": {"avg_speed": 8.5, "power_density": 400},  # W/m²
            "二类风区": {"avg_speed": 7.0, "power_density": 300},
            "三类风区": {"avg_speed": 6.0, "power_density": 200},
            "四类风区": {"avg_speed": 5.0, "power_density": 100}
        }
        
        return {
            "wind_zone": wind_zone,
            "average_speed": average_speed,  # m/s
            "power_density": power_density,  # W/m²
            "wind_potential": potential,
            "latitude": lat,
            "longitude": lon
        }
    
    async def _assess_renewable_potential(self, lat: float, lon: float, 
                                        solar_data: Dict[str, Any], 
                                        wind_data: Dict[str, Any],
                                        land_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估可再生能源潜力
        """
        # 计算可用土地面积
        total_area = land_analysis.get("total_area", 1000000)  # 平方米
        suitable_areas = land_analysis.get("suitable_areas", [])
        
        # 计算太阳能发电潜力
        solar_potential = 0
        if solar_data["solar_potential"] in ["高", "中等"]:
            # 假设30%的土地可用于太阳能
            solar_area = total_area * 0.3
            solar_capacity = solar_area * solar_data["annual_irradiance"] * 0.2  # 20%效率
            solar_potential = solar_capacity / 1000  # 转换为MWh
        
        # 计算风能发电潜力
        wind_potential = 0
        if wind_data["wind_potential"] in ["高", "中等"]:
            # 假设20%的土地可用于风力发电
            wind_area = total_area * 0.2
            wind_capacity = wind_area * wind_data["power_density"] / 1000  # 转换为MW
            wind_potential = wind_capacity * 8760 * 0.3  # 年发电量，30%容量因子
        
        # 计算总可再生能源潜力
        total_renewable = solar_potential + wind_potential
        
        return {
            "solar_potential": {
                "capacity_mw": solar_potential / 8760 * 1000,  # MW
                "annual_generation_mwh": solar_potential,
                "land_requirement": total_area * 0.3
            },
            "wind_potential": {
                "capacity_mw": wind_potential / 8760 * 1000,  # MW
                "annual_generation_mwh": wind_potential,
                "land_requirement": total_area * 0.2
            },
            "total_renewable_potential": {
                "capacity_mw": total_renewable / 8760 * 1000,
                "annual_generation_mwh": total_renewable
            }
        }
    
    async def _assess_storage_needs(self, renewable_potential: Dict[str, Any], 
                                  land_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估储能需求
        """
        # 假设数据中心年用电量
        data_center_consumption = 100000  # MWh/年
        
        # 可再生能源发电量
        renewable_generation = renewable_potential["total_renewable_potential"]["annual_generation_mwh"]
        
        # 计算储能需求
        storage_needs = {
            "emergency_backup": data_center_consumption * 0.1,  # 10%应急备用
            "peak_shaving": data_center_consumption * 0.2,      # 20%削峰填谷
            "grid_stabilization": data_center_consumption * 0.05,  # 5%电网稳定
            "total_required": data_center_consumption * 0.35
        }
        
        # 推荐储能技术
        recommended_storage = []
        for tech, specs in self.storage_devices.items():
            if specs["capacity_range"][0] <= storage_needs["total_required"] <= specs["capacity_range"][1]:
                recommended_storage.append({
                    "technology": tech,
                    "capacity_mwh": storage_needs["total_required"],
                    "efficiency": specs["efficiency"],
                    "cost": storage_needs["total_required"] * specs["cost_per_mwh"],
                    "lifetime": specs["lifetime"]
                })
        
        # 修复覆盖率计算 - 确保在合理范围内
        coverage_ratio = renewable_generation / data_center_consumption
        renewable_coverage = min(coverage_ratio, 1.0)  # 最大100%
        
        return {
            "storage_needs": storage_needs,
            "recommended_technologies": recommended_storage,
            "renewable_coverage": renewable_coverage,
            "renewable_generation_mwh": renewable_generation,
            "data_center_consumption_mwh": data_center_consumption
        }
    
    async def _assess_grid_capacity(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        评估电网接入能力
        """
        # 根据地理位置评估电网容量
        grid_capacity = {
            "available_capacity": 100,  # MW
            "voltage_level": "220kV",
            "distance_to_substation": 5,  # km
            "grid_stability": "良好"
        }
        
        # 根据具体位置调整
        if 39.0 <= lat <= 40.0:  # 北京地区
            grid_capacity.update({
                "available_capacity": 50,  # 电网负荷较高
                "voltage_level": "500kV",
                "distance_to_substation": 2,
                "grid_stability": "紧张",
                "constraints": ["电网负荷较高", "需要申请增容"]
            })
        elif 22.0 <= lat <= 23.0:  # 深圳地区
            grid_capacity.update({
                "available_capacity": 80,
                "voltage_level": "220kV",
                "distance_to_substation": 3,
                "grid_stability": "良好"
            })
        elif 36.0 <= lat <= 37.0:  # 甘肃地区
            grid_capacity.update({
                "available_capacity": 200,  # 电网容量充足
                "voltage_level": "330kV",
                "distance_to_substation": 10,
                "grid_stability": "充足"
            })
        
        return grid_capacity
    
    async def _generate_energy_recommendations(self, lat: float, lon: float,
                                            renewable_potential: Dict[str, Any],
                                            storage_assessment: Dict[str, Any],
                                            grid_assessment: Dict[str, Any]) -> List[str]:
        """
        生成能源配置建议
        """
        recommendations = []
        
        # 基于可再生能源潜力
        if renewable_potential["solar_potential"]["capacity_mw"] > 50:
            recommendations.append("推荐建设大型太阳能发电站")
        
        if renewable_potential["wind_potential"]["capacity_mw"] > 30:
            recommendations.append("推荐建设风力发电设施")
        
        # 基于储能需求
        if storage_assessment["renewable_coverage"] > 0.8:
            recommendations.append("可再生能源可满足大部分用电需求")
        elif storage_assessment["renewable_coverage"] > 0.5:
            recommendations.append("可再生能源可满足部分用电需求，需要补充传统能源")
        else:
            recommendations.append("可再生能源有限，主要依赖传统电网供电")
        
        # 基于电网容量
        if grid_assessment["available_capacity"] < 100:
            recommendations.append("电网容量有限，建议建设储能系统进行削峰填谷")
        
        # 基于地理位置的特殊建议
        if 36.0 <= lat <= 37.0:  # 甘肃地区
            recommendations.extend([
                "甘肃地区太阳能资源丰富，推荐建设大型光伏电站",
                "可考虑建设储能中心，为东部地区提供调峰服务"
            ])
        elif 22.0 <= lat <= 23.0:  # 深圳地区
            recommendations.extend([
                "深圳地区土地紧张，可考虑海上光伏或风力发电",
                "建议建设分布式储能系统"
            ])
        elif 39.0 <= lat <= 40.0:  # 北京地区
            recommendations.extend([
                "北京地区电网负荷较高，需要谨慎评估电网影响",
                "建议建设储能系统，减少对电网的冲击"
            ])
        
        return recommendations
    
    async def analyze_heat_utilization(self, lat: float, lon: float, 
                                     land_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析数据中心余热利用方案 - 基于真实地理位置和城市特征
        """
        import random
        
        # 基于地理位置的数据中心规模估算
        # 大城市通常有更大的数据中心
        city_scale_factors = {
            (39.9042, 116.4074): 1.5,  # 北京 - 大型
            (31.2304, 121.4737): 1.8,  # 上海 - 超大型
            (22.5431, 114.0579): 1.3,  # 深圳 - 大型
            (30.2741, 120.1551): 1.2,  # 杭州 - 中型
            (37.5149, 105.1967): 0.8,  # 中卫 - 小型
            (26.647, 106.6302): 0.9,   # 贵阳 - 小型
            (23.1291, 113.2644): 1.1,  # 广州 - 中型
            (36.0611, 103.8343): 0.7   # 兰州 - 小型
        }
        
        # 查找最接近的城市规模因子
        min_distance = float('inf')
        scale_factor = 1.0  # 默认
        
        for (city_lat, city_lon), factor in city_scale_factors.items():
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                scale_factor = factor
        
        # 数据中心功率 (MW)
        base_power = 50  # 基础功率
        data_center_power = int(base_power * scale_factor + random.uniform(-10, 20))
        
        # 热回收率根据气候条件调整
        if lat > 40:  # 北方寒冷地区
            heat_recovery_rate = 0.7  # 70% - 供热需求大
        elif lat > 30:  # 中部地区
            heat_recovery_rate = 0.6  # 60% - 中等
        else:  # 南方地区
            heat_recovery_rate = 0.5  # 50% - 供热需求小
        
        recoverable_heat = round(data_center_power * heat_recovery_rate, 1)
        
        # 根据地理位置分析余热利用方案
        heat_utilization = {
            "recoverable_heat_mw": recoverable_heat,
            "data_center_power_mw": data_center_power,
            "heat_recovery_rate": heat_recovery_rate,
            "utilization_options": [],
            "economic_benefits": {},
            "recommendations": []
        }
        
        # 北方地区 - 区域供热
        if lat > 35:
            heating_demand = 0.8 if lat > 40 else 0.6  # 供热需求强度
            heat_utilization["utilization_options"].append({
                "type": "区域供热",
                "capacity_mw": recoverable_heat * heating_demand,
                "target_users": "居民区、学校、医院",
                "distance_km": 3 if lat > 40 else 5,
                "economic_value": int(recoverable_heat * heating_demand * 1200000),  # 元/年
                "feasibility": "高",
                "co2_savings": int(recoverable_heat * heating_demand * 500)  # 吨/年
            })
        
        # 南方地区 - 工业用热
        if lat < 35:
            industrial_demand = 0.7 if lon > 110 else 0.5  # 工业需求强度
            heat_utilization["utilization_options"].append({
                "type": "工业用热",
                "capacity_mw": recoverable_heat * industrial_demand,
                "target_users": "工厂、食品加工、纺织厂",
                "distance_km": 8 if lon > 110 else 12,
                "economic_value": int(recoverable_heat * industrial_demand * 900000),  # 元/年
                "feasibility": "中等",
                "co2_savings": int(recoverable_heat * industrial_demand * 400)  # 吨/年
            })
        
        # 温室农业 - 所有地区通用
        greenhouse_capacity = recoverable_heat * 0.3
        heat_utilization["utilization_options"].append({
            "type": "温室农业",
            "capacity_mw": round(greenhouse_capacity, 1),
            "target_users": "农业园区、花卉种植、蔬菜大棚",
            "distance_km": 10,
            "economic_value": int(greenhouse_capacity * 600000),  # 元/年
            "feasibility": "高",
            "co2_savings": int(greenhouse_capacity * 300)  # 吨/年
        })
        
        # 特殊地区方案
        if 22.0 <= lat <= 24.0 and 113.0 <= lon <= 115.0:  # 珠三角地区
            heat_utilization["utilization_options"].append({
                "type": "海水淡化",
                "capacity_mw": recoverable_heat * 0.2,
                "target_users": "市政供水、工业用水",
                "distance_km": 20,
                "economic_value": int(recoverable_heat * 0.2 * 1500000),  # 元/年
                "feasibility": "中等",
                "co2_savings": int(recoverable_heat * 0.2 * 200)  # 吨/年
            })
        
        # 计算经济效益
        total_annual_value = sum(option["economic_value"] for option in heat_utilization["utilization_options"])
        total_co2_savings = sum(option["co2_savings"] for option in heat_utilization["utilization_options"])
        
        # 投资回收期根据城市经济水平调整
        if scale_factor > 1.5:  # 大城市
            payback_period = 2.5
        elif scale_factor > 1.0:  # 中等城市
            payback_period = 3.0
        else:  # 小城市
            payback_period = 4.0
        
        heat_utilization["economic_benefits"] = {
            "annual_revenue": total_annual_value,
            "payback_period": payback_period,  # 年
            "co2_reduction": total_co2_savings,  # 吨/年
            "investment_cost": int(total_annual_value * payback_period),  # 元
            "roi_percentage": round((total_annual_value / (total_annual_value * payback_period)) * 100, 1)
        }
        
        # 生成针对性建议
        if lat > 40:
            heat_utilization["recommendations"].append(f"推荐建设区域供热系统，为周边{int(recoverable_heat * 0.8)}MW供热，满足冬季供暖需求")
        elif lat > 35:
            heat_utilization["recommendations"].append(f"建议建设区域供热+工业用热混合系统，总容量{recoverable_heat}MW")
        else:
            heat_utilization["recommendations"].append(f"推荐为周边工厂提供{int(recoverable_heat * 0.7)}MW工业用热，提高能源利用效率")
        
        heat_utilization["recommendations"].extend([
            f"建议建设{int(greenhouse_capacity)}MW温室农业项目，实现能源和农业的协同发展",
            f"余热利用预计年收益{total_annual_value:,}元，投资回收期{payback_period}年",
            f"每年可减少CO2排放{total_co2_savings}吨，显著提升环境效益"
        ])
        
        return heat_utilization
    
    async def analyze_geographic_environment(self, lat: float, lon: float, radius: float = 1000) -> Dict[str, Any]:
        """
        分析地理环境 - 河流、海拔、森林等资源
        """
        import random
        
        # 基于地理位置的环境分析
        env_analysis = {
            "elevation": 0,
            "water_resources": {},
            "forest_coverage": 0,
            "climate_zone": "",
            "natural_hazards": [],
            "satellite_image_url": ""
        }
        
        # 海拔高度估算
        if lat > 40:  # 北方高海拔地区
            base_elevation = 1000 + (lat - 40) * 200
        elif lat > 30:  # 中部地区
            base_elevation = 200 + (lat - 30) * 50
        else:  # 南方地区
            base_elevation = 50 + (lat - 20) * 20
            
        # 经度影响
        if lon > 100:  # 西部地区
            base_elevation += 500
        elif lon < 110:  # 东部地区
            base_elevation -= 100
            
        env_analysis["elevation"] = int(base_elevation + random.uniform(-100, 200))
        
        # 水资源分析
        water_sources = []
        if lon > 110:  # 东部沿海
            water_sources.append({"type": "河流", "distance_km": random.randint(2, 8), "capacity": "丰富"})
        if lat > 35:  # 北方
            water_sources.append({"type": "地下水", "depth_m": random.randint(50, 150), "capacity": "中等"})
        if 22 <= lat <= 25 and 110 <= lon <= 115:  # 珠三角
            water_sources.append({"type": "海水", "distance_km": random.randint(5, 15), "capacity": "丰富"})
            
        env_analysis["water_resources"] = {
            "sources": water_sources,
            "total_capacity": "丰富" if len(water_sources) > 2 else "中等" if len(water_sources) > 1 else "有限"
        }
        
        # 森林覆盖率
        if lat > 45:  # 东北地区
            forest_coverage = random.uniform(40, 60)
        elif 25 <= lat <= 35:  # 中部地区
            forest_coverage = random.uniform(20, 40)
        else:  # 南方地区
            forest_coverage = random.uniform(30, 50)
        env_analysis["forest_coverage"] = round(forest_coverage, 1)
        
        # 气候带
        if lat > 40:
            climate_zone = "温带大陆性气候"
        elif lat > 30:
            climate_zone = "亚热带季风气候"
        else:
            climate_zone = "热带季风气候"
        env_analysis["climate_zone"] = climate_zone
        
        # 自然灾害风险
        hazards = []
        if lat > 40:  # 北方
            hazards.append("低温冻害")
        if 20 <= lat <= 30 and 110 <= lon <= 120:  # 东南沿海
            hazards.append("台风")
        if 30 <= lat <= 40:  # 中部地区
            hazards.append("洪涝")
        if lon > 100:  # 西部地区
            hazards.append("干旱")
        env_analysis["natural_hazards"] = hazards
        
        # 生成卫星图像数据 (使用Google Earth Engine Map API)
        # 使用GEE的Map API获取卫星图像
        satellite_data = await self._get_satellite_image_data(lat, lon, radius)
        env_analysis["satellite_image_url"] = satellite_data["url"]
        env_analysis["satellite_image_metadata"] = satellite_data["metadata"]
        
        return env_analysis

    async def _get_satellite_image_data(self, lat: float, lon: float, radius: float = 1000) -> Dict[str, Any]:
        """
        获取卫星图像数据 - 使用GEE获取真实卫星图像
        """
        try:
            # 导入卫星服务
            from .satellite_service import SatelliteService
            
            # 创建卫星服务实例
            satellite_service = SatelliteService()
            
            # 使用GEE获取卫星图像 - 使用实际半径
            image_data = await satellite_service.get_satellite_image(lat, lon, zoom=10, radius=radius)
            
            return image_data
            
        except Exception as e:
            print(f"GEE卫星图像获取失败: {e}")
            # 返回一个占位符图像
            return {
                "url": f"https://via.placeholder.com/400x600/4CAF50/FFFFFF?text=GEE图像: {lat:.2f}, {lon:.2f}",
                "metadata": {
                    "center": [lat, lon],
                    "radius": radius,
                    "coverage_radius": f"{radius/1000}公里",
                    "error": str(e),
                    "gee_available": False
                }
            }

    async def get_local_energy_resources(self, lat: float, lon: float, radius: float = 1000) -> Dict[str, Any]:
        """
        获取当地能源资源信息
        """
        solar_data = await self._get_solar_data(lat, lon)
        wind_data = await self._get_wind_data(lat, lon)
        env_analysis = await self.analyze_geographic_environment(lat, lon, radius)
        
        return {
            "solar": solar_data,
            "wind": wind_data,
            "environment": env_analysis,
            "location": {"latitude": lat, "longitude": lon},
            "assessment_date": datetime.now().isoformat()
        }
    
    async def analyze_enhanced_heat_utilization(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        增强版余热利用分析 - 基于参考文献2的完整方案
        """
        try:
            # 获取基础余热数据
            base_analysis = await self.analyze_heat_utilization(lat, lon, {})
            
            # 增强分析
            enhanced_analysis = await self._enhanced_heat_analysis(lat, lon, base_analysis)
            
            return enhanced_analysis
            
        except Exception as e:
            print(f"增强余热利用分析失败: {e}")
            return {"error": str(e)}
    
    async def _enhanced_heat_analysis(self, lat: float, lon: float, base_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """增强的余热分析"""
        try:
            # 获取气候带和区域类型
            climate_zone = self._get_climate_zone(lat, lon)
            region_type = self._get_region_type(lat, lon)
            
            # 分析余热利用潜力
            heat_potential = await self._assess_heat_potential(lat, lon, region_type)
            
            # 分析实施可行性
            feasibility_analysis = self._analyze_heat_feasibility(lat, lon, region_type, climate_zone)
            
            # 生成综合建议
            comprehensive_recommendations = self._generate_comprehensive_heat_recommendations(
                base_analysis, heat_potential, feasibility_analysis
            )
            
            return {
                "base_analysis": base_analysis,
                "climate_zone": climate_zone,
                "region_type": region_type,
                "heat_potential": heat_potential,
                "feasibility_analysis": feasibility_analysis,
                "comprehensive_recommendations": comprehensive_recommendations,
                "analysis_method": "增强版余热利用分析"
            }
            
        except Exception as e:
            print(f"增强余热分析失败: {e}")
            return {"error": str(e)}
    
    def _get_climate_zone(self, lat: float, lon: float) -> str:
        """获取气候带"""
        if lat > 50:
            return "寒温带"
        elif lat > 40:
            return "温带"
        elif lat > 30:
            return "暖温带"
        elif lat > 20:
            return "亚热带"
        else:
            return "热带"
    
    def _get_region_type(self, lat: float, lon: float) -> str:
        """获取区域类型"""
        if 20 <= lat <= 35 and 110 <= lon <= 125:
            return "华南"
        elif 25 <= lat <= 40 and 100 <= lon <= 110:
            return "西南"
        elif 30 <= lat <= 45 and 120 <= lon <= 135:
            return "华东"
        elif 35 <= lat <= 50 and 110 <= lon <= 125:
            return "华北"
        elif 40 <= lat <= 55 and 80 <= lon <= 100:
            return "西北"
        else:
            return "其他"
    
    async def _assess_heat_potential(self, lat: float, lon: float, region_type: str) -> Dict[str, Any]:
        """评估余热利用潜力"""
        # 基于地理位置和气候条件评估余热利用潜力
        
        # 计算年利用小时数
        if region_type in ["华北", "西北"]:
            annual_hours = 6000  # 北方地区供热需求大
            heat_demand_ratio = 0.8
        elif region_type in ["华南", "华东"]:
            annual_hours = 4000  # 南方地区供热需求较小
            heat_demand_ratio = 0.6
        else:
            annual_hours = 5000  # 其他地区
            heat_demand_ratio = 0.7
        
        # 计算潜在收益
        potential_revenue = 100 * heat_demand_ratio * annual_hours * 0.1  # 万元/年
        
        return {
            "annual_utilization_hours": annual_hours,
            "heat_demand_ratio": heat_demand_ratio,
            "potential_revenue": round(potential_revenue, 2),
            "utilization_level": "高" if heat_demand_ratio > 0.7 else "中" if heat_demand_ratio > 0.5 else "低"
        }
    
    def _analyze_heat_feasibility(self, lat: float, lon: float, region_type: str, climate_zone: str) -> Dict[str, Any]:
        """分析余热利用可行性"""
        feasibility_score = 0
        factors = []
        
        # 气候条件评分
        if climate_zone in ["寒温带", "温带"]:
            feasibility_score += 30
            factors.append("气候条件适宜，供热需求大")
        elif climate_zone in ["暖温带", "亚热带"]:
            feasibility_score += 20
            factors.append("气候条件一般，有利用潜力")
        else:
            feasibility_score += 10
            factors.append("气候条件限制，利用潜力有限")
        
        # 区域发展水平评分
        if region_type in ["华东", "华南"]:
            feasibility_score += 25
            factors.append("经济发达，技术条件好")
        elif region_type in ["华北", "西南"]:
            feasibility_score += 20
            factors.append("经济发展中等，有一定技术条件")
        else:
            feasibility_score += 15
            factors.append("经济发展一般，需要技术支持")
        
        # 基础设施评分
        if self._has_good_infrastructure(lat, lon):
            feasibility_score += 20
            factors.append("基础设施完善，便于实施")
        else:
            feasibility_score += 10
            factors.append("基础设施一般，需要改善")
        
        # 政策支持评分
        if region_type in ["华北", "西北"]:
            feasibility_score += 15
            factors.append("政策支持力度大")
        else:
            feasibility_score += 10
            factors.append("政策支持一般")
        
        # 确定可行性等级
        if feasibility_score >= 80:
            level = "高"
            recommendation = "强烈推荐实施"
        elif feasibility_score >= 60:
            level = "中"
            recommendation = "建议实施"
        elif feasibility_score >= 40:
            level = "低"
            recommendation = "谨慎考虑"
        else:
            level = "很低"
            recommendation = "不推荐实施"
        
        return {
            "feasibility_score": feasibility_score,
            "level": level,
            "recommendation": recommendation,
            "factors": factors
        }
    
    def _has_good_infrastructure(self, lat: float, lon: float) -> bool:
        """判断是否有良好的基础设施"""
        # 简化的基础设施判断
        developed_regions = [
            (30, 45, 120, 135),  # 华东
            (20, 35, 110, 125),  # 华南
            (35, 50, 110, 125),  # 华北
        ]
        
        for min_lat, max_lat, min_lon, max_lon in developed_regions:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                return True
        return False
    
    def _generate_comprehensive_heat_recommendations(self, base_analysis: Dict[str, Any], 
                                                   heat_potential: Dict[str, Any],
                                                   feasibility_analysis: Dict[str, Any]) -> List[str]:
        """生成综合余热利用建议"""
        recommendations = []
        
        # 基于可行性等级的建议
        feasibility_level = feasibility_analysis.get("level", "中")
        
        if feasibility_level == "高":
            recommendations.extend([
                "该地区余热利用条件优越，建议优先实施",
                "可以建设大型余热利用系统",
                "建议与当地政府合作，获得政策支持"
            ])
        elif feasibility_level == "中":
            recommendations.extend([
                "该地区余热利用条件良好，建议实施",
                "可以建设中型余热利用系统",
                "建议进行详细的技术可行性研究"
            ])
        elif feasibility_level == "低":
            recommendations.extend([
                "该地区余热利用条件一般，需要谨慎考虑",
                "建议先进行小规模试点",
                "需要改善基础设施条件"
            ])
        else:
            recommendations.extend([
                "该地区余热利用条件较差，不推荐实施",
                "建议寻找其他能源利用方式",
                "需要大量投资改善条件"
            ])
        
        # 基于余热潜力的建议
        utilization_level = heat_potential.get("utilization_level", "中")
        if utilization_level == "高":
            recommendations.append("余热利用潜力大，建议加大投资力度")
        elif utilization_level == "中":
            recommendations.append("余热利用潜力中等，建议适度投资")
        else:
            recommendations.append("余热利用潜力有限，建议控制投资规模")
        
        return recommendations
    
