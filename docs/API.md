# AquaTrace API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API is open for public access. Future versions will implement API key authentication.

## Endpoints

### Get Current Microplastic Data

Retrieve current global microplastic concentration data.

**Endpoint:** `GET /microplastic/current`

**Query Parameters:**
- `bbox` (optional): Bounding box as comma-separated values (min_lon,min_lat,max_lon,max_lat)
- `resolution` (optional): Data resolution - `low`, `medium` (default), or `high`

**Response:**
```json
{
  "type": "FeatureCollection",
  "timestamp": "2025-12-07T00:00:00Z",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-140.0, 35.0]
      },
      "properties": {
        "concentration": 0.85,
        "level": "high",
        "lat": 35.0,
        "lon": -140.0
      }
    }
  ],
  "metadata": {
    "resolution": "medium",
    "data_sources": ["CYGNSS", "Sentinel-2"],
    "model_version": "v1.0"
  }
}
```

### Get Time Series Data

Get historical microplastic concentration data for a specific location.

**Endpoint:** `GET /microplastic/timeseries`

**Query Parameters:**
- `lat` (required): Latitude
- `lon` (required): Longitude
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)

**Response:**
```json
{
  "location": {
    "lat": 35.0,
    "lon": -140.0
  },
  "start_date": "2025-01-01",
  "end_date": "2025-12-07",
  "data": [
    {
      "date": "2025-01-01",
      "concentration": 0.75,
      "confidence": 0.92
    }
  ]
}
```

### Get Active Alerts

Retrieve active microplastic concentration alerts.

**Endpoint:** `GET /alerts`

**Query Parameters:**
- `severity` (optional): Filter by severity (`medium`, `high`, `critical`)

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert_20251207120000_35.0_-140.0",
      "severity": "critical",
      "title": "Critical Microplastic Concentration Detected",
      "description": "Concentration of 95.0% detected at 35.00°, -140.00°",
      "lat": 35.0,
      "lon": -140.0,
      "concentration": 0.95,
      "timestamp": "2025-12-07T12:00:00",
      "region": "North Pacific Gyre",
      "acknowledged": false
    }
  ],
  "total": 1,
  "timestamp": "2025-12-07T12:00:00Z"
}
```

### Get Global Statistics

Get global microplastic statistics and trends.

**Endpoint:** `GET /statistics`

**Response:**
```json
{
  "global_average": 0.52,
  "total_area_monitored_km2": 285000000,
  "high_concentration_zones": 12,
  "trend": "increasing",
  "last_updated": "2025-12-07T00:00:00Z"
}
```

### Get Predefined Regions

Get list of predefined ocean regions.

**Endpoint:** `GET /regions`

**Response:**
```json
{
  "regions": [
    {
      "id": "north_pacific_gyre",
      "name": "North Pacific Gyre",
      "bbox": [-180, 20, -120, 50],
      "description": "Great Pacific Garbage Patch region"
    }
  ]
}
```

## Rate Limiting

Currently no rate limiting. Future versions will implement:
- 100 requests per minute for unauthenticated users
- 1000 requests per minute for authenticated users

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "error": "Invalid parameters",
  "detail": "bbox must contain 4 comma-separated values"
}
```

**404 Not Found**
```json
{
  "error": "Resource not found",
  "detail": "No data available for specified date range"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred"
}
```

## Data Update Frequency

- Current microplastic data: Updated every 6 hours
- Time series data: Historical data available from January 2025
- Alerts: Real-time as new data is processed

## CORS

CORS is enabled for the following origins:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Example Usage

### Python
```python
import requests

# Get current data
response = requests.get('http://localhost:8000/api/v1/microplastic/current')
data = response.json()

# Get time series
params = {
    'lat': 35.0,
    'lon': -140.0,
    'start_date': '2025-01-01',
    'end_date': '2025-12-07'
}
response = requests.get('http://localhost:8000/api/v1/microplastic/timeseries', params=params)
timeseries = response.json()
```

### JavaScript
```javascript
// Get current data
fetch('http://localhost:8000/api/v1/microplastic/current')
  .then(response => response.json())
  .then(data => console.log(data));

// Get alerts
fetch('http://localhost:8000/api/v1/alerts?severity=critical')
  .then(response => response.json())
  .then(alerts => console.log(alerts));
```

## Support

For API support, please open an issue on GitHub or contact us at api@aquatrace.example.com
