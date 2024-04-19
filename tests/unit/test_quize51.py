from unittest.mock import patch
from quize51 import calculate


@patch('quize51.dangerous_function', return_value=0)
def test_calculate(mock_af):
    inp_a = 3
    actual = calculate(inp_a)
    expected = 0
    assert actual == expected
