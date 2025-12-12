import React, { useState } from 'react';
import { Search, Droplet, X, MapPin, TrendingUp, AlertTriangle, ChevronRight } from 'lucide-react';

const SearchPanel = ({ onLocationSelect, onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/search/location?query=${encodeURIComponent(searchQuery)}`
      );
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const getContaminationColor = (level) => {
    const colors = {
      critical: 'bg-red-600 text-white',
      high: 'bg-orange-600 text-white',
      medium: 'bg-yellow-600 text-white',
      low: 'bg-green-600 text-white'
    };
    return colors[level] || 'bg-gray-600 text-white';
  };

  // Full-screen search modal
  return (
    <div className="fixed inset-0 z-[800] bg-black/40 backdrop-blur-md flex items-start justify-center pt-16 px-4 overflow-y-auto">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-5xl mb-10 animate-fade-in">
        {/* Header */}
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-8 rounded-t-3xl flex justify-between items-center border-b border-gray-200">
          <div className="flex items-center gap-4">
            <div className="bg-blue-600 p-3 rounded-xl">
              <Search className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-gray-800 font-bold text-2xl">Search Water Sources</h2>
              <p className="text-gray-600 text-sm mt-1">Find water bodies across India</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:bg-gray-200 p-2.5 rounded-xl transition-all"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Search Bar */}
        <div className="p-8 border-b border-gray-100">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter location name..."
                className="w-full pl-12 pr-6 py-4 text-base border border-gray-200 rounded-2xl focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-100 text-gray-800 transition-all"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={loading}
              className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-semibold text-base transition-all disabled:opacity-50 shadow-sm hover:shadow-md min-w-[120px]"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Searching
                </span>
              ) : (
                'Search'
              )}
            </button>
          </div>
          <p className="mt-4 text-gray-500 text-sm flex items-center gap-2">
            <Droplet className="w-4 h-4 text-blue-500" />
            Try: Telangana, Hyderabad, Maharashtra, Mumbai, Bangalore
          </p>
        </div>

        {/* Results */}
        {searchResults && (
          <div className="p-8">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200 shadow-sm">
                <div className="flex items-center gap-3 mb-2">
                  <div className="bg-blue-600 p-2 rounded-lg">
                    <Droplet className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-gray-600 font-medium text-sm">Total Sources</span>
                </div>
                <div className="text-4xl font-bold text-blue-700">{searchResults.total_sources_found}</div>
              </div>
              <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-2xl p-6 border border-emerald-200 shadow-sm">
                <div className="flex items-center gap-3 mb-2">
                  <div className="bg-emerald-600 p-2 rounded-lg">
                    <span className="text-white font-bold text-sm">QI</span>
                  </div>
                  <span className="text-gray-600 font-medium text-sm">Avg Quality</span>
                </div>
                <div className="text-4xl font-bold text-emerald-700">{searchResults.overall_water_quality_index}/100</div>
              </div>
              <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-2xl p-6 border border-amber-200 shadow-sm">
                <div className="flex items-center gap-3 mb-2">
                  <div className="bg-amber-600 p-2 rounded-lg">
                    <span className="text-white font-bold text-lg">⚠️</span>
                  </div>
                  <span className="text-gray-600 font-medium text-sm">Need Attention</span>
                </div>
                <div className="text-4xl font-bold text-amber-700">
                  {searchResults.contamination_summary.critical + searchResults.contamination_summary.high}
                </div>
              </div>
            </div>

            {/* Water Sources Grid */}
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                <MapPin className="w-6 h-6 text-blue-600" />
                Water Sources
              </h3>
              <span className="text-sm text-gray-500">{searchResults.water_sources.length} results</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              {searchResults.water_sources.map((source) => (
                <div
                  key={source.id}
                  className="bg-white rounded-2xl p-6 border border-gray-200 hover:border-blue-400 cursor-pointer transition-all hover:shadow-lg group"
                  onClick={() => {
                    onLocationSelect && onLocationSelect(source.lat, source.lon);
                    onClose();
                  }}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h4 className="text-lg font-bold text-gray-800 group-hover:text-blue-600 transition-colors">{source.name}</h4>
                      <div className="flex items-center gap-2 mt-2">
                        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-lg text-xs font-semibold">
                          {source.type}
                        </span>
                        <span className="text-gray-600 text-xs flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {source.location}
                        </span>
                      </div>
                    </div>
                    <span className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase ${getContaminationColor(source.contamination_level)}`}>
                      {source.contamination_level}
                    </span>
                  </div>

                  {/* Quality Bar */}
                  <div className="mb-4">
                    <div className="flex justify-between text-xs mb-2">
                      <span className="font-medium text-gray-600">Water Quality Index</span>
                      <span className="font-bold text-gray-800">{source.water_quality_index}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                      <div
                        className={`h-2.5 rounded-full transition-all ${
                          source.water_quality_index >= 70 ? 'bg-gradient-to-r from-green-500 to-emerald-600' :
                          source.water_quality_index >= 50 ? 'bg-gradient-to-r from-yellow-500 to-amber-600' :
                          source.water_quality_index >= 30 ? 'bg-gradient-to-r from-orange-500 to-red-500' :
                          'bg-gradient-to-r from-red-600 to-red-700'
                        }`}
                        style={{ width: `${source.water_quality_index}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Contaminants */}
                  <div className="flex flex-wrap gap-2 mb-3">
                    {source.detected_contaminants.slice(0, 3).map((cont, idx) => (
                      <span
                        key={idx}
                        className="bg-red-50 text-red-700 px-2.5 py-1 rounded-lg text-xs font-semibold border border-red-200"
                      >
                        {cont.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>

                  <button className="mt-2 w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-2.5 rounded-xl font-semibold text-sm transition-all shadow-sm hover:shadow-md">
                    View on Map →
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {!searchResults && !loading && (
          <div className="p-16 text-center text-gray-500">
            <div className="bg-gray-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
              <Search className="w-12 h-12 text-gray-400" />
            </div>
            <p className="text-xl font-semibold text-gray-700">Search for water sources</p>
            <p className="mt-2 text-gray-500">Enter a location to discover rivers, lakes, dams, and ponds</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPanel;
