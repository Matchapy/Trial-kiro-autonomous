# Deployment Guide

This guide covers different deployment options for the AWS re:Invent 2025 Research Automation.

## Table of Contents

- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Local Deployment

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser
- 2GB+ free disk space
- Internet connection

### Installation Steps

1. **Clone or navigate to the repository**
   ```bash
   cd /projects/sandbox/Trial-kiro-autonomous
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify setup**
   ```bash
   python test_setup.py
   ```

4. **Run the automation**
   ```bash
   python run_automation.py
   ```

### Using Make Commands

If you have `make` installed:

```bash
# Install dependencies
make install

# Test setup
make test

# Run automation
make run

# Quick test run
make run-quick

# Fast run (no screenshots)
make run-fast

# View results
make view-results

# Clean outputs
make clean
```

## Docker Deployment

Docker provides a consistent environment and includes all dependencies.

### Prerequisites

- Docker installed and running
- 2GB+ free disk space

### Building the Image

```bash
# Build the Docker image
docker build -t reinvent-automation:latest .
```

### Running with Docker

#### Basic Run

```bash
docker run -v $(pwd)/outputs:/app/outputs reinvent-automation:latest
```

#### Custom Configuration

```bash
# Run with specific number of services
docker run -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:latest \
  --max-services 5

# Run without screenshots
docker run -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:latest \
  --skip-screenshots

# Run with custom blog URL
docker run -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:latest \
  --blog-url "https://custom-url.com"
```

#### Using Docker Compose

```bash
# Run with docker-compose
docker-compose up

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop and remove containers
docker-compose down
```

### Docker Environment Variables

Set AWS credentials via environment variables:

```bash
docker run \
  -e AWS_ACCESS_KEY_ID="your-key" \
  -e AWS_SECRET_ACCESS_KEY="your-secret" \
  -e AWS_SESSION_TOKEN="your-token" \
  -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:latest
```

Or use a `.env` file with docker-compose:

```bash
# .env file
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_SESSION_TOKEN=your-token
LOG_LEVEL=INFO
```

## Production Deployment

### AWS Lambda Deployment (Future Enhancement)

The automation can be adapted for AWS Lambda:

1. Package the code with dependencies
2. Configure Lambda function with adequate memory (2GB+)
3. Set up CloudWatch Events for scheduling
4. Store outputs in S3

### EC2 Deployment

Running on an EC2 instance:

1. **Launch EC2 instance**
   - AMI: Amazon Linux 2 or Ubuntu
   - Instance type: t3.medium or larger
   - Security group: Allow outbound HTTPS

2. **Install dependencies**
   ```bash
   # Update system
   sudo yum update -y  # or sudo apt-get update

   # Install Python 3.8+
   sudo yum install python3 -y  # or sudo apt-get install python3

   # Install Chrome
   # For Amazon Linux:
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
   sudo yum install -y google-chrome-stable_current_x86_64.rpm

   # For Ubuntu:
   # wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   # sudo apt install ./google-chrome-stable_current_amd64.deb
   ```

3. **Deploy code**
   ```bash
   # Clone repository or copy files
   git clone <repository-url>
   cd Trial-kiro-autonomous

   # Install Python dependencies
   pip3 install -r requirements.txt
   ```

4. **Run automation**
   ```bash
   python3 run_automation.py
   ```

### Scheduled Execution

#### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Run daily at 9 AM
0 9 * * * cd /path/to/Trial-kiro-autonomous && python3 run_automation.py

# Run weekly on Monday at 9 AM
0 9 * * 1 cd /path/to/Trial-kiro-autonomous && python3 run_automation.py
```

#### Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Set action: Start a program
   - Program: `python`
   - Arguments: `run_automation.py`
   - Start in: `C:\path\to\Trial-kiro-autonomous`

#### Using AWS EventBridge

```yaml
# Example CloudFormation template
ScheduledRule:
  Type: AWS::Events::Rule
  Properties:
    ScheduleExpression: "cron(0 9 * * ? *)"  # Daily at 9 AM UTC
    State: ENABLED
    Targets:
      - Arn: !GetAtt LambdaFunction.Arn
        Id: ReInventAutomationTarget
```

## Configuration

### Environment Variables

```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_SESSION_TOKEN="your-token"  # Optional

# Logging
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Custom settings
export MAX_SERVICES=10
export SKIP_SCREENSHOTS=false
```

### Configuration File

Edit `config.yaml` for persistent settings:

```yaml
blog:
  url: "https://www.aboutamazon.com/aws-reinvent-news-updates"
  
research:
  max_services: 10
  max_screenshots: 5
  
screenshots:
  enabled: true
  headless: true
  
output:
  base_dir: "outputs"
```

### Command-Line Options

