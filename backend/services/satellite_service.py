"""
卫星数据服务 - 集成Google Earth Engine
"""

import ee
import requests
import json
from typing import Dict, Any, Optional, Tuple
import os
from datetime import datetime, timedelta
import base64
import io
from PIL import Image

class SatelliteService:
    """卫星数据服务类"""
    
    def __init__(self):
        """初始化GEE服务"""
        try:
            # 初始化Google Earth Engine
            # 使用您的项目ID
            ee.Initialize(project='data-center-location-analysis')
            print("Google Earth Engine 初始化成功")
            self.gee_available = True
        except Exception as e:
            print(f"GEE初始化失败: {e}")
            print("可能是网络连接问题，请检查网络连接和代理设置")
            self.gee_available = False
            raise e
    
    async def get_satellite_data(self, lat: float, lon: float, radius: float = 1000) -> Dict[str, Any]:
        """
        获取指定位置的卫星数据
        
        Args:
            lat: 纬度
            lon: 经度
            radius: 搜索半径（米）
            
        Returns:
            包含卫星图像和元数据的字典
        """
        # 创建感兴趣区域
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(radius)
        
        # 获取Landsat 8/9 图像
        collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                     .filterDate('2023-01-01', '2023-12-31')
                     .filterBounds(region)
                     .filter(ee.Filter.lt('CLOUD_COVER', 20)))
        
        # 选择最佳图像（云量最少）
        image = collection.sort('CLOUD_COVER').first()
        
        # 获取图像信息
        image_info = image.getInfo()
        
        # 计算NDVI（归一化植被指数）
        ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
        
        # 计算土地覆盖类型
        land_cover = self._classify_land_cover(image)
        
        return {
            "image": image,
            "ndvi": ndvi,
            "land_cover": land_cover,
            "metadata": {
                "acquisition_date": image_info.get('properties', {}).get('DATE_ACQUIRED'),
                "cloud_cover": image_info.get('properties', {}).get('CLOUD_COVER'),
                "center": [lat, lon],
                "radius": radius
            }
        }
    
    def _classify_land_cover(self, image: ee.Image) -> ee.Image:
        """
        基于卫星图像进行土地覆盖分类
        
        Args:
            image: Landsat图像
            
        Returns:
            土地覆盖分类结果
        """
        # 使用简单的阈值方法进行土地覆盖分类
        # 0: 水体, 1: 植被, 2: 裸地, 3: 建筑
        
        # 计算NDVI
        ndvi = image.normalizedDifference(['SR_B5', 'SR_B4'])
        
        # 计算NDWI（归一化水体指数）
        ndwi = image.normalizedDifference(['SR_B3', 'SR_B5'])
        
        # 计算建筑指数
        nbi = image.normalizedDifference(['SR_B5', 'SR_B6'])
        
        # 分类规则
        water = ndwi.gt(0.1)
        vegetation = ndvi.gt(0.3)
        bare_land = ndvi.lt(0.1).And(ndwi.lt(0.1))
        building = nbi.gt(0.1).And(ndvi.lt(0.2))
        
        # 合并分类结果
        land_cover = (water.multiply(0)
                    .add(vegetation.multiply(1))
                    .add(bare_land.multiply(2))
                    .add(building.multiply(3)))
        
        return land_cover.rename('land_cover')
    
    async def get_satellite_image(self, lat: float, lon: float, zoom: int = 10, radius: float = 1000) -> Dict[str, Any]:
        """
        获取卫星图像URL - 优先使用GEE真实卫星数据
        
        Args:
            lat: 纬度
            lon: 经度
            zoom: 缩放级别
            radius: 分析半径（米）
            
        Returns:
            包含图像URL和元数据的字典
        """
        try:
            # 首先尝试使用GEE获取真实卫星图像
            gee_result = await self._get_gee_satellite_image(lat, lon, zoom, radius)
            if gee_result and not gee_result.get("error"):
                return gee_result
            
            # 如果GEE失败，使用免费地图服务作为备选
            return await self._get_fallback_map_image(lat, lon, zoom)
            
        except Exception as e:
            print(f"卫星图像获取失败: {e}")
            return await self._get_fallback_map_image(lat, lon, zoom)
    
    async def _get_gee_satellite_image(self, lat: float, lon: float, zoom: int, radius: float = 1000) -> Dict[str, Any]:
        """使用GEE获取真实卫星图像"""
        try:
            # 由于GEE Map API需要复杂的认证，我们使用静态图像API
            point = ee.Geometry.Point([lon, lat])
            region = point.buffer(20000)  # 20公里半径
            
            # 获取Landsat 8/9 图像 - 扩大时间范围，放宽云量限制
            collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                         .filterDate('2020-01-01', '2024-12-31')  # 扩大时间范围
                         .filterBounds(region)
                         .filter(ee.Filter.lt('CLOUD_COVER', 50)))  # 放宽云量限制到50%
            
            # 选择最佳图像（云量最少）
            image = collection.sort('CLOUD_COVER').first()
            
            # 检查是否有可用图像
            image_count = collection.size().getInfo()
            print(f"找到 {image_count} 张可用图像")
            
            if image_count == 0:
                print("该地区无可用Landsat数据，尝试使用Sentinel-2")
                # 尝试使用Sentinel-2作为备选
                sentinel_collection = (ee.ImageCollection('COPERNICUS/S2_SR')
                                     .filterDate('2020-01-01', '2024-12-31')
                                     .filterBounds(region)
                                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50)))
                
                sentinel_image = sentinel_collection.sort('CLOUDY_PIXEL_PERCENTAGE').first()
                sentinel_count = sentinel_collection.size().getInfo()
                
                if sentinel_count > 0:
                    print(f"找到 {sentinel_count} 张Sentinel-2图像")
                    # 使用Sentinel-2的波段
                    rgb_image = sentinel_image.select(['B4', 'B3', 'B2'])
                else:
                    print("该地区无可用卫星数据")
                    return {"error": "该地区无可用卫星数据"}
            else:
                # 创建真彩色RGB图像 - 按照您提供的解决方案优化
                # 使用原始DN值，不进行复杂的缩放和偏移
                rgb_image = image.select(['SR_B4', 'SR_B3', 'SR_B2'])
            
            # 根据半径动态调整图像尺寸和缩放级别
            if radius <= 1000:
                dimensions = 400
                zoom_level = 15
            elif radius <= 2000:
                dimensions = 512
                zoom_level = 14
            elif radius <= 5000:
                dimensions = 600
                zoom_level = 13
            else:
                dimensions = 800
                zoom_level = 12
            
            # 使用GEE静态图像API - 根据半径动态调整
            image_url = rgb_image.getThumbURL({
                'region': region,
                'dimensions': dimensions,
                'format': 'png',
                'bands': ['SR_B4', 'SR_B3', 'SR_B2']
                # 去掉min和max参数，让GEE自动处理可视化范围
            })
            
            print(f"GEE卫星图像请求: 位置({lat}, {lon}), 半径{radius}m, 尺寸{dimensions}x{dimensions}")
            print(f"GEE图像URL: {image_url}")
            
            # 检查URL是否有效
            if not image_url or image_url.startswith('data:'):
                print("⚠️ 图像URL无效，可能是数据问题")
                return {"error": "图像URL生成失败"}
            
            return {
                "url": image_url,
                "tile_url": image_url,
                "metadata": {
                    "center": [lat, lon],
                    "radius": radius,
                    "dimensions": f"{dimensions}x{dimensions}",
                    "zoom_level": zoom_level,
                    "image_type": "真彩色RGB卫星图像",
                    "data_source": "Landsat 8/9",
                    "resolution": "30米",
                    "coverage_radius": f"{radius/1000}公里",
                    "map_service": "Google Earth Engine",
                    "free_service": False,
                    "gee_available": True
                }
            }
            
        except Exception as e:
            print(f"GEE卫星图像获取失败: {e}")
            return {"error": str(e)}
    
    async def _get_fallback_map_image(self, lat: float, lon: float, zoom: int) -> Dict[str, Any]:
        """获取备选地图图像"""
        try:
            import math
            
            # 计算瓦片坐标
            n = 2.0 ** zoom
            x = int((lon + 180.0) / 360.0 * n)
            y = int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)
            
            # 方案1: OpenStreetMap (免费，无需API密钥，最可靠)
            osm_url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
            
            # 方案2: Stamen地形图 (免费，显示地形)
            stamen_terrain_url = f"https://stamen-tiles.a.ssl.fastly.net/terrain/{zoom}/{x}/{y}.png"
            
            # 方案3: Stamen卫星图像 (免费，卫星视图)
            stamen_satellite_url = f"https://stamen-tiles.a.ssl.fastly.net/satellite/{zoom}/{x}/{y}.jpg"
            
            # 方案4: CartoDB基础地图 (免费，彩色地图)
            carto_voyager_url = f"https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/voyager/{zoom}/{x}/{y}.png"
            
            # 选择OpenStreetMap作为主要服务，最可靠
            image_url = osm_url
            
            print(f"备选地图图像请求: 位置({lat}, {lon}), 缩放级别{zoom}")
            print(f"瓦片坐标: ({x}, {y})")
            print(f"图像URL: {image_url}")
            
            return {
                "url": image_url,
                "tile_url": osm_url,
                "metadata": {
                    "center": [lat, lon],
                    "zoom": zoom,
                    "tile_coords": [x, y],
                    "image_type": "地图图像",
                    "data_source": "OpenStreetMap",
                    "resolution": "高分辨率",
                    "coverage_radius": "20公里",
                    "map_service": "OpenStreetMap",
                    "free_service": True,
                    "gee_available": False,
                    "alternatives": {
                        "osm": osm_url,
                        "stamen_terrain": stamen_terrain_url,
                        "stamen_satellite": stamen_satellite_url,
                        "carto_voyager": carto_voyager_url
                    }
                }
            }
            
        except Exception as e:
            print(f"备选地图图像获取失败: {e}")
            return {
                "url": f"https://via.placeholder.com/400x600/4CAF50/FFFFFF?text=地图图像: {lat:.2f}, {lon:.2f}",
                "tile_url": "",
                "metadata": {
                    "center": [lat, lon],
                    "zoom": zoom,
                    "error": str(e),
                    "gee_available": False
                }
            }
    
    async def get_city_coordinates(self, city_name: str) -> Optional[Dict[str, float]]:
        """
        获取城市坐标
        
        Args:
            city_name: 城市名称
            
        Returns:
            包含经纬度的字典
        """
        # 城市坐标数据库
        city_coords = {
            "北京": {"latitude": 39.9042, "longitude": 116.4074},
            "上海": {"latitude": 31.2304, "longitude": 121.4737},
            "深圳": {"latitude": 22.5431, "longitude": 114.0579},
            "杭州": {"latitude": 30.2741, "longitude": 120.1551},
            "中卫": {"latitude": 37.5149, "longitude": 105.1967},
            "贵阳": {"latitude": 26.6470, "longitude": 106.6302},
            "广州": {"latitude": 23.1291, "longitude": 113.2644},
            "兰州": {"latitude": 36.0611, "longitude": 103.8343}
        }
        
        return city_coords.get(city_name)
