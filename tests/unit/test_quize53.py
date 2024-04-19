from unittest.mock import patch, call
from quize53 import calculate


@patch('quize53.dangerous_function')
def test_calculate(mock_af):
    inp = [1, 2, 3]
    calculate(inp)
    expected = [call([1, 2, 3]),
                call().mtd_1(),
                call().mtd_2()
                ]
    assert mock_af.mock_calls == expected
