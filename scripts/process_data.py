"""
Data Processing Script
Processes raw satellite data and generates heatmaps
"""

import argparse
import logging
from datetime import datetime
import sys
from pathlib import Path
import pandas as pd

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.processing.pipeline import DataProcessor
from backend.ml_models.detector import MicroplasticDetector
from backend.utils.alerts import AlertManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_latest_cygnss_data() -> pd.DataFrame:
    """Load most recent CYGNSS data file"""
    data_dir = Path("./data/raw/cygnss")
    
    if not data_dir.exists():
        logger.warning("No CYGNSS data directory found")
        return pd.DataFrame()
    
    # Find most recent file
    csv_files = sorted(data_dir.glob("cygnss_*.csv"), reverse=True)
    
    if not csv_files:
        logger.warning("No CYGNSS CSV files found")
        return pd.DataFrame()
    
    latest_file = csv_files[0]
    logger.info(f"Loading data from {latest_file}")
    
    df = pd.read_csv(latest_file)
    logger.info(f"Loaded {len(df)} observations")
    
    return df


def process_data(date: str = None):
    """
    Process satellite data for specified date
    
    Args:
        date: Date string (YYYY-MM-DD), defaults to today
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Processing data for {date}...")
    
    # Load CYGNSS data
    cygnss_df = load_latest_cygnss_data()
    
    if cygnss_df.empty:
        logger.error("No CYGNSS data available for processing")
        return
    
    # Initialize processor
    processor = DataProcessor()
    
    # Run processing pipeline
    heatmap = processor.process_pipeline(cygnss_df)
    
    logger.info(f"Processing complete. Generated heatmap with {len(heatmap['zones'])} zones")
    
    # Process alerts
    alert_manager = AlertManager()
    alerts = alert_manager.process_heatmap(heatmap)
    
    logger.info(f"Generated {len(alerts)} new alerts")
    
    # Print summary
    stats = alert_manager.get_alert_statistics()
    logger.info(f"Alert statistics: {stats}")


def main():
    parser = argparse.ArgumentParser(description='Process satellite data')
    parser.add_argument(
        '--date',
        type=str,
        help='Date to process (YYYY-MM-DD), defaults to today'
    )
    
    args = parser.parse_args()
    
    try:
        process_data(date=args.date)
        logger.info("Data processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data processing: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
