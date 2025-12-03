# Installation Verification Guide

Quick verification steps to ensure the automation is ready to use.

## ✅ Pre-Installation Checklist

### 1. Python Version
```bash
python3 --version
# Should be Python 3.8 or higher
```

### 2. Repository Files
```bash
ls -la /projects/sandbox/Trial-kiro-autonomous/
# Should see all source files, documentation, and configuration
```

### 3. Directory Structure
```bash
tree -L 2 /projects/sandbox/Trial-kiro-autonomous/
# Or: find . -type d | head -10
```

Expected structure:
```
Trial-kiro-autonomous/
├── src/
├── examples/
├── outputs/
├── requirements.txt
├── config.yaml
├── Dockerfile
└── [documentation files]
```

## ✅ Installation Steps

### 1. Install Dependencies
```bash
cd /projects/sandbox/Trial-kiro-autonomous
pip install -r requirements.txt
```

Expected output:
```
Successfully installed beautifulsoup4-4.12.3 requests-2.31.0 selenium-4.16.0 ...
```

### 2. Verify Installation
```bash
python test_setup.py
```

Expected output:
```
✓ Python 3.x.x
✓ requests
✓ beautifulsoup4
✓ selenium
✓ python-pptx
...
✓ All required tests passed!
```

## ✅ Docker Verification (Optional)

### 1. Build Docker Image
```bash
docker build -t reinvent-automation:test .
```

Expected: No errors, image builds successfully

### 2. Test Docker Run
```bash
docker run --name test-run \
  -v $(pwd)/outputs:/app/outputs \
  reinvent-automation:test \
  --max-services 1 --skip-screenshots
```

Expected: Container completes successfully (exit 0)

### 3. Verify Outputs
```bash
ls -lh outputs/presentations/
ls -lh outputs/data/
```

Expected: Files present

### 4. Cleanup
```bash
docker rm test-run
```

## ✅ Functional Tests

### Test 1: Quick Run
```bash
python run_automation.py --max-services 1 --skip-screenshots
```

**Expected Results:**
- ✓ Script completes without errors
- ✓ Log file created: `outputs/automation.log`
- ✓ Data files created in `outputs/data/`
- ✓ Presentation created in `outputs/presentations/`

### Test 2: With Screenshots
```bash
python run_automation.py --max-services 1
```

**Expected Results:**
- ✓ All Test 1 results
- ✓ Screenshots created in `outputs/screenshots/`
- ✓ Chrome/WebDriver works

### Test 3: Configuration
```bash
python run_automation.py --help
```

**Expected Results:**
- ✓ Help message displays
- ✓ All options listed
- ✓ No errors

## ✅ Verification Checklist

### File Verification
- [ ] All source files present (4 Python files in src/)
- [ ] All documentation present (5 .md files)
- [ ] Configuration files present (config.yaml, requirements.txt)
- [ ] Docker files present (Dockerfile, docker-compose.yml)
- [ ] Examples present (2 files in examples/)

### Functionality Verification
- [ ] Dependencies install successfully
- [ ] Python syntax valid (no import errors)
- [ ] Docker builds successfully
- [ ] Docker runs successfully
- [ ] Test script completes successfully
- [ ] Output files generated

### Output Verification
- [ ] PowerPoint file created (.pptx)
- [ ] JSON data files created
- [ ] Summary report created (.txt)
- [ ] Log file created
- [ ] Screenshots captured (if enabled)

## ✅ Common Issues and Solutions

### Issue: Python version too old
**Solution:**
```bash
# Install Python 3.8+
# Ubuntu: sudo apt install python3.8
# Mac: brew install python@3.8
```

### Issue: pip install fails
**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

### Issue: Chrome/ChromeDriver not found
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# Mac
brew install --cask google-chrome

# Or skip screenshots
python run_automation.py --skip-screenshots
```

### Issue: Docker build fails
**Solution:**
```bash
# Check Docker is running
docker info

# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t reinvent-automation:test .
```

### Issue: Permission denied
**Solution:**
```bash
# Make scripts executable
chmod +x run_automation.py test_setup.py

# Or run with python
python3 run_automation.py
```

## ✅ Success Indicators

You know the installation is successful when:

1. **Test script passes:**
   ```
   ✓ All required tests passed!
   ```

2. **Quick run completes:**
   ```
   ✓ Automation completed successfully!
   ```

3. **Files are generated:**
   ```bash
   $ ls outputs/presentations/
   AWS_reInvent_2025_Services.pptx
   ```

4. **Docker works (optional):**
   ```bash
   $ docker ps -a | grep reinvent
   [container] ... Exited (0) ...
   ```

## ✅ Next Steps

After verification:

1. **Review generated presentation:**
   ```bash
   open outputs/presentations/AWS_reInvent_2025_Services.pptx
   ```

2. **Read documentation:**
   ```bash
   cat README.md
   cat QUICKSTART.md
   ```

3. **Customize configuration:**
   ```bash
   vi config.yaml
   ```

4. **Run with desired settings:**
   ```bash
   python run_automation.py --max-services 10
   ```

## ✅ Support

If issues persist:

1. Check logs: `cat outputs/automation.log`
2. Run with verbose: `python run_automation.py --verbose`
3. Test with minimal config: `python run_automation.py --max-services 1 --skip-screenshots`
4. Review documentation: `cat README.md`

---

**Installation Verified?** ✓  
**Ready to Use?** ✓  
**Enjoy the automation!** 🚀
