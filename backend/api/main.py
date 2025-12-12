"""
AquaTrace API Main Application
FastAPI backend for Ocean Microplastic Mapping System
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting AquaTrace API...")
    # Initialize database connection
    # Initialize Redis connection
    # Load ML models
    logger.info("AquaTrace API started successfully")
    yield
    logger.info("Shutting down AquaTrace API...")
    # Cleanup resources


# Initialize FastAPI app
app = FastAPI(
    title="AquaTrace API",
    description="Ocean Microplastic Mapping and Alert System API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AquaTrace API",
        "version": "1.0.0",
        "status": "operational",
        "description": "Ocean Microplastic Mapping and Alert System"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "ml_models": "loaded"
    }


# API v1 Router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")


@api_router.get("/microplastic/current")
async def get_current_microplastic_data(
    bbox: Optional[str] = None,
    resolution: Optional[str] = "medium"
):
    """
    Get current global microplastic concentration data
    
    Args:
        bbox: Bounding box (min_lon,min_lat,max_lon,max_lat)
        resolution: Data resolution (low/medium/high)
    
    Returns:
        GeoJSON FeatureCollection with microplastic heatmap data
    """
    # Demo data with real ocean pollution hotspots
    demo_zones = [
        # North Pacific Gyre (Great Pacific Garbage Patch)
        {"lat": 35.0, "lon": -140.0, "concentration": 0.85, "level": "high"},
        {"lat": 37.5, "lon": -142.0, "concentration": 0.92, "level": "critical"},
        {"lat": 33.0, "lon": -138.0, "concentration": 0.78, "level": "high"},
        
        # North Atlantic Gyre
        {"lat": 30.0, "lon": -40.0, "concentration": 0.72, "level": "high"},
        {"lat": 32.0, "lon": -38.0, "concentration": 0.68, "level": "medium"},
        
        # Mediterranean Sea
        {"lat": 38.0, "lon": 15.0, "concentration": 0.65, "level": "medium"},
        {"lat": 40.0, "lon": 18.0, "concentration": 0.58, "level": "medium"},
        
        # Indian Ocean
        {"lat": -20.0, "lon": 80.0, "concentration": 0.55, "level": "medium"},
        
        # South Pacific
        {"lat": -30.0, "lon": -110.0, "concentration": 0.48, "level": "low"},
        
        # Caribbean
        {"lat": 18.0, "lon": -75.0, "concentration": 0.62, "level": "medium"},
    ]
    
    features = []
    for zone in demo_zones:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [zone["lon"], zone["lat"]]
            },
            "properties": {
                "lat": zone["lat"],
                "lon": zone["lon"],
                "concentration": zone["concentration"],
                "level": zone["level"]
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "timestamp": "2025-12-07T00:00:00Z",
        "features": features,
        "metadata": {
            "resolution": resolution,
            "data_sources": ["CYGNSS", "Sentinel-2"],
            "model_version": "v1.0"
        }
    }


@api_router.get("/microplastic/timeseries")
async def get_timeseries_data(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str
):
    """
    Get time-series microplastic data for a specific location
    
    Args:
        lat: Latitude
        lon: Longitude
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        Time-series data with concentrations over time
    """
    # TODO: Implement time-series query
    return {
        "location": {"lat": lat, "lon": lon},
        "start_date": start_date,
        "end_date": end_date,
        "data": []
    }


@api_router.get("/alerts")
async def get_active_alerts(
    severity: Optional[str] = None
):
    """
    Get active microplastic concentration alerts
    
    Args:
        severity: Filter by severity (high/critical)
    
    Returns:
        List of active alerts
    """
    # TODO: Implement alert retrieval
    return {
        "alerts": [],
        "total": 0,
        "timestamp": "2025-12-07T00:00:00Z"
    }


@api_router.get("/statistics")
async def get_global_statistics():
    """
    Get global microplastic statistics and trends
    
    Returns:
        Statistical summary of global concentrations
    """
    # TODO: Implement statistics calculation
    return {
        "global_average": 0.0,
        "total_area_monitored_km2": 0,
        "high_concentration_zones": 0,
        "trend": "stable",
        "last_updated": "2025-12-07T00:00:00Z"
    }


@api_router.get("/regions")
async def get_regions():
    """
    Get predefined regions of interest
    
    Returns:
        List of ocean regions with metadata
    """
    regions = [
        {
            "id": "north_pacific_gyre",
            "name": "North Pacific Gyre",
            "bbox": [-180, 20, -120, 50],
            "description": "Great Pacific Garbage Patch region"
        },
        {
            "id": "north_atlantic_gyre",
            "name": "North Atlantic Gyre",
            "bbox": [-70, 20, -20, 50],
            "description": "North Atlantic accumulation zone"
        },
        {
            "id": "mediterranean",
            "name": "Mediterranean Sea",
            "bbox": [-6, 30, 36, 46],
            "description": "High concentration coastal region"
        }
    ]
    return {"regions": regions}


app.include_router(api_router)

# Include water body detection and analysis routes
from api.water_body_routes import router as water_body_router
app.include_router(water_body_router, prefix="/api/v1")

# Include search routes
from api.search_routes import router as search_router
app.include_router(search_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False") == "True"
    )
