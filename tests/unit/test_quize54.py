from unittest.mock import MagicMock
from quize54 import calculate


def test_calculate():
    mock_inp = MagicMock()
    mock_inp.mtd_1.return_value = 1
    mock_inp.field_1 = 1

    actual = calculate(mock_inp)
    expected = 4
    assert actual == expected
