"""
Alert System
Monitors microplastic concentrations and generates alerts for critical thresholds
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Alert data structure"""
    id: str
    severity: str  # 'medium', 'high', 'critical'
    title: str
    description: str
    lat: float
    lon: float
    concentration: float
    timestamp: str
    region: Optional[str] = None
    source: Optional[str] = None
    acknowledged: bool = False


class AlertManager:
    """
    Manages alert generation, storage, and notification
    """
    
    def __init__(self):
        self.alerts_dir = Path(os.getenv("PROCESSED_DATA_DIR", "./data/processed")) / "alerts"
        self.alerts_dir.mkdir(parents=True, exist_ok=True)
        
        # Thresholds from environment
        self.thresholds = {
            'medium': float(os.getenv("ALERT_THRESHOLD_MEDIUM", 0.6)),
            'high': float(os.getenv("ALERT_THRESHOLD_HIGH", 0.8)),
            'critical': float(os.getenv("ALERT_THRESHOLD_CRITICAL", 0.95))
        }
        
        self.email_enabled = os.getenv("ALERT_EMAIL_ENABLED", "False") == "True"
        self.email_recipients = os.getenv("ALERT_EMAIL_TO", "").split(",")
        
        self.active_alerts: List[Alert] = []
        self.load_active_alerts()
    
    def evaluate_concentration(
        self,
        lat: float,
        lon: float,
        concentration: float,
        region: Optional[str] = None
    ) -> Optional[Alert]:
        """
        Evaluate if concentration triggers an alert
        
        Args:
            lat: Latitude
            lon: Longitude
            concentration: Microplastic concentration [0-1]
            region: Optional region name
        
        Returns:
            Alert object if threshold exceeded, None otherwise
        """
        severity = None
        
        if concentration >= self.thresholds['critical']:
            severity = 'critical'
        elif concentration >= self.thresholds['high']:
            severity = 'high'
        elif concentration >= self.thresholds['medium']:
            severity = 'medium'
        
        if severity:
            alert = Alert(
                id=f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}_{lat}_{lon}",
                severity=severity,
                title=f"{severity.capitalize()} Microplastic Concentration Detected",
                description=f"Concentration of {concentration*100:.1f}% detected at {lat:.2f}°, {lon:.2f}°",
                lat=lat,
                lon=lon,
                concentration=concentration,
                timestamp=datetime.now().isoformat(),
                region=region,
                source="ML Model"
            )
            
            logger.info(f"Alert generated: {alert.title} at ({lat}, {lon})")
            return alert
        
        return None
    
    def process_heatmap(self, heatmap_data: Dict) -> List[Alert]:
        """
        Process heatmap data and generate alerts
        
        Args:
            heatmap_data: Heatmap data dictionary
        
        Returns:
            List of generated alerts
        """
        new_alerts = []
        
        for zone in heatmap_data.get('zones', []):
            alert = self.evaluate_concentration(
                lat=zone['lat'],
                lon=zone['lon'],
                concentration=zone['concentration'],
                region=zone.get('region')
            )
            
            if alert and not self._is_duplicate(alert):
                new_alerts.append(alert)
                self.active_alerts.append(alert)
        
        if new_alerts:
            self.save_active_alerts()
            
            # Send notifications
            if self.email_enabled:
                self.send_email_notifications(new_alerts)
        
        logger.info(f"Generated {len(new_alerts)} new alerts")
        return new_alerts
    
    def _is_duplicate(self, new_alert: Alert, threshold_km: float = 50.0) -> bool:
        """
        Check if alert is duplicate (same location within threshold)
        
        Args:
            new_alert: New alert to check
            threshold_km: Distance threshold in kilometers
        
        Returns:
            True if duplicate found
        """
        for existing_alert in self.active_alerts:
            if existing_alert.acknowledged:
                continue
            
            # Simple distance check (rough approximation)
            lat_diff = abs(new_alert.lat - existing_alert.lat)
            lon_diff = abs(new_alert.lon - existing_alert.lon)
            distance = ((lat_diff * 111) ** 2 + (lon_diff * 111) ** 2) ** 0.5
            
            if distance < threshold_km:
                logger.debug(f"Duplicate alert found within {distance:.1f}km")
                return True
        
        return False
    
    def get_active_alerts(
        self,
        severity: Optional[str] = None
    ) -> List[Dict]:
        """
        Get active alerts
        
        Args:
            severity: Filter by severity level
        
        Returns:
            List of alert dictionaries
        """
        alerts = self.active_alerts
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        # Filter out acknowledged alerts older than 7 days
        cutoff = datetime.now().timestamp() - (7 * 24 * 60 * 60)
        alerts = [
            a for a in alerts 
            if not a.acknowledged or datetime.fromisoformat(a.timestamp).timestamp() > cutoff
        ]
        
        return [asdict(a) for a in alerts]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Mark alert as acknowledged
        
        Args:
            alert_id: Alert ID
        
        Returns:
            True if successful
        """
        for alert in self.active_alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                self.save_active_alerts()
                logger.info(f"Alert {alert_id} acknowledged")
                return True
        
        return False
    
    def save_active_alerts(self):
        """Save active alerts to file"""
        alerts_file = self.alerts_dir / "active_alerts.json"
        
        with open(alerts_file, 'w') as f:
            json.dump(
                [asdict(a) for a in self.active_alerts],
                f,
                indent=2
            )
        
        logger.debug(f"Saved {len(self.active_alerts)} alerts to {alerts_file}")
    
    def load_active_alerts(self):
        """Load active alerts from file"""
        alerts_file = self.alerts_dir / "active_alerts.json"
        
        if alerts_file.exists():
            with open(alerts_file, 'r') as f:
                alerts_data = json.load(f)
                self.active_alerts = [Alert(**a) for a in alerts_data]
            
            logger.info(f"Loaded {len(self.active_alerts)} alerts from {alerts_file}")
        else:
            logger.debug("No existing alerts file found")
    
    def send_email_notifications(self, alerts: List[Alert]):
        """
        Send email notifications for alerts
        
        Args:
            alerts: List of alerts to send
        """
        if not self.email_recipients or not alerts:
            return
        
        try:
            # Compose email
            subject = f"AquaTrace Alert: {len(alerts)} New Microplastic Detection(s)"
            
            body = "AquaTrace Alert Summary\n"
            body += "=" * 50 + "\n\n"
            
            for alert in alerts:
                body += f"Severity: {alert.severity.upper()}\n"
                body += f"Location: {alert.lat:.2f}°, {alert.lon:.2f}°\n"
                body += f"Concentration: {alert.concentration*100:.1f}%\n"
                body += f"Time: {alert.timestamp}\n"
                body += "-" * 50 + "\n\n"
            
            body += "\nView details at: http://aquatrace.example.com/alerts\n"
            
            # Send email (simplified - needs proper SMTP configuration)
            logger.info(f"Would send email to {self.email_recipients}")
            logger.debug(f"Email body:\n{body}")
            
            # TODO: Implement actual SMTP sending
            # msg = MIMEText(body)
            # msg['Subject'] = subject
            # msg['From'] = os.getenv("SMTP_FROM")
            # msg['To'] = ', '.join(self.email_recipients)
            
            # with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 587))) as server:
            #     server.starttls()
            #     server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            #     server.send_message(msg)
            
        except Exception as e:
            logger.error(f"Failed to send email notifications: {e}")
    
    def get_alert_statistics(self) -> Dict:
        """
        Get alert statistics
        
        Returns:
            Dictionary with alert statistics
        """
        total = len(self.active_alerts)
        
        by_severity = {
            'critical': len([a for a in self.active_alerts if a.severity == 'critical']),
            'high': len([a for a in self.active_alerts if a.severity == 'high']),
            'medium': len([a for a in self.active_alerts if a.severity == 'medium'])
        }
        
        acknowledged = len([a for a in self.active_alerts if a.acknowledged])
        
        return {
            'total': total,
            'by_severity': by_severity,
            'acknowledged': acknowledged,
            'unacknowledged': total - acknowledged
        }


def main():
    """Test the alert system"""
    manager = AlertManager()
    
    # Test alert generation
    test_zones = [
        {'lat': 35.0, 'lon': -140.0, 'concentration': 0.85, 'region': 'North Pacific'},
        {'lat': 30.0, 'lon': -40.0, 'concentration': 0.95, 'region': 'North Atlantic'},
        {'lat': 38.0, 'lon': 15.0, 'concentration': 0.65, 'region': 'Mediterranean'}
    ]
    
    heatmap_data = {'zones': test_zones}
    alerts = manager.process_heatmap(heatmap_data)
    
    print(f"Generated {len(alerts)} alerts")
    print(f"Statistics: {manager.get_alert_statistics()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
