# Architecture Documentation

## System Overview

The AWS re:Invent 2025 Research Automation is a modular Python-based system that automates the complete workflow from blog scraping to presentation generation.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface Layer                         │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  CLI Interface   │         │  Configuration   │             │
│  │ run_automation.py│         │   config.yaml    │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           ReInventResearchAutomation                      │  │
│  │         (Main Workflow Coordinator)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Data Layer    │  │  Integration     │  │  Output Layer    │
│                │  │  Layer           │  │                  │
│ • BlogScraper  │  │ • AWS Docs API   │  │ • Presentation   │
│ • Data Storage │  │ • AWS Pricing    │  │   Generator      │
│ • Caching      │  │ • AWS Console    │  │ • Screenshot     │
│                │  │   (Selenium)     │  │   Storage        │
└────────────────┘  └──────────────────┘  └──────────────────┘
```

## Component Architecture

### 1. Core Components

#### A. ReInventResearchAutomation (Orchestrator)
**Purpose**: Main workflow coordinator

**Responsibilities**:
- Initialize all components
- Coordinate workflow steps
- Handle errors and retries
- Generate final outputs

**Key Methods**:
```python
- run()                    # Main execution method
- load_aws_credentials()   # Credential management
- _generate_presentation() # Presentation creation
- _generate_summary_report() # Report generation
```

#### B. BlogScraper
**Purpose**: Extract announcements from AWS blog

**Responsibilities**:
- HTTP request handling
- HTML parsing
- Announcement extraction
- Service name identification

**Key Methods**:
```python
- extract_announcements()   # Main extraction logic
- _extract_service_name()   # Parse service names
- _get_sample_announcements() # Fallback data
```

**Data Flow**:
```
Blog URL → HTTP Request → HTML Content → BeautifulSoup Parser
    → Filter Announcements → Extract Service Names → JSON Output
```

#### C. AWSDocumentationResearcher
**Purpose**: Research services using AWS documentation

**Responsibilities**:
- Documentation search
- Content extraction
- Information structuring

**Integration Points**:
- AWS Documentation MCP Server
- AWS Pricing MCP Server

**Key Methods**:
```python
- research_service()       # Main research method
- extract_service_information() # Information extraction
```

#### D. AWSConsoleScreenshotter
**Purpose**: Capture AWS Console screenshots

**Responsibilities**:
- WebDriver management
- Console navigation
- Screenshot capture
- Image storage

**Key Methods**:
```python
- setup_driver()           # Initialize Selenium
- login_to_console()       # Handle authentication
- capture_service_console() # Take screenshots
- close()                  # Cleanup
```

**Technology Stack**:
- Selenium WebDriver
- Chrome/Chromium browser
- ChromeDriver (auto-managed)

#### E. PresentationGenerator
**Purpose**: Generate PowerPoint presentations

**Responsibilities**:
- Slide creation
- Content formatting
- Image embedding
- File generation

**Key Methods**:
```python
- add_title_slide()        # Title slide
- add_service_overview_slide() # Overview
- add_pricing_slide()      # Pricing info
- add_screenshot_slide()   # Screenshots
- save()                   # Write PPTX file
```

### 2. Integration Components

#### A. AWSDocumentationIntegration
**Purpose**: Interface with AWS Documentation MCP tools

**MCP Tools Used**:
```python
- search_documentation()   # Search AWS docs
- read_documentation()     # Read doc pages
- get_recommendations()    # Get related docs
```

**Data Structure**:
```json
{
  "service_name": "Amazon Bedrock",
  "overview": "...",
  "key_features": [...],
  "use_cases": [...],
  "documentation_urls": [...]
}
```

#### B. AWSPricingIntegration
**Purpose**: Interface with AWS Pricing MCP tools

**MCP Tools Used**:
```python
- get_service_codes()      # List service codes
- get_pricing()            # Get pricing data
- get_pricing_attributes() # Get pricing dimensions
```

**Data Structure**:
```json
{
  "service_code": "AmazonBedrock",
  "pricing_model": "Pay-as-you-go",
  "free_tier": "...",
  "pricing_details": {...}
}
```

## Data Flow Architecture

### Complete Workflow

```
1. Blog Scraping
   ┌──────────────┐
   │  Blog URL    │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ HTTP Request │
   └──────┬───────┘
          │
          ▼
   ┌──────────────────┐
   │ HTML Parsing     │
   │ (BeautifulSoup)  │
   └──────┬───────────┘
          │
          ▼
   ┌──────────────────┐
   │ Announcements    │
   │ List             │
   └──────┬───────────┘
          │
          │
2. Research Phase
          │
          ▼
   ┌──────────────────┐
   │ For Each Service │
   └──────┬───────────┘
          │
          ├────────────────┐
          │                │
          ▼                ▼
   ┌──────────┐    ┌──────────┐
   │ AWS Docs │    │ AWS      │
   │ Search   │    │ Pricing  │
   └────┬─────┘    └────┬─────┘
        │               │
        └───────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ Research     │
         │ Results      │
         └──────┬───────┘
                │
                │
3. Screenshot Capture
                │
                ▼
         ┌──────────────┐
         │ For Each     │
         │ Service      │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ WebDriver    │
         │ Navigation   │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ Screenshot   │
         │ Files        │
         └──────┬───────┘
                │
                │
4. Presentation Generation
                │
                ▼
         ┌──────────────┐
         │ PPTX Builder │
         └──────┬───────┘
                │
                ├─ Title Slide
                ├─ TOC Slide
                ├─ Service Slides
                │  ├─ Overview
                │  ├─ Problems/Benefits
                │  ├─ Pricing
                │  ├─ Examples
                │  └─ Screenshots
                │
                ▼
         ┌──────────────┐
         │ Final PPTX   │
         └──────────────┘
