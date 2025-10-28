import pytest
from unittest.mock import patch
import pandas as pd
from app import show_interactive_charts

def test_show_interactive_charts_runs():
    df = pd.DataFrame({
        'Column_B': ['John Doe'],
        'K%': [32],
        'ERA': [2.5]
    })
    # Mock st.columns to return 3 mock columns
    from unittest.mock import MagicMock
    with patch('streamlit.subheader'), \
         patch('streamlit.markdown'), \
         patch('streamlit.columns', return_value=[MagicMock(), MagicMock(), MagicMock()]), \
         patch('streamlit.selectbox'), \
         patch('streamlit.button', return_value=False), \
         patch('streamlit.plotly_chart'):
        show_interactive_charts(df)
