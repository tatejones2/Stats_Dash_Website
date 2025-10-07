# Baseball Team Stats Dashboard

This is a Streamlit-based dashboard for visualizing baseball team statistics. Data is fetched from a Google Sheets file and updated weekly. The dashboard allows interactive charting and analysis similar to Power BI.

## Features
- Fetches live data from Google Sheets
- Interactive charts (scatter plots, bar charts, etc.)
- Filter and explore stats

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your Google Sheets credentials and sheet URL
3. Run the app: `streamlit run app.py`

## Files
- `app.py`: Main Streamlit app
- `sheets.py`: Google Sheets data fetching
- `requirements.txt`: Python dependencies
- `tests/`: Test files for pytest
- `.pylintrc`: Pylint configuration
- `pytest.ini`: Pytest configuration
- `.coveragerc`: Coverage configuration
- `htmlcov/`: HTML coverage reports (generated)

## Testing and Linting
- Run tests: `pytest tests/ -v`
- Run tests with coverage: `pytest --cov=. --cov-report=term-missing --cov-report=html`
- Run linting: `pylint *.py`
- Use VS Code tasks: Ctrl+Shift+P -> "Tasks: Run Task" -> Select:
  - "Run Tests"
  - "Run Tests with Coverage"
  - "Run Pylint"

## Coverage Reports
- Terminal coverage report shows missing lines
- HTML coverage report saved to `htmlcov/index.html`
- Current coverage: **93%** overall
- View HTML report: Open `htmlcov/index.html` in browser

## Note
Replace placeholder credentials and sheet URL with your own.