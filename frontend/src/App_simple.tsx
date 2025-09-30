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
    .custom-input-section {
      background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
      backdrop-filter: blur(10px);
      padding: 25px;
      border-radius: 15px;
      margin: 20px auto;
      max-width: 800px;
      border: 1px solid rgba(255,255,255,0.2);
      box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .input-row {
      display: flex;
      gap: 15px;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 15px;
    }
    
    .input-group {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 5px;
    }
    
    .input-label {
      color: #fff;
      font-size: 14px;
      font-weight: 500;
    }
    
    .input-field {
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.3);
      background: rgba(255,255,255,0.1);
      color: #fff;
      font-size: 14px;
      width: 120px;
      text-align: center;
    }
    
    .input-field::placeholder {
      color: rgba(255,255,255,0.6);
    }
    
    .input-field:focus {
      outline: none;
      border-color: #61dafb;
      box-shadow: 0 0 0 2px rgba(97, 218, 251, 0.2);
    }
    
    .analyze-button {
      padding: 10px 20px;
      background: linear-gradient(45deg, #61dafb, #21a0c4);
      color: #000;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
      font-size: 14px;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(97, 218, 251, 0.3);
    }
    
    .analyze-button:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(97, 218, 251, 0.4);
    }
    
    .analyze-button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    
    .area-info {
      font-size: 13px;
      color: rgba(255,255,255,0.8);
      text-align: center;
      margin-top: 10px;
      padding: 8px;
      background: rgba(255,255,255,0.1);
      border-radius: 6px;
    }
    
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
      order: -1;
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
  const [customLat, setCustomLat] = useState<string>('');
  const [customLng, setCustomLng] = useState<string>('');
  const [customRadius, setCustomRadius] = useState<number>(1000);

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

  const handleAnalyze = async (lat: number, lng: number, radius: number = 1000) => {
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
          radius: radius
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
        
        {/* 自定义坐标输入区域 */}
        <div className="custom-input-section">
          <h3 style={{ margin: '0 0 20px 0', color: '#fff', textAlign: 'center', fontSize: '18px' }}>
            🎯 自定义选址分析
          </h3>
          
          <div className="input-row">
            <div className="input-group">
              <label className="input-label">纬度</label>
              <input 
                type="number" 
                step="0.0001"
                placeholder="39.9042"
                value={customLat}
                onChange={(e) => setCustomLat(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div className="input-group">
              <label className="input-label">经度</label>
              <input 
                type="number" 
                step="0.0001"
                placeholder="116.4074"
                value={customLng}
                onChange={(e) => setCustomLng(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div className="input-group">
              <label className="input-label">分析半径</label>
              <select 
                value={customRadius}
                onChange={(e) => setCustomRadius(Number(e.target.value))}
                className="input-field"
                style={{ width: '140px' }}
              >
                <option value={500}>500米</option>
                <option value={1000}>1000米</option>
                <option value={2000}>2000米</option>
                <option value={5000}>5000米</option>
                <option value={10000}>10000米</option>
              </select>
            </div>
            
            <button 
              onClick={() => {
                if (customLat && customLng) {
                  const lat = parseFloat(customLat);
                  const lng = parseFloat(customLng);
                  if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
                    handleAnalyze(lat, lng, customRadius);
                  } else {
                    alert('请输入有效的坐标范围：纬度(-90到90)，经度(-180到180)');
                  }
                } else {
                  alert('请输入纬度和经度');
                }
              }}
              disabled={loading}
              className="analyze-button"
            >
              {loading ? '分析中...' : '🚀 开始分析'}
            </button>
          </div>
          
          <div className="area-info">
            💡 分析面积: {Math.round(Math.PI * (customRadius/1000) ** 2 * 100) / 100} 平方公里
          </div>
        </div>
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
              {/* 卫星图像 - 放在最前面 */}
              <div className="result-section satellite-section">
                <h3>🛰️ 卫星图像</h3>
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
                  Landsat 8/9数据 | 覆盖半径: {analysisData.geographic_environment?.satellite_image_metadata?.coverage_radius || `${customRadius/1000}公里`} | 实时更新
                </p>
              </div>

              <div className="result-section">
                <h3>🏗️ 土地利用分析</h3>
                <div className="result-content">
                  <p><strong>总面积:</strong> {analysisData.land_analysis.total_area?.toLocaleString()} 平方米</p>
                  <p><strong>分析日期:</strong> {new Date(analysisData.land_analysis.analysis_date).toLocaleString()}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>⚡ 能源资源评估</h3>
                <div className="result-content">
                  <p><strong>太阳能年辐射量:</strong> {analysisData.energy_assessment.solar_data?.annual_irradiance} kWh/m²</p>
                  <p><strong>平均风速:</strong> {analysisData.energy_assessment.wind_data?.average_speed} m/s</p>
                  <p><strong>可再生能源覆盖率:</strong> {(analysisData.energy_assessment.storage_assessment?.renewable_coverage * 100)?.toFixed(1)}%</p>
                </div>
              </div>

              <div className="result-section">
                <h3>🌍 地理环境分析</h3>
                <div className="result-content">
                  <p><strong>海拔:</strong> {analysisData.geographic_environment?.elevation} 米</p>
                  <p><strong>森林覆盖率:</strong> {analysisData.geographic_environment?.forest_coverage}%</p>
                  <p><strong>气候带:</strong> {analysisData.geographic_environment?.climate_zone}</p>
                  <p><strong>水资源:</strong> {analysisData.geographic_environment?.water_resources?.total_capacity}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>🎯 决策分析</h3>
                <div className="result-content">
                  <p><strong>综合评分:</strong> {analysisData.decision_recommendation.overall_score?.score} 分</p>
                  <p><strong>决策等级:</strong> {analysisData.decision_recommendation.decision_level}</p>
                  <p><strong>风险等级:</strong> {analysisData.decision_recommendation.risk_assessment?.risk_level}</p>
                </div>
              </div>

              <div className="result-section">
                <h3>🌡️ 余热利用分析</h3>
                <div className="result-content">
                  <p><strong>可回收热量:</strong> {analysisData.heat_utilization.recoverable_heat_mw} MW</p>
                  <p><strong>年收益:</strong> {analysisData.heat_utilization.economic_benefits?.annual_revenue?.toLocaleString()} 元</p>
                  <p><strong>投资回收期:</strong> {analysisData.heat_utilization.economic_benefits?.payback_period} 年</p>
                </div>
              </div>

        {/* 供电方案分析 */}
        <div className="result-section">
          <h3>🔌 供电方案分析</h3>
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
          <h3>🔋 储能布局分析</h3>
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
          <h3>🧠 PROMETHEE-MCGP决策分析</h3>
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
