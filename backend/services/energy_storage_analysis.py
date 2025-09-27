"""
储能布局分析服务 - 分析储能中心布局和配置
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class StorageOption:
    """储能方案选项"""
    name: str
    capacity: float  # 储能容量 (MWh)
    power: float  # 功率 (MW)
    efficiency: float  # 效率
    cost_per_mwh: float  # 每MWh成本 (万元)
    land_requirement: float  # 土地需求 (km²)
    lifespan: int  # 寿命 (年)
    suitability_score: float  # 适用性评分
    description: str

class EnergyStorageAnalysisService:
    """储能布局分析服务类"""
    
    def __init__(self):
        """初始化储能分析服务"""
        self.storage_technologies = {
            "lithium_battery": {
                "name": "锂离子电池",
                "efficiency": 0.90,
                "cost_per_mwh": 200,  # 万元/MWh
                "land_per_mwh": 0.001,  # km²/MWh
                "lifespan": 15,
                "suitable_for": ["削峰填谷", "频率调节", "应急备用"]
            },
            "pumped_hydro": {
                "name": "抽水蓄能",
                "efficiency": 0.75,
                "cost_per_mwh": 150,
                "land_per_mwh": 0.01,
                "lifespan": 50,
                "suitable_for": ["大规模储能", "削峰填谷", "调频调峰"]
            },
            "compressed_air": {
                "name": "压缩空气储能",
                "efficiency": 0.70,
                "cost_per_mwh": 180,
                "land_per_mwh": 0.005,
                "lifespan": 30,
                "suitable_for": ["大规模储能", "削峰填谷"]
            },
            "flow_battery": {
                "name": "液流电池",
                "efficiency": 0.80,
                "cost_per_mwh": 300,
                "land_per_mwh": 0.002,
                "lifespan": 20,
                "suitable_for": ["长时间储能", "削峰填谷"]
            },
            "hydrogen_storage": {
                "name": "氢能储能",
                "efficiency": 0.60,
                "cost_per_mwh": 400,
                "land_per_mwh": 0.003,
                "lifespan": 25,
                "suitable_for": ["长期储能", "跨季节储能"]
            }
        }
    
    async def analyze_storage_layout(self, lat: float, lon: float, 
                                   power_demand: float = 100,
                                   renewable_ratio: float = 0.7) -> Dict[str, Any]:
        """
        分析储能布局方案
        
        Args:
            lat: 纬度
            lon: 经度
            power_demand: 电力需求 (MW)
            renewable_ratio: 可再生能源比例
            
        Returns:
            储能布局分析结果
        """
        try:
            # 计算储能需求
            storage_requirements = self._calculate_storage_requirements(
                power_demand, renewable_ratio
            )
            
            # 获取地理条件
            terrain_type = self._get_terrain_type(lat, lon)
            water_availability = self._assess_water_availability(lat, lon)
            land_availability = self._assess_land_availability(lat, lon)
            
            # 分析各种储能方案
            storage_options = []
            
            # 锂离子电池分析
            if land_availability > 0.1:  # 需要一定土地
                lithium_option = self._analyze_lithium_battery(
                    storage_requirements, terrain_type, land_availability
                )
                storage_options.append(lithium_option)
            
            # 抽水蓄能分析
            if water_availability > 0.6 and terrain_type in ["山地", "丘陵"]:
                pumped_hydro_option = self._analyze_pumped_hydro(
                    storage_requirements, terrain_type, water_availability
                )
                storage_options.append(pumped_hydro_option)
            
            # 压缩空气储能分析
            if terrain_type in ["平原", "丘陵"] and land_availability > 0.2:
                caes_option = self._analyze_compressed_air(
                    storage_requirements, terrain_type, land_availability
                )
                storage_options.append(caes_option)
            
            # 液流电池分析
            if land_availability > 0.05:
                flow_battery_option = self._analyze_flow_battery(
                    storage_requirements, terrain_type, land_availability
                )
                storage_options.append(flow_battery_option)
            
            # 氢能储能分析
            if land_availability > 0.3:  # 需要较大土地
                hydrogen_option = self._analyze_hydrogen_storage(
                    storage_requirements, terrain_type, land_availability
                )
                storage_options.append(hydrogen_option)
            
            # 排序推荐方案
            storage_options.sort(key=lambda x: x.suitability_score, reverse=True)
            
            # 计算综合储能方案
            recommended_combination = self._recommend_storage_combination(
                storage_options, storage_requirements
            )
            
            return {
                "storage_requirements": storage_requirements,
                "terrain_type": terrain_type,
                "water_availability": water_availability,
                "land_availability": land_availability,
                "available_options": [
                    {
                        "name": option.name,
                        "capacity": option.capacity,
                        "power": option.power,
                        "efficiency": option.efficiency,
                        "cost_per_mwh": option.cost_per_mwh,
                        "land_requirement": option.land_requirement,
                        "lifespan": option.lifespan,
                        "suitability_score": option.suitability_score,
                        "description": option.description
                    }
                    for option in storage_options
                ],
                "recommended_combination": recommended_combination,
                "total_storage_capacity": sum(opt.capacity for opt in storage_options),
                "total_land_requirement": sum(opt.land_requirement for opt in storage_options),
                "total_cost": sum(opt.cost_per_mwh * opt.capacity for opt in storage_options)
            }
            
        except Exception as e:
            print(f"储能布局分析失败: {e}")
            return {
                "error": str(e),
                "available_options": [],
                "recommended_combination": []
            }
    
    def _calculate_storage_requirements(self, power_demand: float, 
                                      renewable_ratio: float) -> Dict[str, float]:
        """计算储能需求"""
        # 基础储能需求：可再生能源发电量的20-30%
        base_storage = power_demand * renewable_ratio * 0.25
        
        # 应急备用电源：总需求的10%
        emergency_backup = power_demand * 0.1
        
        # 削峰填谷：总需求的15%
        peak_shaving = power_demand * 0.15
        
        # 频率调节：总需求的5%
        frequency_regulation = power_demand * 0.05
        
        return {
            "base_storage": base_storage,
            "emergency_backup": emergency_backup,
            "peak_shaving": peak_shaving,
            "frequency_regulation": frequency_regulation,
            "total_energy": base_storage + emergency_backup + peak_shaving,
            "total_power": power_demand * 0.3  # 总功率需求
        }
    
    def _get_terrain_type(self, lat: float, lon: float) -> str:
        """获取地形类型"""
        # 简化的地形判断
        if 25 <= lat <= 35 and 100 <= lon <= 110:  # 西南山区
            return "山地"
        elif 30 <= lat <= 40 and 110 <= lon <= 120:  # 华北平原
            return "平原"
        elif 20 <= lat <= 30 and 110 <= lon <= 120:  # 华南丘陵
            return "丘陵"
        elif 40 <= lat <= 50 and 80 <= lon <= 100:  # 西北高原
            return "高原"
        else:
            return "平原"
    
    def _assess_water_availability(self, lat: float, lon: float) -> float:
        """评估水资源可用性"""
        # 基于地理位置的简单评估
        if 20 <= lat <= 35 and 110 <= lon <= 125:  # 华南
            return 0.9
        elif 25 <= lat <= 40 and 100 <= lon <= 110:  # 西南
            return 0.8
        elif 30 <= lat <= 45 and 120 <= lon <= 135:  # 华东
            return 0.7
        elif 35 <= lat <= 50 and 110 <= lon <= 125:  # 华北
            return 0.4
        elif 40 <= lat <= 55 and 80 <= lon <= 100:  # 西北
            return 0.2
        else:
            return 0.5
    
    def _assess_land_availability(self, lat: float, lon: float) -> float:
        """评估土地可用性"""
        # 基于人口密度和地理条件的简单评估
        if 40 <= lat <= 55 and 80 <= lon <= 100:  # 西北
            return 0.9
        elif 25 <= lat <= 40 and 100 <= lon <= 110:  # 西南
            return 0.7
        elif 30 <= lat <= 45 and 120 <= lon <= 135:  # 华东
            return 0.4
        elif 35 <= lat <= 50 and 110 <= lon <= 125:  # 华北
            return 0.5
        elif 20 <= lat <= 30 and 110 <= lon <= 120:  # 华南
            return 0.3
        else:
            return 0.6
    
    def _analyze_lithium_battery(self, requirements: Dict[str, float], 
                               terrain_type: str, land_availability: float) -> StorageOption:
        """分析锂离子电池方案"""
        config = self.storage_technologies["lithium_battery"]
        
        capacity = requirements["total_energy"]
        power = requirements["total_power"]
        
        # 计算适用性评分
        suitability_score = 0.8  # 基础评分
        
        if terrain_type in ["平原", "丘陵"]:
            suitability_score += 0.1
        
        if land_availability > 0.5:
            suitability_score += 0.1
        
        return StorageOption(
            name=config["name"],
            capacity=capacity,
            power=power,
            efficiency=config["efficiency"],
            cost_per_mwh=config["cost_per_mwh"],
            land_requirement=capacity * config["land_per_mwh"],
            lifespan=config["lifespan"],
            suitability_score=suitability_score,
            description=f"适用于削峰填谷和频率调节的锂离子电池储能系统"
        )
    
    def _analyze_pumped_hydro(self, requirements: Dict[str, float], 
                            terrain_type: str, water_availability: float) -> StorageOption:
        """分析抽水蓄能方案"""
        config = self.storage_technologies["pumped_hydro"]
        
        capacity = requirements["total_energy"] * 1.5  # 抽水蓄能容量更大
        power = requirements["total_power"] * 0.8
        
        suitability_score = 0.6  # 基础评分
        
        if terrain_type in ["山地", "丘陵"]:
            suitability_score += 0.3
        
        if water_availability > 0.7:
            suitability_score += 0.2
        
        return StorageOption(
            name=config["name"],
            capacity=capacity,
            power=power,
            efficiency=config["efficiency"],
            cost_per_mwh=config["cost_per_mwh"],
            land_requirement=capacity * config["land_per_mwh"],
            lifespan=config["lifespan"],
            suitability_score=suitability_score,
            description=f"基于{terrain_type}地形和水资源的抽水蓄能系统"
        )
    
    def _analyze_compressed_air(self, requirements: Dict[str, float], 
                              terrain_type: str, land_availability: float) -> StorageOption:
        """分析压缩空气储能方案"""
        config = self.storage_technologies["compressed_air"]
        
        capacity = requirements["total_energy"] * 1.2
        power = requirements["total_power"] * 0.9
        
        suitability_score = 0.7  # 基础评分
        
        if terrain_type in ["平原", "丘陵"]:
            suitability_score += 0.2
        
        if land_availability > 0.6:
            suitability_score += 0.1
        
        return StorageOption(
            name=config["name"],
            capacity=capacity,
            power=power,
            efficiency=config["efficiency"],
            cost_per_mwh=config["cost_per_mwh"],
            land_requirement=capacity * config["land_per_mwh"],
            lifespan=config["lifespan"],
            suitability_score=suitability_score,
            description=f"适用于{terrain_type}地形的大规模压缩空气储能系统"
        )
    
    def _analyze_flow_battery(self, requirements: Dict[str, float], 
                            terrain_type: str, land_availability: float) -> StorageOption:
        """分析液流电池方案"""
        config = self.storage_technologies["flow_battery"]
        
        capacity = requirements["total_energy"] * 0.8
        power = requirements["total_power"] * 0.6
        
        suitability_score = 0.75  # 基础评分
        
        if land_availability > 0.3:
            suitability_score += 0.15
        
        return StorageOption(
            name=config["name"],
            capacity=capacity,
            power=power,
            efficiency=config["efficiency"],
            cost_per_mwh=config["cost_per_mwh"],
            land_requirement=capacity * config["land_per_mwh"],
            lifespan=config["lifespan"],
            suitability_score=suitability_score,
            description="适用于长时间储能的液流电池系统"
        )
    
    def _analyze_hydrogen_storage(self, requirements: Dict[str, float], 
                                terrain_type: str, land_availability: float) -> StorageOption:
        """分析氢能储能方案"""
        config = self.storage_technologies["hydrogen_storage"]
        
        capacity = requirements["total_energy"] * 2.0  # 氢能储能容量大
        power = requirements["total_power"] * 0.5
        
        suitability_score = 0.6  # 基础评分
        
        if land_availability > 0.7:
            suitability_score += 0.3
        
        return StorageOption(
            name=config["name"],
            capacity=capacity,
            power=power,
            efficiency=config["efficiency"],
            cost_per_mwh=config["cost_per_mwh"],
            land_requirement=capacity * config["land_per_mwh"],
            lifespan=config["lifespan"],
            suitability_score=suitability_score,
            description="适用于长期储能和跨季节储能的氢能系统"
        )
    
    def _recommend_storage_combination(self, options: List[StorageOption], 
                                     requirements: Dict[str, float]) -> List[Dict[str, Any]]:
        """推荐储能组合方案"""
        if not options:
            return []
        
        # 选择前3个最合适的方案
        top_options = options[:3]
        
        combination = []
        remaining_energy = requirements["total_energy"]
        remaining_power = requirements["total_power"]
        
        for option in top_options:
            if remaining_energy > 0 and remaining_power > 0:
                # 计算该方案在组合中的比例
                energy_ratio = min(option.capacity / requirements["total_energy"], 1.0)
                power_ratio = min(option.power / requirements["total_power"], 1.0)
                
                combination.append({
                    "name": option.name,
                    "energy_ratio": energy_ratio,
                    "power_ratio": power_ratio,
                    "capacity": option.capacity * energy_ratio,
                    "power": option.power * power_ratio,
                    "suitability_score": option.suitability_score,
                    "description": option.description
                })
                
                remaining_energy -= option.capacity * energy_ratio
                remaining_power -= option.power * power_ratio
        
        return combination
