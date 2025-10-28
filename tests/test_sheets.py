import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from sheets import fetch_sheet_data


class TestSheetsModule:
    """Test cases for the sheets module."""

    @patch('sheets.service_account.Credentials.from_service_account_file')
    @patch('sheets.build')
    def test_fetch_sheet_data_success(self, mock_build, mock_creds):
        """Test successful data fetching from Google Sheets."""
        # Mock the credentials
        mock_creds.return_value = MagicMock()
        
        # Mock the Google Sheets API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock the spreadsheet values
        mock_values = [
            ['Player', 'Position', 'Batting Average', 'Home Runs'],
            ['John Doe', 'CF', '0.350', '15'],
            ['Jane Smith', '1B', '0.280', '22']
        ]
        
        mock_service.spreadsheets().values().get().execute.return_value = {
            'values': mock_values
        }
        
        # Call the function
        result = fetch_sheet_data()
        
        # Assertions
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        # The actual code may add extra columns for B-I if missing, so check for expected columns in result
        for col in ['Player', 'Position', 'Batting Average', 'Home Runs']:
            assert col in result.columns
        assert result.iloc[0]['Player'] == 'John Doe'

    @patch('sheets.service_account.Credentials.from_service_account_file')
    @patch('sheets.build')
    def test_fetch_sheet_data_empty_values(self, mock_build, mock_creds):
        """Test handling of empty sheet data."""
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock empty values
        mock_service.spreadsheets().values().get().execute.return_value = {
            'values': []
        }
        
        result = fetch_sheet_data()
        assert result is None

    @patch('sheets.service_account.Credentials.from_service_account_file')
    def test_fetch_sheet_data_exception(self, mock_creds):
        """Test exception handling in data fetching."""
        mock_creds.side_effect = Exception("Credentials error")
        
        result = fetch_sheet_data()
        assert result is None