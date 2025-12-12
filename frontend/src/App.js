import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';
import TimeSeriesView from './components/TimeSeriesView';
import SearchPanel from './components/SearchPanel';
import LocationPermission from './components/LocationPermission';
import About from './components/About';
import './App.css';

function App() {
  const [currentData, setCurrentData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mapInstance, setMapInstance] = useState(null);
  const [locationGranted, setLocationGranted] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleLocationGranted = () => {
    setLocationGranted(true);
  };

  const handleLocationSelect = (lat, lon) => {
    if (mapInstance) {
      mapInstance.setView([lat, lon], 10, {
        animate: true,
        duration: 1
      });
    }
  };

  const fetchData = useCallback(async () => {
    try {
      // Fetch current microplastic data
      const dataResponse = await fetch(`${API_URL}/api/v1/microplastic/current`);
      const data = await dataResponse.json();
      setCurrentData(data);

      // Fetch alerts
      const alertsResponse = await fetch(`${API_URL}/api/v1/alerts`);
      const alertsData = await alertsResponse.json();
      setAlerts(alertsData.alerts || []);

      // Fetch statistics
      const statsResponse = await fetch(`${API_URL}/api/v1/statistics`);
      const statsData = await statsResponse.json();
      setStatistics(statsData);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  }, [API_URL]);

  useEffect(() => {
    // Fetch initial data
    fetchData();

    // Set up periodic updates
    const interval = setInterval(fetchData, 
      parseInt(process.env.REACT_APP_UPDATE_INTERVAL) || 300000
    );

    return () => clearInterval(interval);
  }, [fetchData]);

  return (
    <Router>
      <div className="App">
        {!locationGranted && <LocationPermission onLocationGranted={handleLocationGranted} />}
        
        <Navbar onSearchClick={() => setSearchOpen(!searchOpen)} />
        
        <Routes>
          <Route 
            path="/" 
            element={
              <div className="main-view">
                <MapView 
                  data={currentData} 
                  loading={loading}
                  onMapReady={setMapInstance}
                />
                {searchOpen && <SearchPanel onLocationSelect={handleLocationSelect} onClose={() => setSearchOpen(false)} />}
              </div>
            } 
          />
          
          <Route 
            path="/dashboard" 
            element={
              <Dashboard 
                statistics={statistics} 
                alerts={alerts}
                loading={loading}
              />
            } 
          />
          
          <Route 
            path="/timeseries" 
            element={<TimeSeriesView />} 
          />
          
          <Route 
            path="/about" 
            element={<About />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
