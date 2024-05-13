class MyClass:
    def __init__(self):
        self.public_attribute = "initial_value"
        self._private_attribute = 10

    def public_method(self):
        print("Public method.")
        self._protected_method()

    @staticmethod
    def _protected_method():
        print("Protected method.")


obj = MyClass()
if hasattr(obj, 'public_attribute'):
    print("Instance has 'public_attribute'.")
    setattr(obj, 'public_attribute', "changed_value")

    changed_value = getattr(obj, 'public_attribute')
    print("Changed value:", changed_value)
else:
    print("Instance doesn't have 'public_attribute'.")
