import pytest
from unittest.mock import patch
import pandas as pd
from app import show_player_page

def test_show_player_page_runs():
    df = pd.DataFrame({
        'Column_B': ['John Doe'],
        'K%': [32],
        'ERA': [2.5]
    })
    player_name_col = 'Column_B'
    player_name = 'John Doe'
    api_key = 'sk-test'
    model_name = 'gpt-4'
    with patch('streamlit.header'), \
         patch('streamlit.subheader'), \
         patch('streamlit.dataframe'), \
         patch('streamlit.spinner'), \
         patch('streamlit.write'), \
         patch('app.generate_player_summary', return_value='AI summary here.'):
        show_player_page(df, player_name_col, player_name, api_key, model_name)
