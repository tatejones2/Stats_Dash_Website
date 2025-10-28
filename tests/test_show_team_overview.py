import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from app import show_team_overview

def test_show_team_overview_runs():
    # Minimal DataFrame for testing
    df = pd.DataFrame({
        'Column_B': ['John Doe'],
        'K%': [32],
        'ERA': [2.5]
    })
    # Mock st.columns to return 4 mock columns
    with patch('streamlit.columns', return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()]), \
         patch('streamlit.markdown'), \
         patch('streamlit.metric'), \
         patch('streamlit.subheader'), \
         patch('streamlit.dataframe'):
        show_team_overview(df)
