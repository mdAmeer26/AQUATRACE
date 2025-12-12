import React, { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import WaterBodyModal from './WaterBodyModal';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapView = ({ data, loading, onMapReady }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const heatLayerRef = useRef(null);
  const [selectedWaterBody, setSelectedWaterBody] = useState(null);
  const [userLocation, setUserLocation] = useState(null);
  const markersRef = useRef([]);

  // Request location permission on component mount
  useEffect(() => {
    const requestLocation = () => {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            setUserLocation({ lat: latitude, lon: longitude });
            console.log('User location:', latitude, longitude);
          },
          (error) => {
            console.warn('Location access denied:', error);
            // Default to India if location denied
            setUserLocation({ lat: 20.5937, lon: 78.9629 });
          }
        );
      } else {
        // Default to India if geolocation not supported
        setUserLocation({ lat: 20.5937, lon: 78.9629 });
      }
    };

    requestLocation();
  }, []);

  // Expose map instance to parent
  useEffect(() => {
    if (mapInstanceRef.current && onMapReady) {
      onMapReady(mapInstanceRef.current);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onMapReady]);

  useEffect(() => {
    // Initialize map with user location
    if (!mapInstanceRef.current && mapRef.current && userLocation) {
      mapInstanceRef.current = L.map(mapRef.current, {
        center: [userLocation.lat, userLocation.lon],
        zoom: 6,
        minZoom: 1,
        maxZoom: 18,
        worldCopyJump: false,
        noWrap: false
      });

      // ESRI World Imagery - Globe view at all zoom levels
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
        minZoom: 1
      }).addTo(mapInstanceRef.current);

      // Add user location marker
      L.marker([userLocation.lat, userLocation.lon], {
        icon: L.divIcon({
          html: '<div style="font-size: 32px;">📍</div>',
          className: 'custom-marker',
          iconSize: [32, 32]
        })
      }).addTo(mapInstanceRef.current)
        .bindPopup('Your Location')
        .openPopup();

      // Fetch all water sources from database
      fetchAllWaterSources();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userLocation]);

  const fetchAllWaterSources = useCallback(async () => {
    try {
      console.log('Fetching all water sources globally...');
      
      // Fetch all water sources from the global endpoint
      const response = await fetch('http://localhost:8000/api/v1/search/all-water-sources');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.water_sources && data.water_sources.length > 0) {
        console.log(`Found ${data.water_sources.length} water sources globally`);
        displayAllWaterSources(data.water_sources);
        console.log(`Displayed ${data.water_sources.length} markers on map`);
      } else {
        console.warn('No water sources found in database');
      }
    } catch (error) {
      console.error('Error fetching water sources:', error);
      
      // Fallback: If global endpoint fails, try regional search
      console.log('Falling back to regional search...');
      await fetchRegionalWaterSources();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchRegionalWaterSources = async () => {
    try {
      const regions = ['telangana', 'hyderabad', 'maharashtra', 'karnataka', 'andhra pradesh', 'tamil nadu', 'kerala', 'goa', 'mumbai', 'bangalore', 'chennai', 'kochi'];
      const allSources = [];

      for (const region of regions) {
        try {
          const response = await fetch(
            `http://localhost:8000/api/v1/search/location?query=${region}`
          );
          const data = await response.json();
          if (data.water_sources && data.water_sources.length > 0) {
            allSources.push(...data.water_sources);
            console.log(`Found ${data.water_sources.length} water sources in ${region}`);
          }
        } catch (err) {
          console.log(`Could not fetch data for ${region}`);
        }
      }

      if (allSources.length > 0) {
        displayAllWaterSources(allSources);
        console.log(`Displayed ${allSources.length} markers on map (regional)`);
      }
    } catch (error) {
      console.error('Regional fetch also failed:', error);
    }
  };

  const displayAllWaterSources = (sources) => {
    if (!mapInstanceRef.current || !sources || sources.length === 0) {
      console.log('Cannot display markers: map not ready or no sources');
      return;
    }

    console.log(`Displaying ${sources.length} water sources on map`);

    // Clear existing markers
    markersRef.current.forEach(marker => {
      try {
        marker.remove();
      } catch (e) {
        console.log('Error removing marker:', e);
      }
    });
    markersRef.current = [];

    // Icon based on water body type and contamination
    const getIcon = (type, contamination) => {
      const colors = {
        critical: '#dc2626',
        high: '#f97316',
        medium: '#eab308',
        low: '#16a34a'
      };

      const color = colors[contamination] || '#3b82f6';

      return L.divIcon({
        html: `<div style="width: 16px; height: 16px; background: ${color}; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); cursor: pointer;"></div>`,
        className: 'custom-water-marker',
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      });
    };

    // Add markers for all water sources
    sources.forEach(source => {
      const marker = L.marker([source.lat, source.lon], {
        icon: getIcon(source.type, source.contamination_level)
      }).addTo(mapInstanceRef.current);

      const popupContent = `
        <div style="min-width: 280px; font-family: 'Inter', sans-serif;">
          <h3 style="margin: 0 0 14px 0; font-size: 20px; font-weight: 700; color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 10px;">
            ${source.name}
          </h3>
          <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 14px; border-radius: 12px; margin-bottom: 12px;">
            <p style="margin: 8px 0; font-size: 15px; color: #1e293b; display: flex; justify-content: space-between;">
              <strong style="color: #475569;">Type:</strong> 
              <span style="background: #3b82f6; color: white; padding: 3px 12px; border-radius: 8px; font-weight: 600; font-size: 13px;">${source.type.toUpperCase()}</span>
            </p>
            <p style="margin: 8px 0; font-size: 15px; color: #1e293b;">
              <strong style="color: #475569;">📍 Location:</strong> ${source.location}
            </p>
          </div>
          <div style="background: ${
            source.contamination_level === 'critical' ? 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)' :
            source.contamination_level === 'high' ? 'linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%)' :
            source.contamination_level === 'medium' ? 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)' :
            'linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)'
          }; padding: 12px; border-radius: 12px; margin-bottom: 12px;">
            <p style="margin: 8px 0; font-size: 15px; display: flex; justify-content: space-between; align-items: center;">
              <strong style="color: #334155;">⚠️ Contamination:</strong> 
              <span style="background: ${
                source.contamination_level === 'critical' ? '#dc2626' :
                source.contamination_level === 'high' ? '#ea580c' :
                source.contamination_level === 'medium' ? '#ca8a04' :
                '#16a34a'
              }; color: white; padding: 5px 14px; border-radius: 10px; font-weight: 700; text-transform: uppercase; font-size: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                ${source.contamination_level}
              </span>
            </p>
          </div>
          <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); padding: 12px; border-radius: 12px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <strong style="color: #475569; font-size: 14px;">💧 Water Quality:</strong>
              <span style="font-weight: 700; font-size: 18px; color: ${
                source.water_quality_index >= 70 ? '#16a34a' :
                source.water_quality_index >= 50 ? '#ca8a04' :
                '#dc2626'
              };">${source.water_quality_index}/100</span>
            </div>
            <div style="width: 100%; background: #cbd5e1; border-radius: 10px; height: 10px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
              <div style="height: 10px; border-radius: 10px; background: ${
                source.water_quality_index >= 70 ? 'linear-gradient(90deg, #16a34a 0%, #22c55e 100%)' :
                source.water_quality_index >= 50 ? 'linear-gradient(90deg, #ca8a04 0%, #eab308 100%)' :
                'linear-gradient(90deg, #dc2626 0%, #ef4444 100%)'
              }; width: ${source.water_quality_index}%; transition: width 0.3s ease;"></div>
            </div>
          </div>
          <div style="margin: 12px 0;">
            <p style="margin: 4px 0 8px 0; font-size: 13px; color: #64748b; font-weight: 600;">🔬 Detected Contaminants:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
              ${source.detected_contaminants.slice(0, 3).map(cont => 
                `<span style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 700; border: 1px solid #fca5a5; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                  ${cont.replace(/_/g, ' ').toUpperCase()}
                </span>`
              ).join('')}
            </div>
          </div>
          <button 
            id="view-details-btn-${source.id || source.name.replace(/\s/g, '-')}"
            data-water-body-id="${source.id || source.name}"
            style="width: 100%; margin-top: 14px; padding: 16px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; border-radius: 16px; font-weight: 700; cursor: pointer; font-size: 17px; transition: all 0.2s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);" 
            onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(37, 99, 235, 0.5)'" 
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(37, 99, 235, 0.4)'"
          >
            📊 View Real-Time Analysis
          </button>
        </div>
      `;

      marker.bindPopup(popupContent);

      // Add click handler after popup opens
      marker.on('popupopen', () => {
        const button = document.getElementById(`view-details-btn-${source.id || source.name.replace(/\s/g, '-')}`);
        if (button) {
          button.onclick = (e) => {
            e.preventDefault();
            const waterBodyId = button.getAttribute('data-water-body-id');
            console.log('Button clicked for:', waterBodyId);
            if (window.showWaterBodyDetails) {
              window.showWaterBodyDetails(waterBodyId);
            }
          };
        }
      });

      markersRef.current.push(marker);
    });
  };

  // Expose function to window for popup button
  useEffect(() => {
    window.showWaterBodyDetails = (waterBodyId) => {
      console.log('Opening modal for:', waterBodyId);
      setSelectedWaterBody(waterBodyId);
    };
    console.log('Window function registered');
    return () => {
      delete window.showWaterBodyDetails;
    };
  }, []);

  // eslint-disable-next-line no-unused-vars
  const updateHeatmap = (heatmapData) => {
    // Remove existing heat layer
    if (heatLayerRef.current) {
      mapInstanceRef.current.removeLayer(heatLayerRef.current);
    }

    // Create layer group for heat zones
    const heatLayer = L.layerGroup();

    // Color mapping for concentration levels
    const colorMap = {
      'very_low': '#90EE90',
      'low': '#FFFF00',
      'medium': '#FFA500',
      'high': '#FF4500',
      'critical': '#8B0000'
    };

    // Add circles for each zone
    if (heatmapData.features && heatmapData.features.length > 0) {
      heatmapData.features.forEach(feature => {
        const { lat, lon, concentration, level } = feature.properties || feature;
        
        if (lat && lon) {
          const circle = L.circle([lat, lon], {
            color: colorMap[level] || '#FFA500',
            fillColor: colorMap[level] || '#FFA500',
            fillOpacity: 0.5,
            radius: 50000, // 50km radius
            weight: 1
          });

          // Add popup
          circle.bindPopup(`
            <div class="popup-content">
              <h3 style="color: #0a1929; font-weight: bold; margin-bottom: 8px;">
                Microplastic Concentration
              </h3>
              <p style="color: #0a1929; margin: 4px 0;">
                <strong>Level:</strong> ${level.replace('_', ' ').toUpperCase()}
              </p>
              <p style="color: #0a1929; margin: 4px 0;">
                <strong>Concentration:</strong> ${(concentration * 100).toFixed(1)}%
              </p>
              <p style="color: #0a1929; margin: 4px 0;">
                <strong>Location:</strong> ${lat.toFixed(2)}°, ${lon.toFixed(2)}°
              </p>
            </div>
          `);

          circle.addTo(heatLayer);
        }
      });
    }

    heatLayer.addTo(mapInstanceRef.current);
    heatLayerRef.current = heatLayer;
  };

  // eslint-disable-next-line no-unused-vars
  const handleZoomToRegion = (region) => {
    if (mapInstanceRef.current && region) {
      const [minLon, minLat, maxLon, maxLat] = region.bbox;
      mapInstanceRef.current.fitBounds([
        [minLat, minLon],
        [maxLat, maxLon]
      ]);
    }
  };

  return (
    <div className="map-container">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}
      
      <div ref={mapRef} className="leaflet-container" />

      {/* Water Body Details Modal */}
      {selectedWaterBody && (
        <WaterBodyModal
          waterBodyId={selectedWaterBody}
          onClose={() => setSelectedWaterBody(null)}
        />
      )}
    </div>
  );
};

export default MapView;
