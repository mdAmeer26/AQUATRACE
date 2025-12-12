import React, { useState, useEffect } from 'react';
import { MapPin, Navigation } from 'lucide-react';

const LocationPermission = ({ onLocationGranted }) => {
  const [showModal, setShowModal] = useState(true);
  const [requesting, setRequesting] = useState(false);

  const requestLocation = () => {
    setRequesting(true);
    
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setShowModal(false);
          onLocationGranted({ lat: latitude, lon: longitude });
        },
        (error) => {
          console.warn('Location access denied:', error);
          // Use default India location
          setShowModal(false);
          onLocationGranted({ lat: 17.385, lon: 78.4867 }); // Hyderabad default
        }
      );
    } else {
      setShowModal(false);
      onLocationGranted({ lat: 17.385, lon: 78.4867 });
    }
  };

  const skipLocation = () => {
    setShowModal(false);
    onLocationGranted({ lat: 17.385, lon: 78.4867 }); // Default to Hyderabad
  };

  if (!showModal) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden animate-fade-in">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 p-6">
          <div className="flex items-center justify-center mb-4">
            <div className="bg-white/20 p-4 rounded-full backdrop-blur-sm">
              <Navigation className="w-12 h-12 text-white" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white text-center">
            Welcome to AquaTrace
          </h2>
          <p className="text-blue-100 text-center mt-2">
            Water Source Monitoring System
          </p>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="mb-6">
            <div className="flex items-start gap-3 mb-4">
              <MapPin className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">Location Access</h3>
                <p className="text-sm text-gray-600 leading-relaxed">
                  AquaTrace needs your location to show nearby water sources and provide accurate contamination data for your area.
                </p>
              </div>
            </div>

            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
              <p className="text-sm text-blue-900 font-medium">
                📍 We'll display all water sources (rivers, lakes, dams, ponds) near you
              </p>
              <p className="text-sm text-blue-900 font-medium mt-2">
                💧 View real-time contamination levels
              </p>
              <p className="text-sm text-blue-900 font-medium mt-2">
                🔍 Search and explore water sources across regions
              </p>
            </div>
          </div>

          {/* Buttons */}
          <div className="space-y-3">
            <button
              onClick={requestLocation}
              disabled={requesting}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {requesting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                  Requesting...
                </>
              ) : (
                <>
                  <Navigation className="w-5 h-5" />
                  Allow Location Access
                </>
              )}
            </button>

            <button
              onClick={skipLocation}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-6 rounded-xl transition-all"
            >
              Skip (Use Default Location)
            </button>
          </div>

          <p className="text-xs text-gray-500 text-center mt-4">
            Your location data is only used to display nearby water sources and is never stored or shared.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LocationPermission;
