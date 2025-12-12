"""
Heatmap Generation Script
Generates map tiles for visualization
"""

import argparse
import logging
from datetime import datetime
import sys
from pathlib import Path
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_heatmap():
    """Generate heatmap tiles from processed data"""
    logger.info("Generating heatmap tiles...")
    
    # Load latest processed data
    processed_dir = Path("./data/processed")
    
    if not processed_dir.exists():
        logger.error("No processed data directory found")
        return
    
    # Find latest heatmap file
    heatmap_files = sorted(processed_dir.glob("heatmap_*.json"), reverse=True)
    
    if not heatmap_files:
        logger.warning("No heatmap files found")
        return
    
    latest_file = heatmap_files[0]
    logger.info(f"Using heatmap from {latest_file}")
    
    with open(latest_file, 'r') as f:
        heatmap_data = json.load(f)
    
    logger.info(f"Heatmap contains {len(heatmap_data['zones'])} zones")
    
    # Generate GeoJSON for web display
    geojson = {
        "type": "FeatureCollection",
        "timestamp": heatmap_data['timestamp'],
        "features": []
    }
    
    for zone in heatmap_data['zones']:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [zone['lon'], zone['lat']]
            },
            "properties": {
                "concentration": zone['concentration'],
                "level": zone['level'],
                "lat": zone['lat'],
                "lon": zone['lon']
            }
        }
        geojson['features'].append(feature)
    
    # Save GeoJSON
    output_file = processed_dir / "current_heatmap.geojson"
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    logger.info(f"Generated GeoJSON with {len(geojson['features'])} features")
    logger.info(f"Saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate heatmap tiles')
    
    args = parser.parse_args()
    
    try:
        generate_heatmap()
        logger.info("Heatmap generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error during heatmap generation: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
