def function_1(*args, **kwargs):
    gathered_args = args, kwargs
    print(gathered_args)


function_1(87, 21, 93, a=55, b=54)
function_1('sor', 'meaw', x=1, y=2, z=3)
function_1(True, False, 'soup', 'none', 'one', name='Alice', age=45)
