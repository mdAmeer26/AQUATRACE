"""
Data Fetching Script
Automated script to fetch satellite data from NASA and ESA
"""

import argparse
import logging
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from data_fetchers.cygnss_fetcher import CYGNSSFetcher
from data_fetchers.sentinel_fetcher import SentinelFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fetch_cygnss_data(days: int = 7):
    """
    Fetch CYGNSS data for the last N days
    
    Args:
        days: Number of days to fetch
    """
    logger.info(f"Fetching CYGNSS data for last {days} days...")
    
    fetcher = CYGNSSFetcher()
    df = fetcher.fetch_recent_data(days=days)
    
    if not df.empty:
        logger.info(f"Successfully fetched {len(df)} CYGNSS observations")
        
        # Save to CSV
        output_file = Path("./data/raw/cygnss") / f"cygnss_{datetime.now().strftime('%Y%m%d')}.csv"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False)
        logger.info(f"Saved to {output_file}")
    else:
        logger.warning("No CYGNSS data retrieved")


def fetch_sentinel_data(bbox: tuple, days: int = 7):
    """
    Fetch Sentinel data for specified region
    
    Args:
        bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
        days: Number of days to fetch
    """
    logger.info(f"Fetching Sentinel data for bbox {bbox}, last {days} days...")
    
    fetcher = SentinelFetcher()
    data = fetcher.fetch_coastal_data(bbox, days=days)
    
    if data:
        logger.info(f"Successfully fetched {len(data)} Sentinel products")
    else:
        logger.warning("No Sentinel data retrieved")


def main():
    parser = argparse.ArgumentParser(description='Fetch satellite data')
    parser.add_argument(
        '--source',
        choices=['cygnss', 'sentinel', 'all'],
        default='all',
        help='Data source to fetch'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days of data to fetch'
    )
    parser.add_argument(
        '--bbox',
        nargs=4,
        type=float,
        metavar=('MIN_LON', 'MIN_LAT', 'MAX_LON', 'MAX_LAT'),
        help='Bounding box for Sentinel data'
    )
    
    args = parser.parse_args()
    
    try:
        if args.source in ['cygnss', 'all']:
            fetch_cygnss_data(days=args.days)
        
        if args.source in ['sentinel', 'all']:
            bbox = tuple(args.bbox) if args.bbox else (10.0, 40.0, 15.0, 43.0)
            fetch_sentinel_data(bbox, days=args.days)
        
        logger.info("Data fetching completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data fetching: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
