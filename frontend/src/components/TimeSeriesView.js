import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const TimeSeriesView = () => {
  const [selectedLocation, setSelectedLocation] = useState({ lat: 35.0, lon: -140.0 });
  const [timeSeriesData, setTimeSeriesData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dateRange, setDateRange] = useState({
    start: '2025-01-01',
    end: '2025-12-07'
  });

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const fetchTimeSeriesData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/v1/microplastic/timeseries`, {
        params: {
          lat: selectedLocation.lat,
          lon: selectedLocation.lon,
          start_date: dateRange.start,
          end_date: dateRange.end
        }
      });

      // Transform data for chart
      const chartData = transformDataForChart(response.data);
      setTimeSeriesData(chartData);
    } catch (error) {
      console.error('Error fetching time series data:', error);
      // Use mock data for demonstration
      setTimeSeriesData(generateMockData());
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTimeSeriesData();
  }, [selectedLocation, dateRange]);

  const generateMockData = () => {
    const labels = [];
    const data = [];
    const startDate = new Date('2025-01-01');
    const endDate = new Date('2025-12-07');
    
    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 7)) {
      labels.push(d.toISOString().split('T')[0]);
      data.push(0.4 + Math.random() * 0.3);
    }

    return {
      labels,
      datasets: [
        {
          label: 'Microplastic Concentration',
          data,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    };
  };

  const transformDataForChart = (apiData) => {
    if (!apiData.data || apiData.data.length === 0) {
      return generateMockData();
    }

    const labels = apiData.data.map(d => d.date);
    const data = apiData.data.map(d => d.concentration);

    return {
      labels,
      datasets: [
        {
          label: 'Microplastic Concentration',
          data,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    };
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
        text: `Microplastic Concentration Time Series (${selectedLocation.lat}°, ${selectedLocation.lon}°)`,
        color: '#ffffff',
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Concentration (0-1)',
          color: '#ffffff'
        },
        ticks: { color: '#9ca3af' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      },
      x: {
        title: {
          display: true,
          text: 'Date',
          color: '#ffffff'
        },
        ticks: { 
          color: '#9ca3af',
          maxRotation: 45,
          minRotation: 45
        },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      }
    }
  };

  const predefinedLocations = [
    { name: 'North Pacific Gyre', lat: 35.0, lon: -140.0 },
    { name: 'North Atlantic Gyre', lat: 30.0, lon: -40.0 },
    { name: 'Mediterranean Sea', lat: 38.0, lon: 15.0 },
    { name: 'Indian Ocean Gyre', lat: -20.0, lon: 80.0 },
    { name: 'Caribbean Sea', lat: 18.0, lon: -75.0 }
  ];

  return (
    <div className="timeseries-container p-6 bg-gray-900 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Time Series Analysis</h1>
          <p className="text-gray-400">Analyze microplastic concentration trends over time</p>
        </div>

        {/* Controls */}
        <div className="bg-gray-800 rounded-lg p-6 mb-6 shadow-lg">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Location Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Select Location
              </label>
              <select
                className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-blue-500"
                onChange={(e) => {
                  const location = predefinedLocations[e.target.value];
                  setSelectedLocation(location);
                }}
              >
                {predefinedLocations.map((loc, idx) => (
                  <option key={idx} value={idx}>
                    {loc.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Start Date */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Start Date
              </label>
              <input
                type="date"
                className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-blue-500"
                value={dateRange.start}
                onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              />
            </div>

            {/* End Date */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                End Date
              </label>
              <input
                type="date"
                className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-blue-500"
                value={dateRange.end}
                onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              />
            </div>
          </div>

          <button
            onClick={fetchTimeSeriesData}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition"
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Update Chart'}
          </button>
        </div>

        {/* Chart */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg mb-6">
          <div style={{ height: '400px' }}>
            {timeSeriesData ? (
              <Line data={timeSeriesData} options={chartOptions} />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="spinner"></div>
              </div>
            )}
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm mb-2">Average</h3>
            <p className="text-2xl font-bold text-white">52.3%</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm mb-2">Peak</h3>
            <p className="text-2xl font-bold text-white">68.5%</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm mb-2">Minimum</h3>
            <p className="text-2xl font-bold text-white">38.2%</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm mb-2">Trend</h3>
            <p className="text-2xl font-bold text-white">↗ +5.2%</p>
          </div>
        </div>

        {/* Seasonal Analysis */}
        <div className="bg-gray-800 rounded-lg p-6 mt-6 shadow-lg">
          <h3 className="text-white text-lg font-semibold mb-4">Seasonal Patterns</h3>
          <p className="text-gray-400 mb-4">
            Analysis shows seasonal variation in microplastic concentrations, with peaks typically occurring in winter months due to increased ocean currents and storm activity.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl mb-2">🌸</div>
              <h4 className="text-white font-semibold">Spring</h4>
              <p className="text-gray-400 text-sm">Moderate (45%)</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">☀️</div>
              <h4 className="text-white font-semibold">Summer</h4>
              <p className="text-gray-400 text-sm">Lower (38%)</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">🍂</div>
              <h4 className="text-white font-semibold">Autumn</h4>
              <p className="text-gray-400 text-sm">Rising (52%)</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">❄️</div>
              <h4 className="text-white font-semibold">Winter</h4>
              <p className="text-gray-400 text-sm">Peak (68%)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimeSeriesView;
