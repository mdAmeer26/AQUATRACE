import React from 'react';

const AlertsPanel = ({ alerts }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-600';
      case 'high':
        return 'bg-orange-500';
      case 'medium':
        return 'bg-yellow-500';
      default:
        return 'bg-blue-500';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return '🚨';
      case 'high':
        return '⚠️';
      case 'medium':
        return '⚡';
      default:
        return 'ℹ️';
    }
  };

  return (
    <div className="alerts-panel bg-gradient-to-br from-gray-800 via-gray-900 to-blue-900 w-80 overflow-y-auto border-l-4 border-cyan-500 shadow-2xl h-full">
      <div className="p-4 border-b-2 border-cyan-500 bg-gradient-to-r from-cyan-600 to-blue-600">
        <h2 className="text-xl font-bold text-white flex items-center drop-shadow-lg">
          <span className="mr-2">🔔</span>
          Active Alerts
        </h2>
        <p className="text-sm text-cyan-100 mt-1">
          {alerts.length} active alert{alerts.length !== 1 ? 's' : ''}
        </p>
      </div>

      <div className="p-4 space-y-3">
        {alerts.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-5xl mb-3">✅</div>
            <p className="text-cyan-300 font-semibold">No active alerts</p>
            <p className="text-sm text-gray-400 mt-2">
              All monitored areas are within normal ranges
            </p>
          </div>
        ) : (
          alerts.map((alert, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-4 border-2 border-gray-700 hover:border-cyan-500 transition-all shadow-lg hover:shadow-cyan-500/20"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-3xl drop-shadow-lg">
                    {getSeverityIcon(alert.severity)}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold text-white ${getSeverityColor(alert.severity)} shadow-md`}>
                    {alert.severity?.toUpperCase()}
                  </span>
                </div>
              </div>

              <h3 className="text-white font-bold mb-2 text-base">
                {alert.title || 'High Concentration Detected'}
              </h3>

              <p className="text-sm text-gray-300 mb-4 leading-relaxed">
                {alert.description || 'Elevated microplastic levels detected in this region'}
              </p>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between bg-gray-800/50 rounded-lg px-3 py-2">
                  <span className="text-gray-400">Location:</span>
                  <span className="text-cyan-300 font-semibold">
                    {alert.lat?.toFixed(2)}°, {alert.lon?.toFixed(2)}°
                  </span>
                </div>
                <div className="flex justify-between bg-gray-800/50 rounded-lg px-3 py-2">
                  <span className="text-gray-400">Concentration:</span>
                  <span className="text-red-400 font-bold">
                    {((alert.concentration || 0) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between bg-gray-800/50 rounded-lg px-3 py-2">
                  <span className="text-gray-400">Detected:</span>
                  <span className="text-gray-300 font-semibold">
                    {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'Recently'}
                  </span>
                </div>
              </div>

              <button className="mt-4 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white text-sm font-semibold py-2.5 rounded-lg transition-all shadow-md hover:shadow-lg">
                View on Map →
              </button>
            </div>
          ))
        )}
      </div>

      {/* Info Section */}
      <div className="p-4 bg-gradient-to-r from-gray-900 to-blue-900 border-t-2 border-cyan-500">
        <h3 className="text-sm font-bold text-cyan-300 mb-2 flex items-center gap-2">
          ℹ️ About Alerts
        </h3>
        <p className="text-xs text-gray-300 leading-relaxed">
          Alerts are triggered when microplastic concentrations exceed predefined thresholds based on ML model predictions.
        </p>
      </div>
    </div>
  );
};

export default AlertsPanel;
