"""
NASA CYGNSS Data Fetcher
Retrieves CYGNSS Level 2 data from NASA PO.DAAC
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import earthaccess
import xarray as xr
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


class CYGNSSFetcher:
    """
    Fetches and processes NASA CYGNSS (Cyclone Global Navigation Satellite System) data
    
    CYGNSS measures ocean surface roughness using reflected GPS signals.
    Changes in roughness can indicate microplastic concentrations.
    """
    
    def __init__(self, username: str = None, password: str = None):
        """
        Initialize CYGNSS data fetcher
        
        Args:
            username: NASA Earthdata username
            password: NASA Earthdata password
        """
        self.username = username or os.getenv("NASA_USERNAME")
        self.password = password or os.getenv("NASA_PASSWORD")
        self.token = os.getenv("NASA_EARTHDATA_TOKEN")
        self.data_dir = Path(os.getenv("RAW_DATA_DIR", "./data/raw"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """
        Authenticate with NASA Earthdata
        
        Returns:
            True if authentication successful
        """
        try:
            earthaccess.login(username=self.username, password=self.password)
            self.authenticated = True
            logger.info("Successfully authenticated with NASA Earthdata")
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def search_data(
        self,
        start_date: datetime,
        end_date: datetime,
        bbox: Optional[List[float]] = None
    ) -> List[Dict]:
        """
        Search for CYGNSS data granules
        
        Args:
            start_date: Start date for data search
            end_date: End date for data search
            bbox: Bounding box [min_lon, min_lat, max_lon, max_lat]
        
        Returns:
            List of data granules metadata
        """
        if not self.authenticated:
            self.authenticate()
        
        try:
            # CYGNSS Level 2 Ocean Surface Heat Flux Product
            # Short name: CYGNSS_L2_SURFACE_FLUX
            # or CYGNSS_L2_V3.1 for general Level 2 data
            
            results = earthaccess.search_data(
                short_name="CYGNSS_L2_V3.1",
                temporal=(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                bounding_box=bbox if bbox else None
            )
            
            logger.info(f"Found {len(results)} CYGNSS granules")
            return results
            
        except Exception as e:
            logger.error(f"Error searching CYGNSS data: {e}")
            return []
    
    def download_data(
        self,
        granules: List,
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Download CYGNSS data granules
        
        Args:
            granules: List of granule objects from search
            output_dir: Output directory for downloaded files
        
        Returns:
            List of downloaded file paths
        """
        output_dir = output_dir or self.data_dir / "cygnss"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            downloaded_files = earthaccess.download(
                granules,
                str(output_dir)
            )
            
            logger.info(f"Downloaded {len(downloaded_files)} files to {output_dir}")
            return [Path(f) for f in downloaded_files]
            
        except Exception as e:
            logger.error(f"Error downloading CYGNSS data: {e}")
            return []
    
    def process_granule(self, file_path: Path) -> pd.DataFrame:
        """
        Process a CYGNSS NetCDF granule and extract relevant variables
        
        Args:
            file_path: Path to CYGNSS NetCDF file
        
        Returns:
            DataFrame with extracted variables
        """
        try:
            ds = xr.open_dataset(file_path)
            
            # Extract key variables for microplastic detection:
            # - surface_roughness: Mean square slope of ocean surface
            # - wind_speed: For normalization
            # - lat/lon: Location
            # - reflectivity: Signal strength
            
            data = {
                'latitude': ds['lat'].values.flatten(),
                'longitude': ds['lon'].values.flatten(),
                'surface_roughness': ds.get('mean_square_slope', ds.get('brcs', None)),
                'wind_speed': ds.get('wind_speed', None),
                'timestamp': ds['time'].values.flatten()
            }
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Remove NaN values
            df = df.dropna()
            
            logger.info(f"Processed {len(df)} observations from {file_path.name}")
            return df
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return pd.DataFrame()
    
    def fetch_recent_data(self, days: int = 7) -> pd.DataFrame:
        """
        Fetch and process recent CYGNSS data
        
        Args:
            days: Number of days of recent data to fetch
        
        Returns:
            Combined DataFrame of all recent observations
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        logger.info(f"Fetching CYGNSS data from {start_date} to {end_date}")
        
        # Search for data
        granules = self.search_data(start_date, end_date)
        
        if not granules:
            logger.warning("No CYGNSS data found for specified period")
            return pd.DataFrame()
        
        # Download data
        files = self.download_data(granules)
        
        # Process all files
        all_data = []
        for file_path in files:
            df = self.process_granule(file_path)
            if not df.empty:
                all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            logger.info(f"Combined {len(combined_df)} total observations")
            return combined_df
        else:
            return pd.DataFrame()


def main():
    """Test the CYGNSS fetcher"""
    fetcher = CYGNSSFetcher()
    
    # Fetch last 3 days of data
    df = fetcher.fetch_recent_data(days=3)
    
    if not df.empty:
        print(f"Successfully fetched {len(df)} CYGNSS observations")
        print(df.head())
    else:
        print("No data retrieved")


if __name__ == "__main__":
    main()
