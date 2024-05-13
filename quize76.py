class CustomNumber:
    def __init__(self, number):
        self.number = number

    def __float__(self):
        return float(self.number)

    def __int__(self):
        return int(self.number)


custom_num = CustomNumber(10.5)

int_value = int(custom_num)
print("Integer value:", int_value)
