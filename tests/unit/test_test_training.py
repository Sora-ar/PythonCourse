from unittest.mock import patch, MagicMock
import pytest
from test_training import *


def test_add_numbers():
    pram_1 = 1
    parm_2 = 2
    actual = add_numbers(pram_1, parm_2)
    expected = 3
    assert actual == expected


@pytest.mark.parametrize('param, expected', [(1, False), (2, True)])
def test_is_even(param, expected):
    actual = is_even(param)
    assert actual == expected


@pytest.mark.parametrize('mock_response_status, expected', [(429, None),
                                                            (200, [{1: '1', 2: '2', 3: '3'}])])
@patch('test_training.requests.get')
def test_fetch_data(mock_f, mock_response_status, expected):
    mock_response = MagicMock()
    mock_response.status_code = mock_response_status
    mock_response.json.return_value = [{1: '1', 2: '2', 3: '3'}]
    mock_f.return_value = mock_response
    actual = fetch_data('http')
    assert actual == expected


# @pytest.mark.parametrize('value, expected', [(1, 2), (-1, None)])
def test_process_mock_object():
    mock_inp = MagicMock()
    mock_inp.value = 1
    actual = process_mock_object(mock_inp)
    expected = 2 #dopisat proverky na None

    assert actual == expected


def test_run_data_pipeline():
    mock_f = MagicMock()
    processed_data_mock = mock_f.process_data.return_value.analyze_data.return_value
    processed_data_mock.save_result.return_value = ['mock_1', 'mock_2', 'mock_3']
    run_data_pipeline(mock_f)

    mock_f.process_data.assert_called_once()
    processed_data_mock.save_result.assert_called_once()


def