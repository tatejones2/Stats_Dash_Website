import pytest
from unittest.mock import patch, MagicMock
from app import generate_player_summary

def test_generate_player_summary_success():
    player_stats = {'Player': 'John Doe', 'K%': 32, 'ERA': 2.5}
    api_key = 'sk-test'
    model_name = 'gpt-4'
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='John Doe is pitching well.'))]
    with patch('openai.ChatCompletion.create', return_value=mock_response) as mock_create:
        summary = generate_player_summary(player_stats, api_key, model_name)
        assert 'John Doe is pitching well.' in summary
        mock_create.assert_called_once()

def test_generate_player_summary_api_error():
    player_stats = {'Player': 'Jane Smith', 'K%': 28, 'ERA': 3.1}
    api_key = 'sk-test'
    model_name = 'gpt-4'
    with patch('openai.ChatCompletion.create', side_effect=Exception('API error')):
        summary = generate_player_summary(player_stats, api_key, model_name)
        assert 'Error generating summary' in summary
