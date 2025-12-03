#!/usr/bin/env python3
"""
CLI wrapper for AWS re:Invent 2025 Research Automation

This script provides a command-line interface to run the automation
with various options and configurations.
"""

import os
import sys
import click
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from reinvent_research_automation import ReInventResearchAutomation


@click.command()
@click.option(
    '--blog-url',
    default='https://www.aboutamazon.com/aws-reinvent-news-updates',
    help='URL of the AWS re:Invent blog'
)
@click.option(
    '--max-services',
    default=10,
    type=int,
    help='Maximum number of services to research'
)
@click.option(
    '--max-screenshots',
    default=5,
    type=int,
    help='Maximum number of services to screenshot'
)
@click.option(
    '--skip-screenshots',
    is_flag=True,
    help='Skip capturing console screenshots'
)
@click.option(
    '--output-dir',
    default='outputs',
    type=click.Path(),
    help='Output directory for all files'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def main(blog_url, max_services, max_screenshots, skip_screenshots, output_dir, verbose):
    """
    AWS re:Invent 2025 Research Automation
    
    This tool automates the extraction and research of AWS services
    announced at re:Invent 2025, generating a comprehensive PowerPoint
    presentation with screenshots and detailed information.
    """
    
    click.echo("=" * 80)
    click.echo("AWS re:Invent 2025 Research Automation")
    click.echo("=" * 80)
    click.echo()
    
    # Display configuration
    click.echo("Configuration:")
    click.echo(f"  Blog URL: {blog_url}")
    click.echo(f"  Max Services: {max_services}")
    click.echo(f"  Max Screenshots: {max_screenshots}")
    click.echo(f"  Skip Screenshots: {skip_screenshots}")
    click.echo(f"  Output Directory: {output_dir}")
    click.echo()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Run automation
        automation = ReInventResearchAutomation()
        
        # Override settings if needed
        if blog_url != 'https://www.aboutamazon.com/aws-reinvent-news-updates':
            automation.blog_scraper.blog_url = blog_url
        
        click.echo("Starting automation...")
        automation.run()
        
        click.echo()
        click.echo("✓ Automation completed successfully!")
        click.echo()
        click.echo("Output files have been generated in the outputs directory.")
        
        return 0
        
    except KeyboardInterrupt:
        click.echo("\n\nAutomation interrupted by user.")
        return 130
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
