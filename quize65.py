class MyClass:
    def __init__(self):
        self._private_attribute = 10

    def public_method(self):
        print("Public method.")
        self._protected_method()

    @staticmethod
    def _protected_method():
        print("Protected method.")


obj = MyClass()
obj.public_method()
