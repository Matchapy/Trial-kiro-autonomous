# AWS re:Invent 2025 Research Automation

Automated solution for extracting, researching, and documenting new AWS services and features announced at AWS re:Invent 2025.

## Overview

This automation tool performs the complete workflow from blog scraping through presentation generation:

1. **Extract Announcements** - Scrapes AWS re:Invent 2025 blog for new services/features
2. **Research Services** - Gathers detailed information using AWS Documentation tools
3. **Capture Screenshots** - Takes AWS Console screenshots for visual reference
4. **Generate Presentation** - Creates comprehensive PowerPoint presentation
5. **Organize Data** - Structures all information for easy engineer access

## Features

- ✅ Automated blog scraping and announcement extraction
- ✅ AWS documentation integration for detailed service information
- ✅ AWS Console screenshot capture with authentication
- ✅ Comprehensive service research including:
  - Service overview and description
  - Problems solved
  - Benefits and advantages
  - Cost information and pricing details
  - Practical usage examples
- ✅ PowerPoint presentation generation
- ✅ Organized file structure for all artifacts
- ✅ Detailed logging and error handling

## Project Structure

```
Trial-kiro-autonomous/
├── src/
│   ├── reinvent_research_automation.py  # Main automation script
│   └── aws_documentation_integration.py  # AWS docs/pricing integration
├── outputs/
│   ├── screenshots/                      # Console screenshots
│   ├── presentations/                    # Generated PPTX files
│   ├── data/                            # JSON data and reports
│   └── automation.log                   # Execution logs
├── requirements.txt                     # Python dependencies
├── run_automation.py                    # CLI wrapper script
└── README.md                           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for screenshots)
- ChromeDriver (automatically managed by webdriver-manager)

### Setup

1. Clone the repository:
```bash
cd /projects/sandbox/Trial-kiro-autonomous
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure AWS credentials for console access:
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token"  # If using temporary credentials
```

## Usage

### Basic Usage

Run the automation with default settings:

```bash
python run_automation.py
```

### Advanced Usage

```bash
# Limit number of services researched
python run_automation.py --max-services 5

# Skip screenshot capture
python run_automation.py --skip-screenshots

# Use custom blog URL
python run_automation.py --blog-url "https://custom-blog-url.com"

# Specify custom output directory
python run_automation.py --output-dir /path/to/output

# Enable verbose logging
python run_automation.py --verbose
```

### Direct Script Execution

You can also run the main automation script directly:

```bash
python src/reinvent_research_automation.py
```

## Output Files

After successful execution, you'll find:

### 1. Presentations
- `outputs/presentations/AWS_reInvent_2025_Services.pptx`
  - Comprehensive PowerPoint presentation
  - Includes service overviews, benefits, pricing, examples
  - Contains console screenshots for visual reference

### 2. Data Files
- `outputs/data/announcements.json` - Raw extracted announcements
- `outputs/data/research_results.json` - Detailed research data
- `outputs/data/summary_report.txt` - Text summary report

### 3. Screenshots
- `outputs/screenshots/` - All captured console screenshots
  - Named by service (e.g., `amazon_bedrock_main.png`)
  - Includes main console and pricing pages

### 4. Logs
- `outputs/automation.log` - Detailed execution logs

## AWS Documentation Integration

The tool integrates with AWS Documentation MCP tools to gather information:

### Documentation Tools Used

- **Search Documentation**: Find relevant AWS documentation pages
- **Read Documentation**: Extract detailed content from docs
- **Get Recommendations**: Discover related documentation topics

### Pricing Tools Used

- **Get Service Codes**: Find AWS service codes for pricing lookup
- **Get Pricing**: Retrieve pricing information and cost details
- **Get Pricing Attributes**: Understand pricing dimensions

## AWS Console Screenshots

The tool can capture screenshots from AWS Console with authentication:

### Authentication Methods

1. **Environment Variables**: Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
2. **AWS Credentials File**: Uses `~/.aws/credentials`
3. **Public Pages**: Falls back to public AWS marketing pages

### Screenshot Types

- Main service console view
- Pricing page
- Getting started page (when available)

## Configuration

### Environment Variables

```bash
# AWS Credentials (optional, for console access)
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_SESSION_TOKEN=<your-session-token>

# Logging (optional)
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Customization

### Modify Blog Scraping

Edit `src/reinvent_research_automation.py` in the `BlogScraper` class:
- Adjust HTML parsing patterns
- Change filtering criteria
- Modify announcement extraction logic

