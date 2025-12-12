"""
ESA Sentinel Data Fetcher
Retrieves Sentinel-2 optical imagery for coastal plastic detection
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import geopandas as gpd
from shapely.geometry import box
import numpy as np
import rasterio
from rasterio.mask import mask

logger = logging.getLogger(__name__)


class SentinelFetcher:
    """
    Fetches ESA Sentinel-2 satellite imagery for microplastic detection
    
    Sentinel-2 provides high-resolution optical imagery that can detect
    floating plastic aggregations and coastal accumulation zones.
    """
    
    def __init__(self, username: str = None, password: str = None):
        """
        Initialize Sentinel data fetcher
        
        Args:
            username: ESA Copernicus Hub username
            password: ESA Copernicus Hub password
        """
        self.username = username or os.getenv("ESA_USERNAME")
        self.password = password or os.getenv("ESA_PASSWORD")
        self.data_dir = Path(os.getenv("RAW_DATA_DIR", "./data/raw"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.api = None
        self.hub_url = "https://dataspace.copernicus.eu"
    
    def connect(self) -> bool:
        """
        Connect to Sentinel API
        
        Returns:
            True if connection successful
        """
        try:
            self.api = SentinelAPI(
                self.username,
                self.password,
                self.hub_url
            )
            logger.info("Successfully connected to Sentinel Hub")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Sentinel Hub: {e}")
            return False
    
    def search_products(
        self,
        bbox: Tuple[float, float, float, float],
        start_date: datetime,
        end_date: datetime,
        cloud_cover: int = 30,
        platform: str = "Sentinel-2"
    ) -> Dict:
        """
        Search for Sentinel products
        
        Args:
            bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
            start_date: Start date for search
            end_date: End date for search
            cloud_cover: Maximum cloud cover percentage
            platform: Satellite platform (Sentinel-2 or Sentinel-3)
        
        Returns:
            Dictionary of product metadata
        """
        if not self.api:
            self.connect()
        
        try:
            # Create WKT footprint from bounding box
            footprint = box(*bbox).wkt
            
            # Query parameters
            products = self.api.query(
                footprint,
                date=(start_date, end_date),
                platformname=platform,
                cloudcoverpercentage=(0, cloud_cover),
                producttype='S2MSI2A' if platform == "Sentinel-2" else None
            )
            
            logger.info(f"Found {len(products)} Sentinel products")
            return products
            
        except Exception as e:
            logger.error(f"Error searching Sentinel products: {e}")
            return {}
    
    def download_product(
        self,
        product_id: str,
        output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Download a Sentinel product
        
        Args:
            product_id: Product UUID
            output_dir: Output directory
        
        Returns:
            Path to downloaded product
        """
        output_dir = output_dir or self.data_dir / "sentinel"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            result = self.api.download(product_id, directory_path=str(output_dir))
            logger.info(f"Downloaded product to {result['path']}")
            return Path(result['path'])
            
        except Exception as e:
            logger.error(f"Error downloading product {product_id}: {e}")
            return None
    
    def extract_marine_bands(
        self,
        product_path: Path,
        bbox: Optional[Tuple[float, float, float, float]] = None
    ) -> Dict[str, np.ndarray]:
        """
        Extract relevant spectral bands for marine plastic detection
        
        Sentinel-2 bands useful for plastic detection:
        - B2 (Blue, 490nm): Water penetration
        - B3 (Green, 560nm): Chlorophyll absorption
        - B4 (Red, 665nm): Vegetation/algae
        - B8 (NIR, 842nm): Plastic spectral signature
        
        Args:
            product_path: Path to Sentinel product
            bbox: Optional bounding box to crop
        
        Returns:
            Dictionary of band arrays
        """
        try:
            bands = {}
            band_files = {
                'blue': 'B02',
                'green': 'B03',
                'red': 'B04',
                'nir': 'B08'
            }
            
            for band_name, band_id in band_files.items():
                # Find band file
                band_file = list(product_path.rglob(f"*{band_id}*.jp2"))
                
                if band_file:
                    with rasterio.open(band_file[0]) as src:
                        if bbox:
                            # Crop to bounding box
                            geom = [box(*bbox).__geo_interface__]
                            out_image, out_transform = mask(src, geom, crop=True)
                            bands[band_name] = out_image[0]
                        else:
                            bands[band_name] = src.read(1)
            
            logger.info(f"Extracted {len(bands)} bands from {product_path.name}")
            return bands
            
        except Exception as e:
            logger.error(f"Error extracting bands: {e}")
            return {}
    
    def calculate_plastic_index(self, bands: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Calculate Plastic Index (PI) from spectral bands
        
        PI = (NIR - Red) / (NIR + Red)  [Similar to NDVI but optimized for plastics]
        
        Args:
            bands: Dictionary of spectral band arrays
        
        Returns:
            Plastic index array
        """
        try:
            nir = bands['nir'].astype(float)
            red = bands['red'].astype(float)
            
            # Avoid division by zero
            denominator = nir + red
            denominator[denominator == 0] = 0.0001
            
            plastic_index = (nir - red) / denominator
            
            logger.info("Calculated plastic index")
            return plastic_index
            
        except Exception as e:
            logger.error(f"Error calculating plastic index: {e}")
            return np.array([])
    
    def fetch_coastal_data(
        self,
        bbox: Tuple[float, float, float, float],
        days: int = 7
    ) -> List[Dict]:
        """
        Fetch recent Sentinel data for coastal region
        
        Args:
            bbox: Bounding box for area of interest
            days: Number of days of recent data
        
        Returns:
            List of processed data dictionaries
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        logger.info(f"Fetching Sentinel-2 data from {start_date} to {end_date}")
        
        # Search for products
        products = self.search_products(bbox, start_date, end_date)
        
        processed_data = []
        
        # Process top 5 products (to limit data volume)
        for product_id in list(products.keys())[:5]:
            # Download product
            product_path = self.download_product(product_id)
            
            if product_path:
                # Extract bands
                bands = self.extract_marine_bands(product_path, bbox)
                
                if bands:
                    # Calculate plastic index
                    plastic_index = self.calculate_plastic_index(bands)
                    
                    processed_data.append({
                        'product_id': product_id,
                        'metadata': products[product_id],
                        'plastic_index': plastic_index,
                        'bands': bands
                    })
        
        logger.info(f"Processed {len(processed_data)} Sentinel products")
        return processed_data


def main():
    """Test the Sentinel fetcher"""
    # Note: ESA has migrated to Copernicus Data Space Ecosystem
    # Register at: https://dataspace.copernicus.eu/
    fetcher = SentinelFetcher()
    
    # Example: Mediterranean region
    bbox = (10.0, 40.0, 15.0, 43.0)  # Italy coast
    
    # Search for recent products
    if fetcher.connect():
        products = fetcher.search_products(
            bbox,
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
        print(f"Found {len(products)} products")


if __name__ == "__main__":
    main()
