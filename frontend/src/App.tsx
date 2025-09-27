import React, { useState } from 'react';
import { Layout, Menu, Typography, Card, Row, Col, Button, Input, Select, message } from 'antd';
import { 
  EnvironmentOutlined, 
  ThunderboltOutlined, 
  BulbOutlined, 
  BarChartOutlined,
  HomeOutlined,
  SearchOutlined
} from '@ant-design/icons';
import MapComponent from './components/MapComponent';
import AnalysisResults from './components/AnalysisResults';
import EnergyAssessment from './components/EnergyAssessment';
import DecisionAnalysis from './components/DecisionAnalysis';
import './App.css';

const { Header, Content, Sider } = Layout;
const { Title, Text } = Typography;
const { Option } = Select;

interface AnalysisData {
  location: { latitude: number; longitude: number };
  land_analysis: any;
  energy_assessment: any;
  decision_recommendation: any;
  heat_utilization: any;
}

const App: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = useState('map');
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState<{lat: number, lng: number} | null>(null);
  const [selectedCity, setSelectedCity] = useState<string>('');

  const cities = [
    { name: '北京', lat: 39.9042, lng: 116.4074 },
    { name: '上海', lat: 31.2304, lng: 121.4737 },
    { name: '深圳', lat: 22.5431, lng: 114.0579 },
    { name: '杭州', lat: 30.2741, lng: 120.1551 },
    { name: '中卫', lat: 37.5149, lng: 105.1967 },
    { name: '贵阳', lat: 26.6470, lng: 106.6302 },
    { name: '广州', lat: 23.1291, lng: 113.2644 },
    { name: '兰州', lat: 36.0611, lng: 103.8343 }
  ];

  const handleLocationSelect = (lat: number, lng: number) => {
    setSelectedLocation({ lat, lng });
  };

  const handleCitySelect = (cityName: string) => {
    const city = cities.find(c => c.name === cityName);
    if (city) {
      setSelectedLocation({ lat: city.lat, lng: city.lng });
      setSelectedCity(cityName);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedLocation) {
      message.warning('请先选择位置');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/analyze/location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: selectedLocation.lat,
          longitude: selectedLocation.lng,
          radius: 1000,
          city_name: selectedCity
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisData(data);
        message.success('分析完成！');
      } else {
        throw new Error('分析失败');
      }
    } catch (error) {
      message.error('分析失败，请重试');
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const menuItems = [
    {
      key: 'map',
      icon: <EnvironmentOutlined />,
      label: '地图选址',
    },
    {
      key: 'analysis',
      icon: <BarChartOutlined />,
      label: '分析结果',
    },
    {
      key: 'energy',
      icon: <ThunderboltOutlined />,
      label: '能源评估',
    },
    {
      key: 'decision',
      icon: <BulbOutlined />,
      label: '决策分析',
    },
  ];

  const renderContent = () => {
    switch (selectedMenu) {
      case 'map':
        return (
          <div>
            <Card title="位置选择" style={{ marginBottom: 16 }}>
              <Row gutter={16} align="middle">
                <Col span={8}>
                  <Select
                    placeholder="选择城市"
                    style={{ width: '100%' }}
                    onChange={handleCitySelect}
                    value={selectedCity}
                  >
                    {cities.map(city => (
                      <Option key={city.name} value={city.name}>
                        {city.name}
                      </Option>
                    ))}
                  </Select>
                </Col>
                <Col span={8}>
                  <Button 
                    type="primary" 
                    icon={<SearchOutlined />}
                    onClick={handleAnalyze}
                    loading={loading}
                    disabled={!selectedLocation}
                  >
                    开始分析
                  </Button>
                </Col>
                <Col span={8}>
                  <Text type="secondary">
                    {selectedLocation ? 
                      `已选择: ${selectedLocation.lat.toFixed(4)}, ${selectedLocation.lng.toFixed(4)}` : 
                      '请在地图上选择位置'
                    }
                  </Text>
                </Col>
              </Row>
            </Card>
            <MapComponent 
              onLocationSelect={handleLocationSelect}
              selectedLocation={selectedLocation}
            />
          </div>
        );
      case 'analysis':
        return <AnalysisResults data={analysisData} />;
      case 'energy':
        return <EnergyAssessment data={analysisData} />;
      case 'decision':
        return <DecisionAnalysis data={analysisData} />;
      default:
        return <div>请选择功能模块</div>;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
          <HomeOutlined style={{ color: 'white', fontSize: '24px', marginRight: '16px' }} />
          <Title level={3} style={{ color: 'white', margin: 0 }}>
            数据中心智能选址与能源优化系统
          </Title>
        </div>
      </Header>
      
      <Layout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[selectedMenu]}
            items={menuItems}
            onClick={({ key }) => setSelectedMenu(key)}
            style={{ height: '100%', borderRight: 0 }}
          />
        </Sider>
        
        <Layout style={{ padding: '24px' }}>
          <Content style={{ background: '#fff', padding: 24, minHeight: 280 }}>
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App;
