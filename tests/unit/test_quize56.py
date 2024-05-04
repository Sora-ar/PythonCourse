from unittest.mock import patch, mock_open
import pytest

from quize56 import read


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_read_valid(mock_f):
    path = "test.txt"
    result = read(path)
    expected_output = "data"

    mock_f.assert_called_once_with(path, "r")
    mock_f.return_value.read.assert_called_once()

    assert result == expected_output


@patch('builtins.open', side_effect=FileNotFoundError)
def test_read_invalid(mock_f):
    path = "nonexistent_file.txt"

    with pytest.raises(FileNotFoundError):
        read(path)
