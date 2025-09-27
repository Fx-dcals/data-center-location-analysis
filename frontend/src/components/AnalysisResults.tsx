import React from 'react';
import { Card, Row, Col, Typography, Progress, Tag, List, Divider } from 'antd';
import { 
  EnvironmentOutlined, 
  ThunderboltOutlined, 
  BulbOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

interface AnalysisResultsProps {
  data: any;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data }) => {
  if (!data) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <ExclamationCircleOutlined style={{ fontSize: '48px', color: '#ccc' }} />
          <Title level={4} style={{ color: '#ccc', marginTop: '16px' }}>
            暂无分析数据
          </Title>
          <Text type="secondary">请先在地图上选择位置并进行分析</Text>
        </div>
      </Card>
    );
  }

  const { land_analysis, energy_assessment, decision_recommendation, heat_utilization } = data;

  const getScoreColor = (score: number) => {
    if (score >= 90) return '#52c41a';
    if (score >= 75) return '#1890ff';
    if (score >= 60) return '#faad14';
    if (score >= 45) return '#ff7875';
    return '#f5222d';
  };

  const getScoreLevel = (score: number) => {
    if (score >= 90) return '优秀';
    if (score >= 75) return '良好';
    if (score >= 60) return '一般';
    if (score >= 45) return '较差';
    return '很差';
  };

  return (
    <div>
      <Title level={2}>分析结果总览</Title>
      
      {/* 土地利用分析 */}
      <Card title="土地利用分析" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={12}>
            <Title level={4}>土地类型分布</Title>
            {land_analysis?.land_use_distribution && Object.entries(land_analysis.land_use_distribution).map(([type, ratio]: [string, any]) => (
              <div key={type} style={{ marginBottom: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <Text>{type}</Text>
                  <Text strong>{(ratio * 100).toFixed(1)}%</Text>
                </div>
                <Progress 
                  percent={ratio * 100} 
                  size="small" 
                  strokeColor={getScoreColor(ratio * 100)}
                />
              </div>
            ))}
          </Col>
          <Col span={12}>
            <Title level={4}>适宜区域</Title>
            {land_analysis?.suitable_areas?.map((area: any, index: number) => (
              <Card key={index} size="small" style={{ marginBottom: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Text strong>{area.type}</Text>
                  <Tag color={getScoreColor(area.suitability_score * 100)}>
                    {getScoreLevel(area.suitability_score * 100)}
                  </Tag>
                </div>
                <Text type="secondary">面积占比: {(area.area_ratio * 100).toFixed(1)}%</Text>
              </Card>
            ))}
          </Col>
        </Row>
        
        {land_analysis?.recommendations && (
          <div style={{ marginTop: 16 }}>
            <Title level={4}>土地利用建议</Title>
            <List
              dataSource={land_analysis.recommendations}
              renderItem={(item: string) => (
                <List.Item>
                  <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                  {item}
                </List.Item>
              )}
            />
          </div>
        )}
      </Card>

      {/* 能源资源评估 */}
      <Card title="能源资源评估" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <ThunderboltOutlined style={{ fontSize: '24px', color: '#faad14' }} />
                <Title level={4}>太阳能资源</Title>
                <Text strong>{energy_assessment?.solar_data?.solar_zone}</Text><br />
                <Text>年辐射量: {energy_assessment?.solar_data?.annual_irradiance} kWh/m²</Text><br />
                <Tag color={energy_assessment?.solar_data?.solar_potential === '高' ? 'green' : 'orange'}>
                  {energy_assessment?.solar_data?.solar_potential}
                </Tag>
              </div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <EnvironmentOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
                <Title level={4}>风能资源</Title>
                <Text strong>{energy_assessment?.wind_data?.wind_zone}</Text><br />
                <Text>平均风速: {energy_assessment?.wind_data?.average_speed} m/s</Text><br />
                <Tag color={energy_assessment?.wind_data?.wind_potential === '高' ? 'green' : 'orange'}>
                  {energy_assessment?.wind_data?.wind_potential}
                </Tag>
              </div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <BulbOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
                <Title level={4}>可再生能源潜力</Title>
                <Text strong>
                  {energy_assessment?.renewable_potential?.total_renewable_potential?.annual_generation_mwh?.toFixed(0)} MWh/年
                </Text><br />
                <Text>覆盖率: {(energy_assessment?.storage_assessment?.renewable_coverage * 100).toFixed(1)}%</Text>
              </div>
            </Card>
          </Col>
        </Row>
      </Card>

      {/* 决策分析 */}
      <Card title="决策分析" style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={12}>
            <Title level={4}>综合评分</Title>
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <Progress
                type="circle"
                percent={decision_recommendation?.overall_score?.score || 0}
                strokeColor={getScoreColor(decision_recommendation?.overall_score?.score || 0)}
                format={(percent) => (
                  <div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{percent}</div>
                    <div style={{ fontSize: '12px' }}>
                      {getScoreLevel(decision_recommendation?.overall_score?.score || 0)}
                    </div>
                  </div>
                )}
              />
            </div>
          </Col>
          <Col span={12}>
            <Title level={4}>详细评分</Title>
            {decision_recommendation?.detailed_scores && Object.entries(decision_recommendation.detailed_scores).map(([criterion, score]: [string, any]) => (
              <div key={criterion} style={{ marginBottom: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <Text>{criterion}</Text>
                  <Text strong>{score.score}</Text>
                </div>
                <Progress 
                  percent={score.score} 
                  size="small" 
                  strokeColor={getScoreColor(score.score)}
                />
              </div>
            ))}
          </Col>
        </Row>
        
        <Divider />
        
        <Title level={4}>决策建议</Title>
        <List
          dataSource={decision_recommendation?.recommendations || []}
          renderItem={(item: string) => (
            <List.Item>
              <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
              {item}
            </List.Item>
          )}
        />
      </Card>

      {/* 余热利用分析 */}
      <Card title="余热利用分析">
        <Row gutter={16}>
          <Col span={12}>
            <Title level={4}>可回收热量</Title>
            <Text strong style={{ fontSize: '18px', color: '#1890ff' }}>
              {heat_utilization?.recoverable_heat_mw} MW
            </Text>
            <div style={{ marginTop: 16 }}>
              <Title level={5}>利用方案</Title>
              {heat_utilization?.utilization_options?.map((option: any, index: number) => (
                <Card key={index} size="small" style={{ marginBottom: 8 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text strong>{option.type}</Text>
                    <Tag color={option.feasibility === '高' ? 'green' : 'orange'}>
                      {option.feasibility}
                    </Tag>
                  </div>
                  <Text type="secondary">容量: {option.capacity_mw} MW</Text><br />
                  <Text type="secondary">目标用户: {option.target_users}</Text><br />
                  <Text type="secondary">年收益: {option.economic_value.toLocaleString()} 元</Text>
                </Card>
              ))}
            </div>
          </Col>
          <Col span={12}>
            <Title level={4}>经济效益</Title>
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <Text strong style={{ fontSize: '24px', color: '#52c41a' }}>
                {heat_utilization?.economic_benefits?.annual_revenue?.toLocaleString()} 元/年
              </Text>
              <div style={{ marginTop: 8 }}>
                <Text>投资回收期: {heat_utilization?.economic_benefits?.payback_period} 年</Text><br />
                <Text>CO₂减排: {heat_utilization?.economic_benefits?.co2_reduction?.toFixed(0)} 吨/年</Text>
              </div>
            </div>
            
            <Title level={5}>余热利用建议</Title>
            <List
              dataSource={heat_utilization?.recommendations || []}
              renderItem={(item: string) => (
                <List.Item>
                  <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                  {item}
                </List.Item>
              )}
            />
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default AnalysisResults;
