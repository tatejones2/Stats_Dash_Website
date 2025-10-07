#!/bin/bash
# Script to run tests with coverage and open the HTML report

echo "Running tests with coverage..."
/home/tatejones/StatsDashSite/.venv/bin/python -m pytest --cov=. --cov-report=term-missing --cov-report=html

echo ""
echo "Coverage report generated!"
echo "HTML report available at: htmlcov/index.html"
echo ""
echo "To view the HTML report, run:"
echo "  xdg-open htmlcov/index.html"
echo ""