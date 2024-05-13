class SimpleContextManager:
    def __enter__(self):
        print("Before context block")

    def __exit__(self, exc_type, exc_value, traceback):
        print("After context block")


with SimpleContextManager():
    print("Inside context block")
