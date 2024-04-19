from quize48 import add_numbers


def test_add_numbers():
    input_param_a = 1
    input_param_b = 2
    actual = add_numbers(input_param_a, input_param_b)
    expected = 3
    assert actual == expected
