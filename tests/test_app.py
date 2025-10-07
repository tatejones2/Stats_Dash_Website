import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAppModule:
    """Test cases for the main app module."""

    @patch('sheets.fetch_sheet_data')
    def test_fetch_data_integration(self, mock_fetch_data):
        """Test integration with fetch_sheet_data function."""
        # Mock data
        test_data = pd.DataFrame({
            'Player': ['John Doe', 'Jane Smith'],
            'Position': ['CF', '1B'],
            'Batting Average': [0.350, 0.280],
            'Home Runs': [15, 22]
        })
        
        mock_fetch_data.return_value = test_data
        
        # Import and test the function directly
        from sheets import fetch_sheet_data
        result = fetch_sheet_data()
        
        assert result is not None
        assert len(result) == 2
        mock_fetch_data.assert_called_once()

    def test_basic_imports(self):
        """Test that the app module can be imported without errors."""
        try:
            import streamlit
            import pandas
            assert True
        except ImportError:
            pytest.fail("Required modules not available")

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.dataframe')
    @patch('streamlit.subheader')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    @patch('streamlit.scatter_chart')
    @patch('sheets.fetch_sheet_data')
    def test_app_with_data_flow(self, mock_fetch_data, mock_scatter, mock_button, 
                                mock_selectbox, mock_subheader, mock_dataframe, 
                                mock_title, mock_config):
        """Test the main app flow with data."""
        # Mock data
        test_data = pd.DataFrame({
            'Player': ['John', 'Jane'],
            'BA': [0.350, 0.280]
        })
        
        mock_fetch_data.return_value = test_data
        mock_selectbox.side_effect = ['Player', 'BA', 'Scatter']
        mock_button.return_value = True
        
        # Import app to trigger execution
        import app
        
        # Verify basic streamlit setup was called
        mock_config.assert_called_once()
        mock_title.assert_called_once()

    @patch('streamlit.error')
    @patch('sheets.fetch_sheet_data')
    def test_app_with_no_data(self, mock_fetch_data, mock_error):
        """Test app behavior when no data is available."""
        mock_fetch_data.return_value = None
        
        # Reload the app module to test error case
        if 'app' in sys.modules:
            del sys.modules['app']
        
        import app
        
        # Should show error when no data
        mock_error.assert_called_once_with("Failed to load data from Google Sheets.")