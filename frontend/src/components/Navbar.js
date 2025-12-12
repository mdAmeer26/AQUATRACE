import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ onSearchClick }) => {
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-700 shadow-lg">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="relative">
              <svg 
                className="w-8 h-8 text-white" 
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
              </svg>
            </div>
            <span className="text-xl font-bold text-white">
              AquaTrace
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-1">
            <Link 
              to="/" 
              className="px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
            >
              Map
            </Link>
            <Link 
              to="/dashboard" 
              className="px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
            >
              Dashboard
            </Link>
            <Link 
              to="/timeseries" 
              className="px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
            >
              Analysis
            </Link>
            <Link 
              to="/about" 
              className="px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
            >
              About
            </Link>
          </div>

          {/* Right Section: Search + Status */}
          <div className="flex items-center space-x-4">
            {/* Search Button */}
            <button
              onClick={onSearchClick}
              className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition text-white text-sm font-medium"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Search</span>
            </button>
            
            {/* Status Indicator */}
            <div className="flex items-center space-x-2 bg-green-500 px-3 py-1.5 rounded-full">
              <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
              <span className="text-xs text-white font-semibold">Live</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
