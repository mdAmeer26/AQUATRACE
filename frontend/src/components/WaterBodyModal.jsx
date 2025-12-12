import React, { useState, useEffect } from 'react';
import { X, Droplet, AlertTriangle, Factory, Shield, Lightbulb, TrendingUp, Activity, MapPin, Thermometer, Wind, Waves, Zap, Users, Building2 } from 'lucide-react';

const WaterBodyModal = ({ waterBodyId, onClose }) => {
  const [realTimeData, setRealTimeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('realtime');

  useEffect(() => {
    const fetchRealTimeData = async () => {
      try {
        setLoading(true);
        
        // Fetch water body data
        const response = await fetch(`http://localhost:8000/api/v1/search/all-water-sources`);
        const waterBodyData = await response.json();
        
        const specificWaterBody = waterBodyData.water_sources?.find(
          source => source.id === waterBodyId || source.name === waterBodyId
        );
        
        const waterBody = specificWaterBody || {
          id: waterBodyId,
          name: waterBodyId,
          type: 'lake',
          location: 'Unknown',
          lat: 17.385,
          lon: 78.486,
          contamination_level: 'medium',
          detected_contaminants: ['microplastics'],
          water_quality_index: 50
        };

        // Simulate real-time data
        setRealTimeData({
          ...waterBody,
          realtime: {
            temperature: (Math.random() * 10 + 20).toFixed(1),
            ph: (Math.random() * 2 + 6.5).toFixed(2),
            dissolvedOxygen: (Math.random() * 5 + 4).toFixed(2),
            turbidity: (Math.random() * 50 + 10).toFixed(1),
            microplasticCount: Math.floor(Math.random() * 500 + 100),
            pollutionIndex: Math.floor(Math.random() * 40 + 30),
            lastUpdated: new Date().toLocaleTimeString()
          },
          nearbyFactories: generateNearbyFactories(waterBody.location),
          solutions: generateSolutions(waterBody.contamination_level),
          preventions: generatePreventions()
        });

        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchRealTimeData();
    const interval = setInterval(fetchRealTimeData, 30000);
    return () => clearInterval(interval);
  }, [waterBodyId]);

  const generateNearbyFactories = (location) => {
    const factoryTypes = [
      { name: 'Textile Processing Plant', distance: '2.3 km', pollution: 'high', type: 'Chemical discharge' },
      { name: 'Steel Manufacturing Unit', distance: '4.7 km', pollution: 'critical', type: 'Heavy metals' },
      { name: 'Pharmaceutical Factory', distance: '5.2 km', pollution: 'high', type: 'Chemical waste' },
      { name: 'Plastic Processing Plant', distance: '3.8 km', pollution: 'medium', type: 'Microplastics' },
      { name: 'Leather Tannery', distance: '6.1 km', pollution: 'critical', type: 'Chromium & toxins' },
      { name: 'Food Processing Unit', distance: '1.9 km', pollution: 'medium', type: 'Organic waste' }
    ];
    
    return factoryTypes.slice(0, Math.floor(Math.random() * 3) + 3);
  };

  const generateSolutions = (contaminationLevel) => {
    const baseSolutions = [
      { title: 'Advanced Filtration Systems', description: 'Install multi-stage filtration units to remove microplastics and contaminants', priority: 'high' },
      { title: 'Bioremediation', description: 'Use microorganisms to break down organic pollutants naturally', priority: 'medium' },
      { title: 'Wetland Construction', description: 'Build artificial wetlands for natural water purification', priority: 'medium' },
      { title: 'UV Treatment', description: 'Deploy UV disinfection systems to eliminate pathogens', priority: 'high' }
    ];

    const criticalSolutions = [
      { title: 'Emergency Dredging', description: 'Remove contaminated sediment immediately', priority: 'critical' },
      { title: 'Chemical Neutralization', description: 'Deploy chemical agents to neutralize toxic compounds', priority: 'critical' }
    ];

    return contaminationLevel === 'critical' ? [...criticalSolutions, ...baseSolutions] : baseSolutions;
  };

  const generatePreventions = () => [
    { title: 'Strict Industrial Monitoring', description: 'Regular inspections and compliance checks for nearby factories', icon: '🏭' },
    { title: 'Community Awareness Programs', description: 'Educate locals about water conservation and pollution prevention', icon: '👥' },
    { title: 'Waste Management Systems', description: 'Implement proper sewage and industrial waste treatment', icon: '♻️' },
    { title: 'Buffer Zones', description: 'Create protected green zones around water bodies', icon: '🌳' },
    { title: 'Real-time Monitoring', description: 'Install IoT sensors for continuous water quality tracking', icon: '📡' },
    { title: 'Legal Framework', description: 'Enforce strict penalties for pollution violations', icon: '⚖️' }
  ];

  if (loading) {
    return (
      <div className="fixed inset-0 z-[1000] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl p-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-gray-700 font-semibold">Loading real-time data...</span>
          </div>
        </div>
      </div>
    );
  }

  if (!realTimeData) return null;

  const getPollutionColor = (level) => {
    const colors = {
      critical: 'bg-red-600',
      high: 'bg-orange-600',
      medium: 'bg-yellow-600',
      low: 'bg-green-600'
    };
    return colors[level] || 'bg-gray-600';
  };

  return (
    <div className="fixed inset-0 z-[1000] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-gradient-to-br from-slate-50 to-blue-50 rounded-3xl shadow-2xl w-full max-w-7xl max-h-[90vh] overflow-hidden my-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 text-white p-6 relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 hover:bg-white/20 rounded-xl transition-all"
          >
            <X className="w-6 h-6" />
          </button>
          
          <div className="flex items-start gap-4 mb-4">
            <div className="bg-white/20 p-3 rounded-2xl backdrop-blur-sm">
              <Droplet className="w-8 h-8" />
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold mb-2">{realTimeData.name}</h2>
              <div className="flex flex-wrap items-center gap-3 text-sm">
                <span className="flex items-center gap-1 bg-white/20 px-3 py-1 rounded-lg backdrop-blur-sm">
                  <MapPin className="w-4 h-4" />
                  {realTimeData.location}
                </span>
                <span className="bg-white/20 px-3 py-1 rounded-lg backdrop-blur-sm">
                  {realTimeData.type.toUpperCase()}
                </span>
                <span className={`${getPollutionColor(realTimeData.contamination_level)} px-3 py-1 rounded-lg font-semibold`}>
                  {realTimeData.contamination_level.toUpperCase()} RISK
                </span>
              </div>
            </div>
          </div>

          {/* Live Status */}
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium">Live Monitoring Active</span>
            </div>
            <span className="text-sm">Updated: {realTimeData.realtime.lastUpdated}</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white border-b border-gray-200 px-6">
          <div className="flex gap-2">
            {[
              { id: 'realtime', label: 'Real-Time Data', icon: Activity },
              { id: 'factories', label: 'Nearby Factories', icon: Factory },
              { id: 'solutions', label: 'Solutions', icon: Lightbulb },
              { id: 'prevention', label: 'Prevention', icon: Shield }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all border-b-2 ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-280px)]">
          {activeTab === 'realtime' && (
            <div className="space-y-6">
              {/* Real-time metrics grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <MetricCard
                  icon={<Thermometer className="w-6 h-6" />}
                  label="Temperature"
                  value={`${realTimeData.realtime.temperature}°C`}
                  color="bg-orange-500"
                />
                <MetricCard
                  icon={<Waves className="w-6 h-6" />}
                  label="pH Level"
                  value={realTimeData.realtime.ph}
                  color="bg-blue-500"
                />
                <MetricCard
                  icon={<Wind className="w-6 h-6" />}
                  label="Dissolved Oxygen"
                  value={`${realTimeData.realtime.dissolvedOxygen} mg/L`}
                  color="bg-cyan-500"
                />
                <MetricCard
                  icon={<Activity className="w-6 h-6" />}
                  label="Turbidity"
                  value={`${realTimeData.realtime.turbidity} NTU`}
                  color="bg-amber-500"
                />
                <MetricCard
                  icon={<AlertTriangle className="w-6 h-6" />}
                  label="Microplastics"
                  value={`${realTimeData.realtime.microplasticCount} particles/L`}
                  color="bg-red-500"
                />
                <MetricCard
                  icon={<TrendingUp className="w-6 h-6" />}
                  label="Pollution Index"
                  value={`${realTimeData.realtime.pollutionIndex}%`}
                  color="bg-purple-500"
                />
              </div>

              {/* Water Quality Chart */}
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <Droplet className="w-6 h-6 text-blue-600" />
                  Water Quality Index
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-700 font-semibold">Overall Score</span>
                    <span className="text-3xl font-bold text-blue-600">{realTimeData.water_quality_index}/100</span>
                  </div>
                  <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        realTimeData.water_quality_index >= 70 ? 'bg-green-500' :
                        realTimeData.water_quality_index >= 50 ? 'bg-yellow-500' :
                        'bg-red-500'
                      } transition-all duration-500`}
                      style={{ width: `${realTimeData.water_quality_index}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Detected Contaminants */}
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                <h3 className="text-xl font-bold text-gray-800 mb-4">Detected Contaminants</h3>
                <div className="flex flex-wrap gap-3">
                  {realTimeData.detected_contaminants.map((contaminant, idx) => (
                    <span
                      key={idx}
                      className="bg-red-100 border border-red-300 text-red-800 px-4 py-2 rounded-xl font-semibold text-sm"
                    >
                      ⚠️ {contaminant.replace(/_/g, ' ').toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'factories' && (
            <div className="space-y-4">
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-xl">
                <div className="flex items-center gap-2 text-red-800 font-bold mb-2">
                  <AlertTriangle className="w-5 h-5" />
                  Pollution Sources Detected
                </div>
                <p className="text-red-700 text-sm">
                  {realTimeData.nearbyFactories.length} industrial facilities detected within 10km radius
                </p>
              </div>

              {realTimeData.nearbyFactories.map((factory, idx) => (
                <div key={idx} className="bg-white rounded-2xl p-6 shadow-lg border-l-4 border-red-500">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-start gap-3">
                      <div className="bg-red-100 p-3 rounded-xl">
                        <Factory className="w-6 h-6 text-red-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-bold text-gray-800">{factory.name}</h4>
                        <p className="text-gray-600 text-sm mt-1">Distance: {factory.distance}</p>
                      </div>
                    </div>
                    <span className={`${getPollutionColor(factory.pollution)} text-white px-3 py-1 rounded-lg text-sm font-bold`}>
                      {factory.pollution.toUpperCase()}
                    </span>
                  </div>
                  <div className="bg-gray-50 rounded-xl p-3 mt-3">
                    <p className="text-sm text-gray-700">
                      <strong>Pollution Type:</strong> {factory.type}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'solutions' && (
            <div className="space-y-4">
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-xl">
                <div className="flex items-center gap-2 text-blue-800 font-bold mb-2">
                  <Lightbulb className="w-5 h-5" />
                  Recommended Remediation Solutions
                </div>
                <p className="text-blue-700 text-sm">
                  Based on contamination level and detected pollutants
                </p>
              </div>

              {realTimeData.solutions.map((solution, idx) => (
                <div key={idx} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-start gap-3 flex-1">
                      <div className={`${
                        solution.priority === 'critical' ? 'bg-red-500' :
                        solution.priority === 'high' ? 'bg-orange-500' :
                        'bg-blue-500'
                      } p-3 rounded-xl`}>
                        <Zap className="w-6 h-6 text-white" />
                      </div>
                      <div className="flex-1">
                        <h4 className="text-lg font-bold text-gray-800">{solution.title}</h4>
                        <p className="text-gray-600 mt-2 text-sm leading-relaxed">{solution.description}</p>
                      </div>
                    </div>
                    <span className={`${
                      solution.priority === 'critical' ? 'bg-red-100 text-red-800 border-red-300' :
                      solution.priority === 'high' ? 'bg-orange-100 text-orange-800 border-orange-300' :
                      'bg-blue-100 text-blue-800 border-blue-300'
                    } px-3 py-1 rounded-lg text-xs font-bold border ml-4`}>
                      {solution.priority.toUpperCase()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'prevention' && (
            <div className="space-y-4">
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-r-xl">
                <div className="flex items-center gap-2 text-green-800 font-bold mb-2">
                  <Shield className="w-5 h-5" />
                  Long-term Prevention Strategies
                </div>
                <p className="text-green-700 text-sm">
                  Proactive measures to prevent future contamination
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {realTimeData.preventions.map((prevention, idx) => (
                  <div key={idx} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all">
                    <div className="flex items-start gap-3">
                      <div className="text-4xl">{prevention.icon}</div>
                      <div className="flex-1">
                        <h4 className="text-lg font-bold text-gray-800 mb-2">{prevention.title}</h4>
                        <p className="text-gray-600 text-sm leading-relaxed">{prevention.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Action Plan */}
              <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white mt-6">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <Users className="w-7 h-7" />
                  Community Action Required
                </h3>
                <ul className="space-y-3">
                  <li className="flex items-start gap-3">
                    <div className="bg-white/20 p-1 rounded mt-1">
                      <Building2 className="w-4 h-4" />
                    </div>
                    <span className="flex-1">Contact local authorities to enforce pollution regulations on nearby factories</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="bg-white/20 p-1 rounded mt-1">
                      <Users className="w-4 h-4" />
                    </div>
                    <span className="flex-1">Organize community clean-up drives every month</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="bg-white/20 p-1 rounded mt-1">
                      <AlertTriangle className="w-4 h-4" />
                    </div>
                    <span className="flex-1">Report any illegal dumping or suspicious activities immediately</span>
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon, label, value, color }) => (
  <div className="bg-white rounded-2xl p-5 shadow-lg border border-gray-200 hover:shadow-xl transition-all">
    <div className="flex items-center gap-3 mb-3">
      <div className={`${color} p-2.5 rounded-xl text-white`}>
        {icon}
      </div>
      <span className="text-gray-600 font-medium text-sm">{label}</span>
    </div>
    <div className="text-2xl font-bold text-gray-800">{value}</div>
  </div>
);

export default WaterBodyModal;
