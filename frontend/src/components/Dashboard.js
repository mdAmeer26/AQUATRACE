import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = ({ statistics, alerts, loading }) => {
  const [trendData, setTrendData] = useState(null);

  useEffect(() => {
    // Generate mock trend data
    generateTrendData();
  }, []);

  const generateTrendData = () => {
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const data = {
      labels,
      datasets: [
        {
          label: 'Average Concentration',
          data: [0.42, 0.45, 0.48, 0.51, 0.53, 0.55, 0.58, 0.56, 0.54, 0.52, 0.49, 0.46],
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    };
    setTrendData(data);
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#ffffff'
        }
      },
      title: {
        display: true,
        text: 'Global Microplastic Concentration Trend (2025)',
        color: '#ffffff',
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        ticks: { color: '#9ca3af' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      },
      x: {
        ticks: { color: '#9ca3af' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard-container p-6 overflow-y-auto bg-gray-900 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Global Ocean Monitoring Dashboard</h1>
          <p className="text-gray-400">Real-time microplastic concentration statistics and trends</p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white text-sm font-semibold">Global Average</h3>
              <span className="text-2xl">🌍</span>
            </div>
            <p className="text-3xl font-bold text-white">
              {((statistics?.global_average || 0.52) * 100).toFixed(1)}%
            </p>
            <p className="text-blue-200 text-sm mt-2">Concentration Level</p>
          </div>

          <div className="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white text-sm font-semibold">Area Monitored</h3>
              <span className="text-2xl">📊</span>
            </div>
            <p className="text-3xl font-bold text-white">
              {(statistics?.total_area_monitored_km2 || 285000000).toLocaleString()}
            </p>
            <p className="text-green-200 text-sm mt-2">km² of ocean</p>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white text-sm font-semibold">Alert Zones</h3>
              <span className="text-2xl">⚠️</span>
            </div>
            <p className="text-3xl font-bold text-white">
              {statistics?.high_concentration_zones || alerts.length || 12}
            </p>
            <p className="text-orange-200 text-sm mt-2">High concentration areas</p>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white text-sm font-semibold">Trend</h3>
              <span className="text-2xl">📈</span>
            </div>
            <p className="text-3xl font-bold text-white">
              {statistics?.trend === 'increasing' ? '↗' : statistics?.trend === 'decreasing' ? '↘' : '→'}
            </p>
            <p className="text-purple-200 text-sm mt-2">
              {statistics?.trend || 'Stable'}
            </p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Trend Chart */}
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <div style={{ height: '300px' }}>
              {trendData && (
                <Line data={trendData} options={chartOptions} />
              )}
            </div>
          </div>

          {/* Regional Breakdown */}
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-white text-lg font-semibold mb-4">Regional Hotspots</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">North Pacific Gyre</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div className="bg-red-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                  <span className="text-white font-semibold">85%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">North Atlantic Gyre</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div className="bg-orange-500 h-2 rounded-full" style={{ width: '72%' }}></div>
                  </div>
                  <span className="text-white font-semibold">72%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Mediterranean Sea</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '68%' }}></div>
                  </div>
                  <span className="text-white font-semibold">68%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Indian Ocean Gyre</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '58%' }}></div>
                  </div>
                  <span className="text-white font-semibold">58%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">South Pacific Gyre</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                  </div>
                  <span className="text-white font-semibold">45%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Data Sources */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h3 className="text-white text-lg font-semibold mb-4">Data Sources</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-start space-x-3">
              <div className="text-2xl">🛰️</div>
              <div>
                <h4 className="text-white font-semibold">NASA CYGNSS</h4>
                <p className="text-sm text-gray-400">GPS signal reflectometry</p>
                <p className="text-xs text-green-400 mt-1">● Active</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="text-2xl">🌐</div>
              <div>
                <h4 className="text-white font-semibold">ESA Sentinel-2</h4>
                <p className="text-sm text-gray-400">Optical imagery</p>
                <p className="text-xs text-green-400 mt-1">● Active</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="text-2xl">🌊</div>
              <div>
                <h4 className="text-white font-semibold">Copernicus Marine</h4>
                <p className="text-sm text-gray-400">Oceanographic data</p>
                <p className="text-xs text-green-400 mt-1">● Active</p>
              </div>
            </div>
          </div>
        </div>

        {/* Last Updated */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          Last updated: {statistics?.last_updated ? new Date(statistics.last_updated).toLocaleString() : new Date().toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
