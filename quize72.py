from abc import ABC, abstractmethod


class MyClass(ABC):
    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass


class ChildClass(MyClass):
    def method1(self):
        print("Method 1")

    def method2(self):
        print("Method 2")


child_instance = ChildClass()
child_instance.method1()
child_instance.method2()
