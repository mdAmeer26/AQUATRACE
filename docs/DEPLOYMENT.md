# Deployment Guide

This guide provides instructions for deploying AquaTrace to production.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ with PostGIS
- Redis server
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

## System Requirements

### Minimum Requirements
- 4 CPU cores
- 16 GB RAM
- 500 GB storage (for satellite data)
- 100 Mbps network connection

### Recommended Requirements
- 8+ CPU cores
- 32+ GB RAM
- 2 TB SSD storage
- 1 Gbps network connection

## Backend Deployment

### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql postgis redis-server nginx

# Install GDAL
sudo apt install -y gdal-bin libgdal-dev
```

### 2. Database Setup

```bash
# Create database
sudo -u postgres createdb aquatrace
sudo -u postgres psql -c "CREATE USER aquatrace WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aquatrace TO aquatrace;"

# Enable PostGIS
sudo -u postgres psql aquatrace -c "CREATE EXTENSION postgis;"
```

### 3. Application Setup

```bash
# Clone repository
git clone https://github.com/yourusername/aquatrace.git
cd aquatrace

# Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production settings
nano .env
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Configure Systemd Service

Create `/etc/systemd/system/aquatrace-api.service`:

```ini
[Unit]
Description=AquaTrace API
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=aquatrace
Group=aquatrace
WorkingDirectory=/opt/aquatrace/backend
Environment="PATH=/opt/aquatrace/backend/venv/bin"
ExecStart=/opt/aquatrace/backend/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable aquatrace-api
sudo systemctl start aquatrace-api
```

### 6. Configure Celery for Background Tasks

Create `/etc/systemd/system/aquatrace-worker.service`:

```ini
[Unit]
Description=AquaTrace Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=aquatrace
Group=aquatrace
WorkingDirectory=/opt/aquatrace/backend
Environment="PATH=/opt/aquatrace/backend/venv/bin"
ExecStart=/opt/aquatrace/backend/venv/bin/celery -A tasks worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

## Frontend Deployment

### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
```

### 2. Configure Nginx

Create `/etc/nginx/sites-available/aquatrace`:

```nginx
server {
    listen 80;
    server_name aquatrace.example.com;

    # Frontend
    location / {
        root /opt/aquatrace/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/aquatrace /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Setup SSL with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d aquatrace.example.com
```

## Scheduled Tasks

### Setup Cron Jobs

```bash
crontab -e
```

Add the following:
```cron
# Fetch new satellite data daily at 2 AM
0 2 * * * cd /opt/aquatrace && /opt/aquatrace/backend/venv/bin/python scripts/fetch_data.py --source all --days 1

# Process data daily at 4 AM
0 4 * * * cd /opt/aquatrace && /opt/aquatrace/backend/venv/bin/python scripts/process_data.py

# Generate heatmap daily at 5 AM
0 5 * * * cd /opt/aquatrace && /opt/aquatrace/backend/venv/bin/python scripts/generate_heatmap.py
```

## Monitoring

### 1. Application Logs

```bash
# API logs
sudo journalctl -u aquatrace-api -f

# Worker logs
sudo journalctl -u aquatrace-worker -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. System Monitoring

Install monitoring tools:
```bash
sudo apt install -y htop iotop nethogs
```

### 3. Database Monitoring

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('aquatrace'));

-- Active connections
SELECT count(*) FROM pg_stat_activity;
```

## Backup Strategy

### Database Backup

Create backup script `/opt/aquatrace/scripts/backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/aquatrace"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U aquatrace aquatrace | gzip > $BACKUP_DIR/aquatrace_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "aquatrace_*.sql.gz" -mtime +30 -delete
```

Schedule daily backups:
```cron
0 1 * * * /opt/aquatrace/scripts/backup_db.sh
```

### Data Backup

```bash
# Backup processed data
rsync -av /opt/aquatrace/data/ /backup/aquatrace/data/
```

## Security Considerations

1. **Firewall Configuration**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

2. **API Rate Limiting** - Configure in production settings

3. **Database Security** - Use strong passwords, restrict access

4. **API Keys** - Store sensitive keys in environment variables

5. **Regular Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## Scaling

### Horizontal Scaling

- Use load balancer (e.g., HAProxy, AWS ALB)
- Deploy multiple API instances
- Shared database and Redis
- S3 or object storage for satellite data

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Cache frequently accessed data
- CDN for static assets

## Troubleshooting

### API Not Responding
```bash
sudo systemctl status aquatrace-api
sudo journalctl -u aquatrace-api --since "10 minutes ago"
```

### Database Connection Issues
```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT version();"
```

### High Memory Usage
```bash
htop
free -h
df -h
```

## Performance Optimization

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_lat_lon ON microplastic_data (lat, lon);
   CREATE INDEX idx_timestamp ON microplastic_data (timestamp);
   ```

2. **Redis Caching** - Cache API responses

3. **CDN** - Use CloudFlare or AWS CloudFront

4. **Database Connection Pooling** - Configure in production

## Support

For deployment issues:
- Check logs first
- Review troubleshooting section
- Open GitHub issue with details
- Contact: deploy@aquatrace.example.com