```

## File Organization

```
Trial-kiro-autonomous/
│
├── src/                              # Source code
│   ├── reinvent_research_automation.py  # Main automation
│   └── aws_documentation_integration.py # MCP integration
│
├── examples/                         # Example code
│   └── mcp_integration_example.py    # MCP usage examples
│
├── outputs/                          # Generated files
│   ├── screenshots/                  # PNG screenshots
│   ├── presentations/                # PPTX files
│   ├── data/                        # JSON & TXT data
│   └── automation.log               # Execution logs
│
├── config.yaml                       # Configuration
├── requirements.txt                  # Dependencies
├── run_automation.py                 # CLI wrapper
├── test_setup.py                     # Setup validator
├── Makefile                         # Common commands
│
└── Documentation
    ├── README.md                     # Main documentation
    ├── QUICKSTART.md                 # Quick start guide
    └── ARCHITECTURE.md               # This file
```

## Technology Stack

### Core Technologies
- **Python 3.8+**: Main programming language
- **Requests**: HTTP client for web scraping
- **BeautifulSoup4**: HTML parsing
- **Selenium**: Browser automation
- **python-pptx**: PowerPoint generation

### AWS Integration
- **AWS Documentation MCP Server**: Documentation access
- **AWS Pricing MCP Server**: Pricing information
- **Boto3**: AWS SDK (optional, for direct AWS access)

### Supporting Libraries
- **Click**: CLI interface
- **PyYAML**: Configuration management
- **Pillow**: Image processing
- **tqdm**: Progress bars
- **tenacity**: Retry logic

## Design Patterns

### 1. Service Layer Pattern
Each major functionality is encapsulated in its own class:
- `BlogScraper` - Blog data extraction
- `AWSDocumentationResearcher` - Research logic
- `AWSConsoleScreenshotter` - Screenshot capture
- `PresentationGenerator` - PPTX generation

### 2. Orchestrator Pattern
`ReInventResearchAutomation` coordinates all services and manages the workflow.

### 3. Integration Pattern
Separate integration modules (`AWSDocumentationIntegration`, `AWSPricingIntegration`) abstract MCP tool interactions.

### 4. Configuration Pattern
Externalized configuration in `config.yaml` for easy customization.

## Error Handling Strategy

### Levels of Error Handling

1. **Component Level**
   - Each component handles its own errors
   - Logs errors with context
   - Returns appropriate error indicators

2. **Orchestrator Level**
   - Catches component errors
   - Decides whether to continue or abort
   - Maintains workflow state

3. **User Level**
   - Clear error messages
   - Actionable suggestions
   - Graceful degradation

### Fallback Strategies

- **Blog Scraping Fails**: Use sample data
- **Documentation Unavailable**: Use cached data
- **Screenshots Fail**: Continue without screenshots
- **Pricing Unavailable**: Mark as "N/A"

## Scalability Considerations

### Current Limitations
- Sequential processing (one service at a time)
- Single-threaded execution
- Limited caching

### Future Enhancements
- Parallel processing for multiple services
- Distributed caching (Redis)
- Async/await for I/O operations
- Message queue for large-scale processing

## Security Considerations

### Credential Management
- Never hardcode credentials
- Use environment variables
- Support AWS Secrets Manager
- Secure credential storage

### Data Privacy
- Screenshots may contain sensitive data
- Logs should not contain credentials
- Temporary files should be cleaned up

### Network Security
- HTTPS for all external requests
- Certificate verification enabled
- Timeout configurations
- Rate limiting

## Performance Optimization

### Current Optimizations
- Caching of documentation searches
- Reuse of WebDriver sessions
- Batch processing where possible

### Metrics
- Typical execution time: 5-10 minutes for 10 services
- Memory usage: ~200-500 MB
- Network bandwidth: Moderate (mainly for screenshots)

## Testing Strategy

### Test Levels
1. **Setup Tests**: Verify dependencies and configuration
2. **Unit Tests**: Test individual components
3. **Integration Tests**: Test MCP tool interactions
4. **End-to-End Tests**: Complete workflow validation

### Test Execution
```bash
# Setup validation
python test_setup.py

# Quick test with limited data
python run_automation.py --max-services 1

# Full test
python run_automation.py
```

## Monitoring and Logging

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for recoverable issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

### Log Locations
- Console output (real-time)
- `outputs/automation.log` (persistent)

### Key Metrics Logged
- Services processed
- Screenshots captured
- Errors encountered
- Execution time per phase

## Extension Points

### Adding New Data Sources
1. Create new scraper class
2. Implement `extract_announcements()` method
3. Register with orchestrator

### Adding New Output Formats
1. Create new generator class
2. Implement `generate()` method
3. Add to output configuration

### Adding New Research Sources
1. Extend `AWSDocumentationIntegration`
2. Add new MCP tool calls
3. Update data structure

## Deployment Considerations

### Local Deployment
- Direct Python execution
- Virtual environment recommended
- Manual dependency installation

### Containerized Deployment (Future)
- Docker container with all dependencies
- Headless Chrome included
- Volume mounts for outputs

### Scheduled Execution (Future)
- Cron job setup
- AWS Lambda deployment
- Event-driven triggers

## Maintenance

### Regular Updates
- Keep dependencies updated
- Monitor blog structure changes
- Update service mappings
- Review and update documentation

### Backup Strategy
- Version control for code
- Backup configuration files
- Archive important presentations
- Retain execution logs

---

**Version**: 1.0.0  
**Last Updated**: December 3, 2024  
**Maintainer**: AWS Research Team
