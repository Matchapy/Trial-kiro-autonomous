#!/usr/bin/env python3
"""
Test script to verify the automation setup

This script checks that all dependencies are installed and
the basic components are working correctly.
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    display_name = package_name or module_name
    try:
        importlib.import_module(module_name)
        print(f"✓ {display_name}")
        return True
    except ImportError as e:
        print(f"✗ {display_name} - {e}")
        return False

def test_directory(path):
    """Test if a directory exists"""
    if path.exists():
        print(f"✓ Directory: {path}")
        return True
    else:
        print(f"✗ Directory missing: {path}")
        return False

def main():
    print("=" * 80)
    print("AWS re:Invent 2025 Research Automation - Setup Test")
    print("=" * 80)
    print()
    
    all_tests_passed = True
    
    # Test Python version
    print("Python Version:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        all_tests_passed = False
    print()
    
    # Test required packages
    print("Required Packages:")
    packages = [
        ('requests', None),
        ('bs4', 'beautifulsoup4'),
        ('selenium', None),
        ('pptx', 'python-pptx'),
        ('PIL', 'Pillow'),
        ('boto3', None),
        ('yaml', 'pyyaml'),
        ('click', None),
        ('tqdm', None),
        ('tenacity', None),
    ]
    
    for module, package in packages:
        if not test_import(module, package):
            all_tests_passed = False
    print()
    
    # Test directory structure
    print("Directory Structure:")
    base_path = Path(__file__).parent
    dirs_to_check = [
        base_path / 'src',
        base_path / 'outputs',
        base_path / 'outputs' / 'screenshots',
        base_path / 'outputs' / 'presentations',
        base_path / 'outputs' / 'data',
    ]
    
    for dir_path in dirs_to_check:
        if not test_directory(dir_path):
            all_tests_passed = False
    print()
    
    # Test source files
    print("Source Files:")
    source_files = [
        base_path / 'src' / 'reinvent_research_automation.py',
        base_path / 'src' / 'aws_documentation_integration.py',
        base_path / 'run_automation.py',
        base_path / 'requirements.txt',
        base_path / 'config.yaml',
    ]
    
    for file_path in source_files:
        if file_path.exists():
            print(f"✓ {file_path.name}")
        else:
            print(f"✗ {file_path.name} missing")
            all_tests_passed = False
    print()
    
    # Test WebDriver (optional)
    print("WebDriver (for screenshots):")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.quit()
            print("✓ Chrome WebDriver is working")
        except Exception as e:
            print(f"⚠ Chrome WebDriver not available: {e}")
            print("  Screenshots will not work, but automation can still run")
    except Exception as e:
        print(f"⚠ Could not test WebDriver: {e}")
    print()
    
    # Final result
    print("=" * 80)
    if all_tests_passed:
        print("✓ All required tests passed!")
        print("\nYou can now run the automation with:")
        print("  python run_automation.py")
    else:
        print("✗ Some tests failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("=" * 80)
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    sys.exit(main())
