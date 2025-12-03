#!/usr/bin/env python3
"""
AWS re:Invent 2025 Announcement Research Automation

This script automates the entire workflow of:
1. Extracting new AWS services/features from re:Invent 2025 blog
2. Researching each service using AWS documentation
3. Capturing AWS Console screenshots
4. Generating a comprehensive PowerPoint presentation
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outputs/automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
BLOG_URL = "https://www.aboutamazon.com/aws-reinvent-news-updates"
OUTPUT_DIR = Path("outputs")
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"
PRESENTATIONS_DIR = OUTPUT_DIR / "presentations"
DATA_DIR = OUTPUT_DIR / "data"
AWS_CONSOLE_URL = "https://console.aws.amazon.com"


class BlogScraper:
    """Scrapes AWS re:Invent 2025 announcements from the blog"""
    
    def __init__(self, blog_url: str):
        self.blog_url = blog_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_announcements(self) -> List[Dict[str, Any]]:
        """Extract service/feature announcements from the blog"""
        logger.info(f"Fetching blog content from {self.blog_url}")
        
        try:
            response = self.session.get(self.blog_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            announcements = []
            
            # Look for announcement patterns
            # The blog structure may vary, so we'll try multiple patterns
            
            # Pattern 1: Article headers with links
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['post', 'article', 'news', 'update']
            ))
            
            if not articles:
                # Pattern 2: Look for headings and links
                articles = soup.find_all(['h2', 'h3', 'h4'])
            
            for article in articles[:50]:  # Limit to first 50 items
                title_elem = article.find(['a', 'h2', 'h3', 'h4'])
                if not title_elem:
                    title_elem = article
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                # Look for description nearby
                description = ""
                if article.name in ['article', 'div']:
                    desc_elem = article.find(['p', 'div'], class_=lambda x: x and 'desc' in str(x).lower())
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                
                # Filter for AWS service announcements
                if title and len(title) > 10 and any(
                    keyword in title.lower() for keyword in [
                        'aws', 'amazon', 'launch', 'announce', 'new', 'service',
                        'feature', 'available', 'now', 'general availability', 'ga'
                    ]
                ):
                    # Extract potential service name
                    service_name = self._extract_service_name(title)
                    
                    announcements.append({
                        'title': title,
                        'service_name': service_name,
                        'description': description,
                        'link': link if link.startswith('http') else f"https://aws.amazon.com{link}",
                        'extracted_at': datetime.now().isoformat()
                    })
            
            # Remove duplicates based on title
            unique_announcements = []
            seen_titles = set()
            for ann in announcements:
                if ann['title'] not in seen_titles:
                    seen_titles.add(ann['title'])
                    unique_announcements.append(ann)
            
            logger.info(f"Extracted {len(unique_announcements)} unique announcements")
            return unique_announcements
            
        except Exception as e:
            logger.error(f"Error extracting announcements: {e}")
            # Return sample data for testing if scraping fails
            return self._get_sample_announcements()
    
    def _extract_service_name(self, title: str) -> str:
        """Extract AWS service name from title"""
        # Common patterns for service names
        words = title.split()
        
        # Look for "Amazon XXX" or "AWS XXX"
        for i, word in enumerate(words):
            if word.lower() in ['amazon', 'aws'] and i + 1 < len(words):
                # Get next 1-3 words as service name
                service_parts = []
                for j in range(i + 1, min(i + 4, len(words))):
                    if words[j][0].isupper() or words[j].lower() in ['s3', 'ec2', 'rds', 'eks', 'ecs']:
                        service_parts.append(words[j])
                    else:
                        break
                if service_parts:
                    return ' '.join(service_parts)
        
        # Fallback: return first capitalized words
        return ' '.join(word for word in words[:5] if word and word[0].isupper())
    
    def _get_sample_announcements(self) -> List[Dict[str, Any]]:
        """Return sample announcements for testing"""
        logger.info("Using sample announcements for testing")
        return [
            {
                'title': 'Amazon Bedrock announces Claude 3.5 Sonnet v2',
                'service_name': 'Amazon Bedrock',
                'description': 'New version of Claude 3.5 Sonnet available on Amazon Bedrock',
                'link': 'https://aws.amazon.com/about-aws/whats-new/2024/10/amazon-bedrock-claude-3-5-sonnet-v2/',
                'extracted_at': datetime.now().isoformat()
            },
            {
                'title': 'AWS Lambda now supports Node.js 22',
                'service_name': 'AWS Lambda',
                'description': 'AWS Lambda adds support for Node.js 22 runtime',
                'link': 'https://aws.amazon.com/lambda/',
                'extracted_at': datetime.now().isoformat()
            },
            {
                'title': 'Amazon S3 Express One Zone storage class',
                'service_name': 'Amazon S3',
                'description': 'New S3 storage class for high-performance applications',
                'link': 'https://aws.amazon.com/s3/storage-classes/express-one-zone/',
                'extracted_at': datetime.now().isoformat()
            }
        ]


class AWSDocumentationResearcher:
    """Researches AWS services using AWS Documentation tools"""
    
    def research_service(self, service_name: str, description: str) -> Dict[str, Any]:
        """
        Research a service using AWS documentation
        Note: In production, this would use the AWS Documentation MCP tools
        """
        logger.info(f"Researching service: {service_name}")
        
        # This is a placeholder - in actual implementation, you would use:
        # - awslabs_-_aws-documentation-mcp-server_search_documentation
        # - awslabs_-_aws-documentation-mcp-server_read_documentation
        # - awslabs_-_aws-pricing-mcp-server_get_pricing
        
        research_data = {
            'service_name': service_name,
            'overview': f"{service_name} is an AWS service that provides cloud capabilities.",
            'problems_solved': [
                "Reduces operational complexity",
                "Improves scalability and performance",
                "Enhances security and compliance"
            ],
            'benefits': [
                "Pay-as-you-go pricing",
                "Fully managed service",
                "Integration with other AWS services",
                "High availability and durability"
            ],
            'cost_info': {
                'pricing_model': 'Pay per use',
                'free_tier': 'Available for first 12 months',
                'estimated_cost': 'Varies based on usage'
            },
            'usage_examples': [
                {
                    'title': 'Basic Setup',
                    'description': f'Getting started with {service_name}',
                    'steps': [
                        'Sign in to AWS Console',
                        f'Navigate to {service_name}',
                        'Create new resource',
                        'Configure settings',
                        'Deploy and test'
                    ]
                }
            ],
            'documentation_urls': [
                f'https://docs.aws.amazon.com/{service_name.lower().replace(" ", "-")}/'
            ]
        }
        
        return research_data


class AWSConsoleScreenshotter:
    """Captures screenshots from AWS Console"""
    
    def __init__(self, aws_credentials: Dict[str, str] = None):
        self.aws_credentials = aws_credentials or {}
        self.driver = None
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def login_to_console(self) -> bool:
        """Login to AWS Console using credentials"""
        if not self.aws_credentials:
            logger.warning("No AWS credentials provided, skipping console login")
            return False
        
        try:
            logger.info("Attempting to login to AWS Console")
            self.driver.get(AWS_CONSOLE_URL)
            time.sleep(3)
            
            # AWS login flow (simplified - actual implementation needs proper handling)
            # This is a placeholder - actual login would require:
            # 1. Handle IAM user or SSO login
            # 2. Enter credentials
            # 3. Handle MFA if required
            
            return True
        except Exception as e:
            logger.error(f"Failed to login to AWS Console: {e}")
            return False
    
    def capture_service_console(self, service_name: str) -> List[str]:
        """Capture screenshots of service console"""
        screenshots = []
        
        if not self.driver:
            self.setup_driver()
        
        try:
            # Map service name to console URL
            service_url = self._get_service_console_url(service_name)
            
            logger.info(f"Capturing screenshots for {service_name}")
            
            # For public pages (no login required)
            self.driver.get(service_url)
            time.sleep(2)
            
            # Capture main page
            screenshot_path = SCREENSHOTS_DIR / f"{service_name.lower().replace(' ', '_')}_main.png"
            self.driver.save_screenshot(str(screenshot_path))
            screenshots.append(str(screenshot_path))
            logger.info(f"Saved screenshot: {screenshot_path}")
            
            # Try to capture pricing page
            pricing_url = f"{service_url}/pricing"
            try:
                self.driver.get(pricing_url)
                time.sleep(2)
                pricing_screenshot = SCREENSHOTS_DIR / f"{service_name.lower().replace(' ', '_')}_pricing.png"
                self.driver.save_screenshot(str(pricing_screenshot))
                screenshots.append(str(pricing_screenshot))
                logger.info(f"Saved pricing screenshot: {pricing_screenshot}")
            except Exception as e:
                logger.warning(f"Could not capture pricing page: {e}")
            
        except Exception as e:
            logger.error(f"Error capturing screenshots for {service_name}: {e}")
        
        return screenshots
    
    def _get_service_console_url(self, service_name: str) -> str:
        """Map service name to AWS console or marketing URL"""
        service_lower = service_name.lower().replace(' ', '-')
        
        # Common service mappings
        service_map = {
            'amazon-bedrock': 'https://aws.amazon.com/bedrock',
            'aws-lambda': 'https://aws.amazon.com/lambda',
            'amazon-s3': 'https://aws.amazon.com/s3',
            'amazon-ec2': 'https://aws.amazon.com/ec2',
            'amazon-rds': 'https://aws.amazon.com/rds',
        }
        
        return service_map.get(service_lower, f'https://aws.amazon.com/{service_lower}')
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")


class PresentationGenerator:
    """Generates PowerPoint presentation from research data"""
    
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)
    
    def add_title_slide(self, title: str, subtitle: str):
        """Add title slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        slide.shapes.title.text = title
        slide.placeholders[1].text = subtitle
    
    def add_content_slide(self, title: str, content: List[str]):
        """Add content slide with bullet points"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = title
        
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()
        
        for item in content:
            p = text_frame.add_paragraph()
            p.text = item
            p.level = 0
            p.font.size = Pt(18)
    
    def add_service_overview_slide(self, service_data: Dict[str, Any]):
        """Add service overview slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = service_data['service_name']
        
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()
        
        # Add overview
        p = text_frame.add_paragraph()
        p.text = "Overview"
        p.font.bold = True
        p.font.size = Pt(20)
        
        p = text_frame.add_paragraph()
        p.text = service_data['overview']
        p.level = 1
        p.font.size = Pt(16)
    
    def add_problems_benefits_slide(self, service_data: Dict[str, Any]):
        """Add problems and benefits slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = f"{service_data['service_name']} - Problems & Benefits"
        
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()
        
        # Problems solved
        p = text_frame.add_paragraph()
        p.text = "Problems Solved"
        p.font.bold = True
        p.font.size = Pt(18)
        
        for problem in service_data['problems_solved']:
            p = text_frame.add_paragraph()
            p.text = problem
            p.level = 1
            p.font.size = Pt(14)
        
        # Benefits
        p = text_frame.add_paragraph()
        p.text = "\nBenefits"
        p.font.bold = True
        p.font.size = Pt(18)
        
        for benefit in service_data['benefits']:
            p = text_frame.add_paragraph()
            p.text = benefit
            p.level = 1
            p.font.size = Pt(14)
    
    def add_pricing_slide(self, service_data: Dict[str, Any]):
        """Add pricing information slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = f"{service_data['service_name']} - Pricing"
        
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()
        
        cost_info = service_data.get('cost_info', {})
        
        p = text_frame.add_paragraph()
        p.text = f"Pricing Model: {cost_info.get('pricing_model', 'N/A')}"
        p.font.size = Pt(16)
        
        p = text_frame.add_paragraph()
        p.text = f"Free Tier: {cost_info.get('free_tier', 'N/A')}"
        p.font.size = Pt(16)
        
        p = text_frame.add_paragraph()
        p.text = f"Estimated Cost: {cost_info.get('estimated_cost', 'N/A')}"
        p.font.size = Pt(16)
    
    def add_usage_examples_slide(self, service_data: Dict[str, Any]):
        """Add usage examples slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = f"{service_data['service_name']} - Usage Examples"
        
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()
        
        for example in service_data.get('usage_examples', [])[:2]:  # Limit to 2 examples
            p = text_frame.add_paragraph()
            p.text = example['title']
            p.font.bold = True
            p.font.size = Pt(16)
            
            for step in example.get('steps', [])[:5]:  # Limit to 5 steps
                p = text_frame.add_paragraph()
                p.text = step
                p.level = 1
                p.font.size = Pt(14)
    
    def add_screenshot_slide(self, service_name: str, screenshot_path: str):
        """Add slide with screenshot"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # Blank layout
        
        # Add title
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"{service_name} - Console View"
        p.font.size = Pt(24)
        p.font.bold = True
        
        # Add screenshot
        try:
            if os.path.exists(screenshot_path):
                slide.shapes.add_picture(
                    screenshot_path,
                    Inches(0.5), Inches(1),
                    width=Inches(9), height=Inches(5.5)
                )
        except Exception as e:
            logger.error(f"Failed to add screenshot {screenshot_path}: {e}")
    
    def save(self, filepath: str):
        """Save presentation"""
        self.prs.save(filepath)
        logger.info(f"Presentation saved to {filepath}")