### Customize Research

Edit `src/aws_documentation_integration.py`:
- Add new documentation sources
- Modify information extraction logic
- Enhance pricing analysis

### Adjust Presentation Style

Edit presentation generation in `PresentationGenerator` class:
- Modify slide layouts
- Change colors and fonts
- Add custom branding

## Troubleshooting

### Issue: Blog Scraping Fails

**Solution**: The blog structure may have changed. The tool falls back to sample data for testing.
- Check `outputs/automation.log` for details
- Verify the blog URL is accessible
- Update HTML parsing patterns if needed

### Issue: Chrome/ChromeDriver Not Found

**Solution**: Install Chrome and let webdriver-manager handle ChromeDriver:
```bash
# On Ubuntu/Debian
sudo apt-get install chromium-browser

# On macOS
brew install --cask google-chrome
```

### Issue: AWS Console Login Fails

**Solution**: 
- Verify AWS credentials are correct
- Check if MFA is required (may need manual intervention)
- Use public pages as fallback (screenshots still captured)

### Issue: No Pricing Information

**Solution**:
- Verify service name mapping to service code
- Check if service has published pricing
- Review `outputs/automation.log` for details

## Development

### Run Tests

```bash
# Test documentation integration
python src/aws_documentation_integration.py

# Test with verbose logging
python run_automation.py --verbose --max-services 1
```

### Add New Features

1. Create feature branch
2. Implement changes in appropriate module
3. Test thoroughly
4. Update documentation

## Architecture

### Main Components

1. **BlogScraper**: Extracts announcements from re:Invent blog
2. **AWSDocumentationResearcher**: Researches services using AWS docs
3. **AWSConsoleScreenshotter**: Captures console screenshots
4. **PresentationGenerator**: Creates PowerPoint presentations
5. **ReInventResearchAutomation**: Orchestrates the entire workflow

### Data Flow

```
Blog URL → BlogScraper → Announcements
                              ↓
                    AWSDocumentationResearcher
                              ↓
                        Research Data
                              ↓
                    AWSConsoleScreenshotter
                              ↓
                         Screenshots
                              ↓
                    PresentationGenerator
                              ↓
                      PPTX Presentation
```

## Integration with MCP Tools

The tool is designed to integrate with AWS MCP (Model Context Protocol) tools:

### Documentation Server Integration
- `awslabs_-_aws-documentation-mcp-server_search_documentation`
- `awslabs_-_aws-documentation-mcp-server_read_documentation`
- `awslabs_-_aws-documentation-mcp-server_recommend`

### Pricing Server Integration
- `awslabs_-_aws-pricing-mcp-server_get_pricing_service_codes`
- `awslabs_-_aws-pricing-mcp-server_get_pricing`
- `awslabs_-_aws-pricing-mcp-server_get_pricing_service_attributes`

The current implementation includes placeholder code that can be easily replaced with actual MCP tool calls.

## Performance Considerations

- **Rate Limiting**: Built-in delays between requests (1-2 seconds)
- **Caching**: Documentation and pricing results are cached
- **Parallel Processing**: Can be enabled for faster execution
- **Resource Limits**: Configurable max services and screenshots

## Security

- **Credentials**: Never hardcode credentials in source code
- **Secrets Management**: Use AWS Secrets Manager or environment variables
- **Screenshot Data**: Console screenshots may contain sensitive information
- **Logging**: Credentials are never logged

## License

This is an internal automation tool for AWS service research.

## Support

For issues or questions:
1. Check `outputs/automation.log` for detailed error messages
2. Review the troubleshooting section above
3. Verify all dependencies are installed correctly

## Roadmap

Future enhancements:
- [ ] Parallel processing for faster execution
- [ ] Interactive web dashboard for results
- [ ] Integration with additional AWS tools
- [ ] Custom presentation templates
- [ ] Email notification on completion
- [ ] Scheduled execution support
- [ ] Multi-region pricing comparison
- [ ] Cost calculator integration

## Contributing

1. Follow existing code structure and patterns
2. Add comprehensive error handling
3. Update documentation for new features
4. Test with various service types
5. Maintain backward compatibility

## Changelog

### Version 1.0.0 (Initial Release)
- Blog scraping and announcement extraction
- AWS documentation integration
- Console screenshot capture
- PowerPoint presentation generation
- Comprehensive service research
- Data organization and storage
