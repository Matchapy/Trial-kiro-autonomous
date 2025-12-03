.PHONY: help install test run run-quick run-fast clean view-results examples

help:
	@echo "AWS re:Invent 2025 Research Automation - Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make test          - Test the setup"
	@echo "  make run           - Run the automation (default settings)"
	@echo "  make run-quick     - Quick run (3 services, 2 screenshots)"
	@echo "  make run-fast      - Fast run (5 services, no screenshots)"
	@echo "  make clean         - Clean output files"
	@echo "  make view-results  - Show summary of results"
	@echo "  make examples      - Run MCP integration examples"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Installation complete"

test:
	@echo "Testing setup..."
	python test_setup.py

run:
	@echo "Running automation with default settings..."
	python run_automation.py

run-quick:
	@echo "Running quick test (3 services)..."
	python run_automation.py --max-services 3 --max-screenshots 2

run-fast:
	@echo "Running fast (no screenshots)..."
	python run_automation.py --max-services 5 --skip-screenshots

clean:
	@echo "Cleaning output files..."
	rm -f outputs/data/*.json
	rm -f outputs/data/*.txt
	rm -f outputs/presentations/*.pptx
	rm -f outputs/screenshots/*.png
	rm -f outputs/*.log
	@echo "✓ Output files cleaned"

view-results:
	@echo "=== Results Summary ==="
	@echo ""
	@echo "Presentations:"
	@ls -lh outputs/presentations/*.pptx 2>/dev/null || echo "  No presentations found"
	@echo ""
	@echo "Data Files:"
	@ls -lh outputs/data/*.json outputs/data/*.txt 2>/dev/null || echo "  No data files found"
	@echo ""
	@echo "Screenshots:"
	@ls -lh outputs/screenshots/*.png 2>/dev/null | wc -l | xargs -I {} echo "  {} screenshot(s) captured"
	@echo ""
	@echo "Logs:"
	@ls -lh outputs/*.log 2>/dev/null || echo "  No log files found"

examples:
	@echo "Running MCP integration examples..."
	python examples/mcp_integration_example.py