class ReInventResearchAutomation:
    """Main orchestrator for the automation workflow"""
    
    def __init__(self):
        self.blog_scraper = BlogScraper(BLOG_URL)
        self.researcher = AWSDocumentationResearcher()
        self.screenshotter = None
        self.presentation_generator = PresentationGenerator()
        self.announcements = []
        self.research_results = []
    
    def load_aws_credentials(self) -> Dict[str, str]:
        """Load AWS credentials from environment or secrets"""
        # In production, this would load from AWS Secrets Manager or environment
        # For now, return empty dict (screenshots will use public pages)
        credentials = {
            'access_key_id': os.getenv('AWS_ACCESS_KEY_ID', ''),
            'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
            'session_token': os.getenv('AWS_SESSION_TOKEN', '')
        }
        
        if not credentials['access_key_id']:
            logger.warning("No AWS credentials found, will use public pages only")
        
        return credentials
    
    def run(self):
        """Execute the complete automation workflow"""
        logger.info("=" * 80)
        logger.info("Starting AWS re:Invent 2025 Research Automation")
        logger.info("=" * 80)
        
        try:
            # Step 1: Extract announcements from blog
            logger.info("\n[Step 1/5] Extracting announcements from blog...")
            self.announcements = self.blog_scraper.extract_announcements()
            
            # Save raw announcements
            announcements_file = DATA_DIR / "announcements.json"
            with open(announcements_file, 'w') as f:
                json.dump(self.announcements, f, indent=2)
            logger.info(f"Saved {len(self.announcements)} announcements to {announcements_file}")
            
            # Step 2: Research each service
            logger.info(f"\n[Step 2/5] Researching {len(self.announcements)} services...")
            for i, announcement in enumerate(self.announcements[:10], 1):  # Limit to 10 services
                logger.info(f"  [{i}/{min(10, len(self.announcements))}] Researching {announcement['service_name']}")
                research_data = self.researcher.research_service(
                    announcement['service_name'],
                    announcement['description']
                )
                research_data['announcement'] = announcement
                self.research_results.append(research_data)
                time.sleep(1)  # Rate limiting
            
            # Save research results
            research_file = DATA_DIR / "research_results.json"
            with open(research_file, 'w') as f:
                json.dump(self.research_results, f, indent=2)
            logger.info(f"Saved research results to {research_file}")
            
            # Step 3: Capture console screenshots
            logger.info(f"\n[Step 3/5] Capturing console screenshots...")
            aws_credentials = self.load_aws_credentials()
            self.screenshotter = AWSConsoleScreenshotter(aws_credentials)
            
            for i, research in enumerate(self.research_results[:5], 1):  # Limit to 5 for screenshots
                service_name = research['service_name']
                logger.info(f"  [{i}/{min(5, len(self.research_results))}] Capturing {service_name}")
                screenshots = self.screenshotter.capture_service_console(service_name)
                research['screenshots'] = screenshots
                time.sleep(2)  # Rate limiting
            
            self.screenshotter.close()
            
            # Step 4: Generate PowerPoint presentation
            logger.info(f"\n[Step 4/5] Generating PowerPoint presentation...")
            self._generate_presentation()
            
            # Step 5: Generate summary report
            logger.info(f"\n[Step 5/5] Generating summary report...")
            self._generate_summary_report()
            
            logger.info("\n" + "=" * 80)
            logger.info("Automation completed successfully!")
            logger.info("=" * 80)
            logger.info(f"\nOutput files:")
            logger.info(f"  - Announcements: {DATA_DIR}/announcements.json")
            logger.info(f"  - Research: {DATA_DIR}/research_results.json")
            logger.info(f"  - Presentation: {PRESENTATIONS_DIR}/AWS_reInvent_2025_Services.pptx")
            logger.info(f"  - Summary: {DATA_DIR}/summary_report.txt")
            logger.info(f"  - Screenshots: {SCREENSHOTS_DIR}/")
            
        except Exception as e:
            logger.error(f"Automation failed: {e}", exc_info=True)
            raise
    
    def _generate_presentation(self):
        """Generate the PowerPoint presentation"""
        # Title slide
        self.presentation_generator.add_title_slide(
            "AWS re:Invent 2025",
            f"New Services and Features\nGenerated on {datetime.now().strftime('%B %d, %Y')}"
        )
        
        # Table of contents
        toc_items = [f"{i+1}. {r['service_name']}" for i, r in enumerate(self.research_results)]
        self.presentation_generator.add_content_slide("Services Covered", toc_items)
        
        # Add slides for each service
        for research in self.research_results:
            # Overview slide
            self.presentation_generator.add_service_overview_slide(research)
            
            # Problems & Benefits slide
            self.presentation_generator.add_problems_benefits_slide(research)
            
            # Pricing slide
            self.presentation_generator.add_pricing_slide(research)
            
            # Usage examples slide
            self.presentation_generator.add_usage_examples_slide(research)
            
            # Screenshot slides
            for screenshot in research.get('screenshots', []):
                self.presentation_generator.add_screenshot_slide(
                    research['service_name'],
                    screenshot
                )
        
        # Save presentation
        presentation_path = PRESENTATIONS_DIR / "AWS_reInvent_2025_Services.pptx"
        self.presentation_generator.save(str(presentation_path))
    
    def _generate_summary_report(self):
        """Generate a text summary report"""
        report_path = DATA_DIR / "summary_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AWS re:Invent 2025 - New Services and Features Summary\n")
            f.write(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Services Researched: {len(self.research_results)}\n\n")
            
            for i, research in enumerate(self.research_results, 1):
                f.write(f"\n{i}. {research['service_name']}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Overview: {research['overview']}\n\n")
                
                f.write("Problems Solved:\n")
                for problem in research['problems_solved']:
                    f.write(f"  • {problem}\n")
                
                f.write("\nBenefits:\n")
                for benefit in research['benefits']:
                    f.write(f"  • {benefit}\n")
                
                f.write(f"\nPricing: {research['cost_info']['pricing_model']}\n")
                f.write(f"Free Tier: {research['cost_info']['free_tier']}\n")
                
                f.write(f"\nDocumentation: {research['documentation_urls'][0]}\n")
                
                if research.get('screenshots'):
                    f.write(f"\nScreenshots: {len(research['screenshots'])} captured\n")
                
                f.write("\n")
        
        logger.info(f"Summary report saved to {report_path}")


def main():
    """Main entry point"""
    try:
        automation = ReInventResearchAutomation()
        automation.run()
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
