from unittest.mock import patch
from quize50 import calculate


@patch('quize50.dangerous_function')
def test_calculate(mock_af):
    inp_a = 1
    inp_b = 2
    actual = calculate(inp_a, inp_b)
    expected = 6
    assert actual == expected
