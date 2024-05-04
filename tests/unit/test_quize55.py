from unittest.mock import patch
from quize55 import calculate


@patch('quize55.dangerous_function')
def test_calculate(mock_f):
    mock_f.return_value.mtd_1.return_value.mtd_2.return_value = 3
    actual = calculate()
    expected = 24

    assert actual == expected
