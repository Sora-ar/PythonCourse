import pytest
from quize49 import calculate


@pytest.mark.parametrize('inp_a, inp_b, action, expected', [(1, 2, '+', 3),
                                                            (2, 1, '-', 1)])
def test_calculate(inp_a, inp_b, action, expected):
    actual = calculate(inp_a, inp_b, action)
    assert actual == expected
