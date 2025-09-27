import React from 'react';
import { Card, Row, Col, Typography, Progress, Tag, Table, Statistic } from 'antd';
import { 
  ThunderboltOutlined, 
  EnvironmentOutlined,
  BulbOutlined,
  FireOutlined
} from '@ant-design/icons';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const { Title, Text } = Typography;

interface EnergyAssessmentProps {
  data: any;
}

const EnergyAssessment: React.FC<EnergyAssessmentProps> = ({ data }) => {
  if (!data) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <ThunderboltOutlined style={{ fontSize: '48px', color: '#ccc' }} />
          <Title level={4} style={{ color: '#ccc', marginTop: '16px' }}>
            暂无能源评估数据
          </Title>
          <Text type="secondary">请先进行位置分析</Text>
        </div>
      </Card>
    );
  }

  const { energy_assessment } = data;

  // 准备图表数据
  const landUseData = data.land_analysis?.land_use_distribution ? 
    Object.entries(data.land_analysis.land_use_distribution).map(([name, value]: [string, any]) => ({
      name,
      value: (value * 100).toFixed(1),
      percentage: value * 100
    })) : [];

  const energySourceData = [
    {
      name: '太阳能',
      value: energy_assessment?.renewable_potential?.solar_potential?.annual_generation_mwh || 0,
      color: '#faad14'
    },
    {
      name: '风能',
      value: energy_assessment?.renewable_potential?.wind_potential?.annual_generation_mwh || 0,
      color: '#1890ff'
    },
    {
      name: '传统电网',
      value: 100000 - (energy_assessment?.renewable_potential?.total_renewable_potential?.annual_generation_mwh || 0),
      color: '#ff7875'
    }
  ];

  const storageColumns = [
    {
      title: '储能技术',
      dataIndex: 'technology',
      key: 'technology',
    },
    {
      title: '容量 (MWh)',
      dataIndex: 'capacity_mwh',
      key: 'capacity_mwh',
    },
    {
      title: '效率',
      dataIndex: 'efficiency',
      key: 'efficiency',
      render: (efficiency: number) => `${(efficiency * 100).toFixed(1)}%`
    },
    {
      title: '成本 (万元)',
      dataIndex: 'cost',
      key: 'cost',
      render: (cost: number) => (cost / 10000).toFixed(0)
    },
    {
      title: '寿命 (年)',
      dataIndex: 'lifetime',
      key: 'lifetime',
    },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <div>
      <Title level={2}>能源资源详细评估</Title>
      
      {/* 能源资源概览 */}
      <Card title="能源资源概览" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Statistic
              title="太阳能年辐射量"
              value={energy_assessment?.solar_data?.annual_irradiance || 0}
              suffix="kWh/m²"
              prefix={<ThunderboltOutlined style={{ color: '#faad14' }} />}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="平均风速"
              value={energy_assessment?.wind_data?.average_speed || 0}
              suffix="m/s"
              prefix={<EnvironmentOutlined style={{ color: '#1890ff' }} />}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="可再生能源潜力"
              value={energy_assessment?.renewable_potential?.total_renewable_potential?.annual_generation_mwh || 0}
              suffix="MWh/年"
              prefix={<BulbOutlined style={{ color: '#52c41a' }} />}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="可再生能源覆盖率"
              value={(energy_assessment?.storage_assessment?.renewable_coverage * 100 || 0).toFixed(1)}
              suffix="%"
              prefix={<FireOutlined style={{ color: '#ff7875' }} />}
            />
          </Col>
        </Row>
      </Card>

      {/* 土地利用分布 */}
      <Card title="土地利用分布" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={12}>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={landUseData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name}: ${percentage.toFixed(1)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="percentage"
                >
                  {landUseData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Col>
          <Col span={12}>
            <Title level={4}>土地类型详情</Title>
            {landUseData.map((item, index) => (
              <div key={index} style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div 
                      style={{ 
                        width: 12, 
                        height: 12, 
                        backgroundColor: COLORS[index % COLORS.length], 
                        marginRight: 8 
                      }} 
                    />
                    <Text>{item.name}</Text>
                  </div>
                  <Text strong>{item.value}%</Text>
                </div>
                <Progress 
                  percent={parseFloat(item.value)} 
                  size="small" 
                  strokeColor={COLORS[index % COLORS.length]}
                  showInfo={false}
                />
              </div>
            ))}
          </Col>
        </Row>
      </Card>

      {/* 能源结构分析 */}
      <Card title="能源结构分析" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={12}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={energySourceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Col>
          <Col span={12}>
            <Title level={4}>能源配置建议</Title>
            <div style={{ marginBottom: 16 }}>
              <Text strong>太阳能发电:</Text>
              <div style={{ marginLeft: 16 }}>
                <Text>• 装机容量: {energy_assessment?.renewable_potential?.solar_potential?.capacity_mw?.toFixed(1)} MW</Text><br />
                <Text>• 年发电量: {energy_assessment?.renewable_potential?.solar_potential?.annual_generation_mwh?.toFixed(0)} MWh</Text><br />
                <Text>• 土地需求: {(energy_assessment?.renewable_potential?.solar_potential?.land_requirement / 10000).toFixed(1)} 公顷</Text>
              </div>
            </div>
            
            <div style={{ marginBottom: 16 }}>
              <Text strong>风力发电:</Text>
              <div style={{ marginLeft: 16 }}>
                <Text>• 装机容量: {energy_assessment?.renewable_potential?.wind_potential?.capacity_mw?.toFixed(1)} MW</Text><br />
                <Text>• 年发电量: {energy_assessment?.renewable_potential?.wind_potential?.annual_generation_mwh?.toFixed(0)} MWh</Text><br />
                <Text>• 土地需求: {(energy_assessment?.renewable_potential?.wind_potential?.land_requirement / 10000).toFixed(1)} 公顷</Text>
              </div>
            </div>
          </Col>
        </Row>
      </Card>

      {/* 储能系统评估 */}
      <Card title="储能系统评估" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={12}>
            <Title level={4}>储能需求分析</Title>
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <Text>应急备用电源</Text>
                <Text strong>{energy_assessment?.storage_assessment?.storage_needs?.emergency_backup?.toFixed(0)} MWh</Text>
              </div>
              <Progress 
                percent={25} 
                strokeColor="#52c41a" 
                size="small"
              />
            </div>
            
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <Text>削峰填谷</Text>
                <Text strong>{energy_assessment?.storage_assessment?.storage_needs?.peak_shaving?.toFixed(0)} MWh</Text>
              </div>
              <Progress 
                percent={50} 
                strokeColor="#1890ff" 
                size="small"
              />
            </div>
            
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <Text>电网稳定</Text>
                <Text strong>{energy_assessment?.storage_assessment?.storage_needs?.grid_stabilization?.toFixed(0)} MWh</Text>
              </div>
              <Progress 
                percent={15} 
                strokeColor="#faad14" 
                size="small"
              />
            </div>
            
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <Text>总储能需求</Text>
                <Text strong style={{ fontSize: '16px', color: '#1890ff' }}>
                  {energy_assessment?.storage_assessment?.storage_needs?.total_required?.toFixed(0)} MWh
                </Text>
              </div>
              <Progress 
                percent={100} 
                strokeColor="#ff7875" 
                size="small"
              />
            </div>
          </Col>
          <Col span={12}>
            <Title level={4}>推荐储能技术</Title>
            <Table
              columns={storageColumns}
              dataSource={energy_assessment?.storage_assessment?.recommended_technologies || []}
              pagination={false}
              size="small"
            />
          </Col>
        </Row>
      </Card>

      {/* 电网接入评估 */}
      <Card title="电网接入评估">
        <Row gutter={16}>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <Title level={4}>可用容量</Title>
                <Text strong style={{ fontSize: '24px', color: '#1890ff' }}>
                  {energy_assessment?.grid_assessment?.available_capacity} MW
                </Text>
              </div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <Title level={4}>电压等级</Title>
                <Text strong style={{ fontSize: '18px' }}>
                  {energy_assessment?.grid_assessment?.voltage_level}
                </Text>
              </div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <Title level={4}>电网稳定性</Title>
                <Tag 
                  color={
                    energy_assessment?.grid_assessment?.grid_stability === '充足' ? 'green' :
                    energy_assessment?.grid_assessment?.grid_stability === '良好' ? 'blue' :
                    energy_assessment?.grid_assessment?.grid_stability === '紧张' ? 'orange' : 'red'
                  }
                  style={{ fontSize: '14px' }}
                >
                  {energy_assessment?.grid_assessment?.grid_stability}
                </Tag>
              </div>
            </Card>
          </Col>
        </Row>
        
        {energy_assessment?.recommendations && (
          <div style={{ marginTop: 16 }}>
            <Title level={4}>能源配置建议</Title>
            {energy_assessment.recommendations.map((recommendation: string, index: number) => (
              <div key={index} style={{ 
                padding: '8px 12px', 
                marginBottom: '8px', 
                background: '#f6ffed', 
                border: '1px solid #b7eb8f', 
                borderRadius: '4px' 
              }}>
                <Text>{recommendation}</Text>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export default EnergyAssessment;