```bash
python run_automation.py --help

Options:
  --blog-url TEXT           Blog URL to scrape
  --max-services INTEGER    Maximum services to research
  --max-screenshots INTEGER Maximum services to screenshot
  --skip-screenshots        Skip screenshot capture
  --output-dir PATH         Output directory
  --verbose                 Enable verbose logging
```

## Troubleshooting

### Docker Issues

#### Issue: "Cannot connect to Docker daemon"
```bash
# Start Docker service
sudo systemctl start docker

# Or on Mac
open -a Docker
```

#### Issue: "Permission denied" when running Docker
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

#### Issue: Container runs but no outputs
```bash
# Verify volume mount
docker run -v $(pwd)/outputs:/app/outputs \
  --entrypoint ls \
  reinvent-automation:latest \
  -la /app/outputs
```

### Chrome/WebDriver Issues

#### Issue: Chrome not found
```bash
# Install Chrome (Ubuntu/Debian)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Install Chromium (alternative)
sudo apt-get install chromium-browser
```

#### Issue: ChromeDriver version mismatch
```bash
# The webdriver-manager package handles this automatically
# If issues persist, manually specify ChromeDriver version:
pip install webdriver-manager --upgrade
```

### Memory Issues

#### Issue: Out of memory during execution
```bash
# For Docker, increase memory limit
docker run -m 2g -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:latest

# For local execution, reduce max services
python run_automation.py --max-services 5
```

### Network Issues

#### Issue: Unable to connect to blog URL
```bash
# Test connectivity
curl -I https://www.aboutamazon.com/aws-reinvent-news-updates

# Use proxy if needed
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### AWS Credentials Issues

#### Issue: AWS credentials not found
```bash
# Verify credentials
aws sts get-caller-identity

# Or set manually
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

## Monitoring

### Logs

Check logs for detailed execution information:

```bash
# View real-time logs
tail -f outputs/automation.log

# Search for errors
grep ERROR outputs/automation.log

# View last 50 lines
tail -50 outputs/automation.log
```

### Health Checks

Verify automation is working:

```bash
# Check if outputs are being generated
ls -lt outputs/presentations/ | head -5

# Verify recent execution
stat outputs/automation.log

# Count generated screenshots
ls outputs/screenshots/*.png | wc -l
```

## Backup and Archiving

### Backup Outputs

```bash
# Create timestamped backup
tar -czf reinvent-backup-$(date +%Y%m%d-%H%M%S).tar.gz outputs/

# Backup to S3
aws s3 sync outputs/ s3://your-bucket/reinvent-archives/$(date +%Y%m%d)/
```

### Cleanup Old Files

```bash
# Remove outputs older than 30 days
find outputs/ -type f -mtime +30 -delete

# Keep only last 5 presentations
ls -t outputs/presentations/*.pptx | tail -n +6 | xargs rm -f
```

## Performance Optimization

### Parallel Execution (Future Enhancement)

```python
# Modify the code to use multiprocessing
from multiprocessing import Pool

def research_service_parallel(service):
    # Research logic here
    pass

with Pool(processes=4) as pool:
    results = pool.map(research_service_parallel, services)
```

### Caching

```bash
# Use persistent cache directory
mkdir -p .cache
export CACHE_DIR=.cache
```

### Resource Limits

For Docker:

```yaml
# docker-compose.yml
services:
  reinvent-automation:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## Security Considerations

### Credentials Management

1. **Never commit credentials to Git**
   ```bash
   # Verify .gitignore includes
   cat .gitignore | grep -E "credentials|secrets|.env"
   ```

2. **Use AWS Secrets Manager**
   ```python
   import boto3
   
   secrets = boto3.client('secretsmanager')
   response = secrets.get_secret_value(SecretId='reinvent-automation-creds')
   ```

3. **Use IAM roles on EC2**
   - Attach IAM role to EC2 instance
   - No need to manage credentials manually

### Network Security

1. **Use VPC endpoints for AWS services**
2. **Enable VPC Flow Logs for monitoring**
3. **Use Security Groups to restrict access**

### Data Security

1. **Encrypt sensitive outputs**
   ```bash
   # Encrypt presentation
   gpg -c outputs/presentations/AWS_reInvent_2025_Services.pptx
   ```

2. **Use S3 with encryption**
   ```bash
   # Upload with server-side encryption
   aws s3 cp outputs/ s3://bucket/ --recursive --sse AES256
   ```

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Rebuild Docker image
docker build -t reinvent-automation:latest --no-cache .
```

### Monitoring

Set up monitoring for:
- Execution success/failure
- Execution time
- Output file sizes
- Error rates

### Alerts

Configure alerts for:
- Failed executions
- Missing outputs
- Execution time > threshold
- Disk space issues

---

**Need Help?**

- Check the [README.md](README.md) for general documentation
- See [QUICKSTART.md](QUICKSTART.md) for quick start guide
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system details
- Check logs in `outputs/automation.log` for error messages
