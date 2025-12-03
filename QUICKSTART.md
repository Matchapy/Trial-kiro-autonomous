# Quick Start Guide

Get started with AWS re:Invent 2025 Research Automation in 5 minutes!

## 1. Installation (2 minutes)

```bash
# Navigate to the project directory
cd /projects/sandbox/Trial-kiro-autonomous

# Install Python dependencies
pip install -r requirements.txt
```

## 2. Verify Setup (1 minute)

```bash
# Run the setup test
python test_setup.py
```

Expected output:
```
✓ All required tests passed!
```

## 3. Run the Automation (2 minutes)

### Basic Run
```bash
# Run with default settings
python run_automation.py
```

### Quick Test Run
```bash
# Test with limited services (faster)
python run_automation.py --max-services 3 --max-screenshots 2
```

### Skip Screenshots (Fastest)
```bash
# Run without screenshot capture
python run_automation.py --skip-screenshots
```

## 4. View Results

After execution completes, check these files:

### 📊 PowerPoint Presentation
```bash
# Location: outputs/presentations/AWS_reInvent_2025_Services.pptx
open outputs/presentations/AWS_reInvent_2025_Services.pptx
```

### 📄 Summary Report
```bash
# Location: outputs/data/summary_report.txt
cat outputs/data/summary_report.txt
```

### 📷 Screenshots
```bash
# Location: outputs/screenshots/
ls -lh outputs/screenshots/
```

### 📋 Raw Data
```bash
# View extracted announcements
cat outputs/data/announcements.json | python -m json.tool

# View research results
cat outputs/data/research_results.json | python -m json.tool
```

## Common Use Cases

### Research Specific Number of Services
```bash
python run_automation.py --max-services 5
```

### Use Custom Blog URL
```bash
python run_automation.py --blog-url "https://your-blog-url.com"
```

### Enable Verbose Logging
```bash
python run_automation.py --verbose
```

### Combine Options
```bash
python run_automation.py \
  --max-services 8 \
  --max-screenshots 4 \
  --verbose
```

## Directory Structure

```
Trial-kiro-autonomous/
├── outputs/
│   ├── presentations/          # ← Your PPTX files
│   │   └── AWS_reInvent_2025_Services.pptx
│   ├── data/                   # ← JSON data and reports
│   │   ├── announcements.json
│   │   ├── research_results.json
│   │   └── summary_report.txt
│   ├── screenshots/            # ← Console screenshots
│   │   ├── amazon_bedrock_main.png
│   │   └── ...
│   └── automation.log          # ← Execution logs
```

## Troubleshooting

### Issue: Import errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: Chrome/WebDriver error
```bash
# Solution: Install Chrome
# Ubuntu/Debian:
sudo apt-get install chromium-browser

# macOS:
brew install --cask google-chrome
```

### Issue: Blog scraping fails
**Solution**: The tool will use sample data automatically for testing.
Check `outputs/automation.log` for details.

## Next Steps

1. ✅ Review the generated PowerPoint presentation
2. 📖 Read the full [README.md](README.md) for detailed documentation
3. 🔧 Customize settings in [config.yaml](config.yaml)
4. 🚀 Integrate with AWS Documentation MCP tools (see examples/)

## Help

```bash
# Show all available options
python run_automation.py --help
```

## Success Indicators

✅ **Successful Run**: You should see these files:
- `outputs/presentations/AWS_reInvent_2025_Services.pptx`
- `outputs/data/announcements.json`
- `outputs/data/research_results.json`
- `outputs/data/summary_report.txt`
- Multiple PNG files in `outputs/screenshots/`

✅ **Log Check**: `outputs/automation.log` should end with:
```
Automation completed successfully!
```

## Pro Tips

💡 **Start Small**: Use `--max-services 1` to test the complete workflow quickly

💡 **Check Logs**: Always review `outputs/automation.log` for detailed execution info

💡 **Screenshots Optional**: Skip screenshots with `--skip-screenshots` for faster execution

💡 **Customize Config**: Edit `config.yaml` for persistent settings changes

## Time Estimates

- **Quick Test** (1-2 services): ~30 seconds
- **Small Run** (3-5 services): ~2-3 minutes  
- **Medium Run** (10 services): ~5-7 minutes
- **Full Run** (20+ services): ~10-15 minutes

Times vary based on network speed and screenshot capture.

---

**Ready to go!** 🚀

Run: `python run_automation.py` and watch the automation work!
