import React, { useState } from 'react';
import './App.css';

interface AnalysisData {
  location: { latitude: number; longitude: number };
  land_analysis: any;
  energy_assessment: any;
  decision_recommendation: any;
  heat_utilization: any;
  geographic_environment: any;
  power_supply_analysis: any;
  energy_storage_analysis: any;
  promethee_mcgp_analysis: any;
}

const App: React.FC = () => {
  // 添加内联样式
  const styles = `
    .result-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    
    .result-section {
      background: #f8f9fa;
      border: 1px solid #e9ecef;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .satellite-section {
      grid-column: 1 / -1;
    }
    
    .satellite-image {
      margin: 10px 0;
      position: relative;
      overflow: hidden;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .satellite-image img {
      transition: transform 0.3s ease;
    }
    
    .satellite-image:hover img {
      transform: scale(1.02);
    }
    
    .image-caption {
      font-size: 12px;
      color: #666;
      text-align: center;
      margin-top: 5px;
    }
    
    .result-content p {
      margin: 8px 0;
      padding: 5px 0;
      border-bottom: 1px solid #eee;
    }
    
    .result-content p:last-child {
      border-bottom: none;
    }
  `;
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState<{lat: number, lng: number} | null>(null);

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

  const handleAnalyze = async (lat: number, lng: number) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/analyze/location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: lat,
          longitude: lng,
          radius: 1000
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisData(data);
        alert('分析完成！');
      } else {
        throw new Error('分析失败');
      }
    } catch (error) {
      alert('分析失败，请重试');
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <style>{styles}</style>
      <header className="App-header">
        <h1>数据中心智能选址与能源优化系统</h1>
        <p>基于真实GEE数据的智能分析平台</p>
      </header>

      <main className="App-main">
        <div className="location-section">
          <h2>位置选择</h2>
          <div className="city-buttons">
            {cities.map(city => (
              <button
                key={city.name}
                onClick={() => {
                  setSelectedLocation({ lat: city.lat, lng: city.lng });
                  handleAnalyze(city.lat, city.lng);
                }}
                disabled={loading}
                className="city-button"
              >
                {city.name}
              </button>
            ))}
          </div>
          
          {selectedLocation && (
            <div className="selected-location">
              <p>已选择位置: {selectedLocation.lat.toFixed(4)}, {selectedLocation.lng.toFixed(4)}</p>
            </div>
          )}
        </div>

        {loading && (
          <div className="loading">
            <p>正在分析中，请稍候...</p>
          </div>
        )}

        {analysisData && (
          <div className="analysis-results">
            <h2>分析结果</h2>
            
            <div className="result-grid">
              <div className="result-section">
                <h3>土地利用分析</h3>
                <div className="result-content">
                  <p><strong>总面积:</strong> {analysisData.land_analysis.total_area?.toLocaleString()} 平方米</p>
                  <p><strong>分析日期:</strong> {new Date(analysisData.land_analysis.analysis_date).toLocaleString()}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>能源资源评估</h3>
                <div className="result-content">
                  <p><strong>太阳能年辐射量:</strong> {analysisData.energy_assessment.solar_data?.annual_irradiance} kWh/m²</p>
                  <p><strong>平均风速:</strong> {analysisData.energy_assessment.wind_data?.average_speed} m/s</p>
                  <p><strong>可再生能源覆盖率:</strong> {(analysisData.energy_assessment.storage_assessment?.renewable_coverage * 100)?.toFixed(1)}%</p>
                </div>
              </div>

              <div className="result-section">
                <h3>地理环境分析</h3>
                <div className="result-content">
                  <p><strong>海拔:</strong> {analysisData.geographic_environment?.elevation} 米</p>
                  <p><strong>森林覆盖率:</strong> {analysisData.geographic_environment?.forest_coverage}%</p>
                  <p><strong>气候带:</strong> {analysisData.geographic_environment?.climate_zone}</p>
                  <p><strong>水资源:</strong> {analysisData.geographic_environment?.water_resources?.total_capacity}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>决策分析</h3>
                <div className="result-content">
                  <p><strong>综合评分:</strong> {analysisData.decision_recommendation.overall_score?.score} 分</p>
                  <p><strong>决策等级:</strong> {analysisData.decision_recommendation.decision_level}</p>
                  <p><strong>风险等级:</strong> {analysisData.decision_recommendation.risk_assessment?.risk_level}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>余热利用分析</h3>
                <div className="result-content">
                  <p><strong>可回收热量:</strong> {analysisData.heat_utilization.recoverable_heat_mw} MW</p>
                  <p><strong>年收益:</strong> {analysisData.heat_utilization.economic_benefits?.annual_revenue?.toLocaleString()} 元</p>
                  <p><strong>投资回收期:</strong> {analysisData.heat_utilization.economic_benefits?.payback_period} 年</p>
                </div>
              </div>

        <div className="result-section satellite-section">
          <h3>卫星图像</h3>
          <div className="satellite-image">
            <img 
              src={analysisData.geographic_environment?.satellite_image_url} 
              alt="卫星图像" 
              style={{
                width: '100%', 
                height: '500px', 
                objectFit: 'cover', 
                borderRadius: '8px',
                imageRendering: 'high-quality' as any
              }}
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.src = `https://via.placeholder.com/400x600/4CAF50/FFFFFF?text=位置: ${analysisData.location?.latitude?.toFixed(2)}, ${analysisData.location?.longitude?.toFixed(2)}`;
              }}
            />
          </div>
          <p className="image-caption">
            基于GEE的高分辨率卫星图像<br/>
            Landsat 8/9数据 | 覆盖半径: 20公里 | 实时更新
          </p>
        </div>

        {/* 供电方案分析 */}
        <div className="result-section">
          <h3>供电方案分析</h3>
          <div className="result-content">
            {analysisData.power_supply_analysis?.recommended_options?.map((option: any, index: number) => (
              <div key={index} className="option-item">
                <h4>{option.name}</h4>
                <p>装机容量: {option.capacity?.toFixed(1)} MW</p>
                <p>效率: {(option.efficiency * 100)?.toFixed(1)}%</p>
                <p>适用性评分: {(option.suitability_score * 100)?.toFixed(1)}%</p>
                <p>{option.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 储能布局分析 */}
        <div className="result-section">
          <h3>储能布局分析</h3>
          <div className="result-content">
            {analysisData.energy_storage_analysis?.available_options?.map((option: any, index: number) => (
              <div key={index} className="option-item">
                <h4>{option.name}</h4>
                <p>储能容量: {option.capacity?.toFixed(1)} MWh</p>
                <p>功率: {option.power?.toFixed(1)} MW</p>
                <p>效率: {(option.efficiency * 100)?.toFixed(1)}%</p>
                <p>适用性评分: {(option.suitability_score * 100)?.toFixed(1)}%</p>
                <p>{option.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* PROMETHEE-MCGP决策分析 */}
        <div className="result-section">
          <h3>PROMETHEE-MCGP决策分析</h3>
          <div className="result-content">
            <div className="decision-summary">
              <h4>综合评分: {analysisData.promethee_mcgp_analysis?.final_ranking?.final_score}</h4>
              <p>等级: {analysisData.promethee_mcgp_analysis?.final_ranking?.level}</p>
              <p>推荐: {analysisData.promethee_mcgp_analysis?.final_ranking?.recommendation}</p>
            </div>
            <div className="economic-analysis">
              <h4>经济因素分析</h4>
              <p>评分: {analysisData.promethee_mcgp_analysis?.economic_analysis?.ranking?.score}</p>
              <p>等级: {analysisData.promethee_mcgp_analysis?.economic_analysis?.ranking?.level}</p>
            </div>
            <div className="recommendations">
              <h4>建议</h4>
              {analysisData.promethee_mcgp_analysis?.recommendation?.recommendations?.map((rec: string, index: number) => (
                <p key={index}>• {rec}</p>
              ))}
            </div>
          </div>
        </div>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>© 2024 数据中心智能选址与能源优化系统 - 使用真实GEE数据</p>
      </footer>
    </div>
  );
};

export default App;
