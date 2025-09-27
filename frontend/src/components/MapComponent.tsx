import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import { Card, Typography, Button, Space } from 'antd';
import { EnvironmentOutlined } from '@ant-design/icons';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const { Title, Text } = Typography;

// 修复Leaflet默认图标问题
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

interface MapComponentProps {
  onLocationSelect: (lat: number, lng: number) => void;
  selectedLocation: { lat: number; lng: number } | null;
}

// 地图点击事件处理组件
const MapClickHandler: React.FC<{ onLocationSelect: (lat: number, lng: number) => void }> = ({ onLocationSelect }) => {
  useMapEvents({
    click: (e) => {
      const { lat, lng } = e.latlng;
      onLocationSelect(lat, lng);
    },
  });
  return null;
};

const MapComponent: React.FC<MapComponentProps> = ({ onLocationSelect, selectedLocation }) => {
  const [mapCenter, setMapCenter] = useState<[number, number]>([39.9042, 116.4074]); // 默认北京
  const [mapZoom, setMapZoom] = useState(10);

  // 当选择位置改变时，更新地图中心
  useEffect(() => {
    if (selectedLocation) {
      setMapCenter([selectedLocation.lat, selectedLocation.lng]);
      setMapZoom(15);
    }
  }, [selectedLocation]);

  const handleGetCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          onLocationSelect(latitude, longitude);
        },
        (error) => {
          console.error('获取位置失败:', error);
        }
      );
    } else {
      console.error('浏览器不支持地理定位');
    }
  };

  return (
    <Card title="地图选址" className="map-container">
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Button 
            type="primary" 
            icon={<EnvironmentOutlined />}
            onClick={handleGetCurrentLocation}
          >
            获取当前位置
          </Button>
          <Text type="secondary">
            点击地图选择位置，或使用按钮获取当前位置
          </Text>
        </Space>
      </div>
      
      <div style={{ height: '500px', width: '100%' }}>
        <MapContainer
          center={mapCenter}
          zoom={mapZoom}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {/* 卫星图层选项 */}
          <TileLayer
            attribution='&copy; <a href="https://www.esri.com/">Esri</a>'
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            opacity={0.7}
          />
          
          <MapClickHandler onLocationSelect={onLocationSelect} />
          
          {selectedLocation && (
            <Marker position={[selectedLocation.lat, selectedLocation.lng]}>
              <Popup>
                <div>
                  <Title level={5}>选择的位置</Title>
                  <Text>纬度: {selectedLocation.lat.toFixed(6)}</Text><br />
                  <Text>经度: {selectedLocation.lng.toFixed(6)}</Text>
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>
      
      {selectedLocation && (
        <div style={{ marginTop: 16, padding: 12, background: '#f6ffed', borderRadius: 4 }}>
          <Text strong>已选择位置:</Text><br />
          <Text>纬度: {selectedLocation.lat.toFixed(6)}</Text><br />
          <Text>经度: {selectedLocation.lng.toFixed(6)}</Text>
        </div>
      )}
    </Card>
  );
};

export default MapComponent;
