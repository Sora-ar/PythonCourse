class MyClass:
    def __init__(self):
        self.__private_attribute = 0

    def public_method(self):
        print("Public method.")
        self._protected_method()

    @staticmethod
    def _protected_method():
        print("Protected method.")

    @property
    def private_attribute(self):
        return self.__private_attribute

    @private_attribute.setter
    def private_attribute(self, value):
        self.__private_attribute = value


obj = MyClass()

print(obj.private_attribute)
obj.private_attribute = 123456
print(obj.private_attribute)
