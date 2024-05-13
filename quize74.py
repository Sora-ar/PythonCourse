class CalculationUtils:
    @staticmethod
    def sum(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b


result_sum = CalculationUtils.sum(55, 33)
print("Sum:", result_sum)

result_sub = CalculationUtils.sub(55, 33)
print("Subtraction:", result_sub)
