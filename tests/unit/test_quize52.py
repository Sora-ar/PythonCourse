from unittest.mock import patch
from quize52 import calculate


@patch('quize52.dangerous_function',
       side_effect=[True, True, False, False, False])
def test_calculate(mock_af):
    inp_a = [1, 2, 3, 4, 5]
    actual = calculate(inp_a)
    expected = 0
    assert actual == expected
