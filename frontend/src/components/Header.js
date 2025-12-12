import React from 'react';
import { Droplets, Satellite } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg">
              <Droplets className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 tracking-tight">
                AquaTrace
              </h1>
              <p className="text-xs text-gray-500 -mt-0.5">
                Water Quality Monitor
              </p>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="hidden md:flex items-center space-x-6">
            <a 
              href="#map" 
              className="flex items-center space-x-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
            >
              <Satellite className="w-4 h-4" />
              <span>Live Map</span>
            </a>
            <a 
              href="#analytics" 
              className="flex items-center space-x-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
            >
              <span>Analytics</span>
            </a>
            <a 
              href="#about" 
              className="flex items-center space-x-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
            >
              <span>About</span>
            </a>
          </nav>

          {/* Status Indicator */}
          <div className="flex items-center space-x-2 px-4 py-2 bg-green-50 rounded-full border border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-green-700">Live</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
