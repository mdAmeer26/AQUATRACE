import React from 'react';

const About = () => {
  return (
    <div className="about-container p-6 bg-gray-900 min-h-screen overflow-y-auto">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">About AquaTrace</h1>
          <p className="text-xl text-gray-400">
            Real-time Ocean Microplastic Mapping and Alert System
          </p>
        </div>

        {/* Mission Statement */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-4">Our Mission</h2>
          <p className="text-white text-lg">
            AquaTrace bridges cutting-edge satellite technology with artificial intelligence to provide
            unprecedented visibility into ocean microplastic pollution. By making this data accessible
            and actionable, we empower scientists, policymakers, and environmental organizations to
            protect our oceans.
          </p>
        </div>

        {/* How It Works */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-6">How It Works</h2>
          
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">1</span>
              </div>
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">Satellite Data Collection</h3>
                <p className="text-gray-400">
                  We continuously fetch data from NASA CYGNSS satellites, which measure ocean surface
                  roughness using reflected GPS signals. ESA Sentinel-2 provides high-resolution optical
                  imagery for coastal regions.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">2</span>
              </div>
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">AI-Powered Analysis</h3>
                <p className="text-gray-400">
                  Our machine learning models (CNN-LSTM architecture) analyze satellite observations to
                  detect anomalies in ocean surface characteristics that indicate microplastic presence.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">3</span>
              </div>
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">Real-Time Visualization</h3>
                <p className="text-gray-400">
                  Processed data is transformed into interactive heatmaps, showing microplastic
                  concentration levels across the global ocean in near-real-time.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">4</span>
              </div>
              <div>
                <h3 className="text-white font-semibold text-lg mb-2">Alert Generation</h3>
                <p className="text-gray-400">
                  When concentrations exceed critical thresholds, automated alerts notify relevant
                  stakeholders to enable rapid response and targeted cleanup efforts.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Scientific Foundation */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-6">Scientific Foundation</h2>
          
          <div className="space-y-4 text-gray-400">
            <p>
              <strong className="text-white">NASA CYGNSS:</strong> The Cyclone Global Navigation Satellite
              System uses reflected GPS signals to measure ocean surface properties. Recent research has
              demonstrated that changes in surface roughness can indicate microplastic concentrations.
            </p>
            
            <p>
              <strong className="text-white">ESA Sentinel-2:</strong> High-resolution optical imagery
              enables detection of larger plastic aggregations and coastal pollution patterns.
            </p>
            
            <p>
              <strong className="text-white">Machine Learning:</strong> Our deep learning models are trained
              on correlated satellite-ground truth datasets to accurately predict microplastic densities
              from remotely sensed observations.
            </p>
            
            <p>
              <strong className="text-white">Validation:</strong> Model predictions are continuously validated
              against in-situ measurements from research vessels and autonomous platforms.
            </p>
          </div>
        </div>

        {/* Key Features */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-6">Key Features</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🌍</span>
              <div>
                <h3 className="text-white font-semibold">Global Coverage</h3>
                <p className="text-gray-400 text-sm">Monitor all major ocean regions</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <span className="text-2xl">⚡</span>
              <div>
                <h3 className="text-white font-semibold">Real-Time Updates</h3>
                <p className="text-gray-400 text-sm">Data refreshed continuously</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🤖</span>
              <div>
                <h3 className="text-white font-semibold">AI-Powered Detection</h3>
                <p className="text-gray-400 text-sm">Advanced ML models</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <span className="text-2xl">📊</span>
              <div>
                <h3 className="text-white font-semibold">Temporal Analysis</h3>
                <p className="text-gray-400 text-sm">Track trends over time</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🔔</span>
              <div>
                <h3 className="text-white font-semibold">Smart Alerts</h3>
                <p className="text-gray-400 text-sm">Threshold-based notifications</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <span className="text-2xl">🔓</span>
              <div>
                <h3 className="text-white font-semibold">Open API</h3>
                <p className="text-gray-400 text-sm">Access for researchers</p>
              </div>
            </div>
          </div>
        </div>

        {/* Impact */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-6">Real-World Impact</h2>
          
          <div className="space-y-4 text-gray-400">
            <p>
              <strong className="text-white">For Policymakers:</strong> Identify pollution hotspots to
              target legislation and allocate cleanup resources effectively.
            </p>
            
            <p>
              <strong className="text-white">For NGOs:</strong> Plan cleanup operations with data-driven
              insights, maximizing impact per dollar spent.
            </p>
            
            <p>
              <strong className="text-white">For Scientists:</strong> Access comprehensive time-series
              data to study pollution dynamics, seasonal patterns, and the effectiveness of interventions.
            </p>
            
            <p>
              <strong className="text-white">For the Public:</strong> Raise awareness about ocean pollution
              and track progress toward cleaner oceans.
            </p>
          </div>
        </div>

        {/* Data Sources */}
        <div className="bg-gray-800 rounded-lg p-8 mb-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-6">Data Sources</h2>
          
          <div className="space-y-4">
            <div className="border-l-4 border-blue-500 pl-4">
              <h3 className="text-white font-semibold">NASA Physical Oceanography DAAC</h3>
              <p className="text-gray-400 text-sm">CYGNSS Level 2 Ocean Surface Data</p>
            </div>
            
            <div className="border-l-4 border-green-500 pl-4">
              <h3 className="text-white font-semibold">ESA Copernicus Hub</h3>
              <p className="text-gray-400 text-sm">Sentinel-2 and Sentinel-3 Imagery</p>
            </div>
            
            <div className="border-l-4 border-purple-500 pl-4">
              <h3 className="text-white font-semibold">NOAA</h3>
              <p className="text-gray-400 text-sm">Oceanographic Reference Data</p>
            </div>
          </div>
        </div>

        {/* Team & Contact */}
        <div className="bg-gray-800 rounded-lg p-8 shadow-lg">
          <h2 className="text-2xl font-bold text-white mb-4">Get Involved</h2>
          <p className="text-gray-400 mb-6">
            AquaTrace is an open platform committed to ocean conservation. We welcome collaborations
            with researchers, environmental organizations, and technology partners.
          </p>
          
          <div className="flex flex-wrap gap-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition">
              API Documentation
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition">
              GitHub Repository
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition">
              Contact Us
            </button>
          </div>
        </div>

        {/* Footer Note */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>
            AquaTrace is a research and awareness platform. Concentration estimates are based on
            satellite-derived proxies and ML models, subject to ongoing validation.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;
