class MyClass:
    def __init__(self):
        self._protected_field = "Protected field of MyClass"

    def _protected_method(self):
        print("Protected method of MyClass:", self._protected_field)


class ChildClass(MyClass):
    def public_method(self):
        self._protected_method()


child_obj = ChildClass()
child_obj.public_method()
