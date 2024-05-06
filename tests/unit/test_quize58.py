from unittest.mock import patch, mock_open
import pytest

from quize58 import FileTextManipulator

PATH = "test.txt"


@pytest.fixture(scope='function')
def obj():
    return FileTextManipulator(PATH)


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_read_text_from_file_valid(mock_f, obj):
    result = obj.read_text_from_file()
    expected_output = None

    mock_f.assert_called_once_with(PATH, "r")
    mock_f.return_value.read.assert_called_once()

    assert result == expected_output


@patch('builtins.open', return_value='Error: File not found.', side_effect=FileNotFoundError('Error: File not found.'))
def test_read_text_from_file_invalid(mock_f, obj):
    with pytest.raises(FileNotFoundError):
        actual = obj.read_text_from_file()
        expected = 'Error: File not found.'

        assert actual == expected


@patch.object(FileTextManipulator, 'read_text_from_file', return_value='😊')
def test_get_text(mock_read_text, obj):
    actual = obj.get_text()
    expected = 'TEXT -- 😊'

    assert actual == expected
