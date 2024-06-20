import requests


# 1.
def add_numbers(a, b):
    return a + b


# 2.
def is_even(number):
    return True if number % 2 == 0 else False


# 3.
def fetch_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


# 4.
def process_mock_object(obj):
    return obj.value * 2 if obj.value > 0 else None


# 5.
def run_data_pipeline(data_processor):
    prepared_data = data_processor.process_data().analyze_data()
    prepared_data.save_result()


# 6.
def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    except TypeError:
        print("Error: Unsupported operand type(s) for division!")
    else:
        return result


# 7.
def check_even_odd(numbers, url):
    result = []
    for number in numbers:
        response = requests.get(f'{url} / {number}').json()['results'][0]['value']
        if response % 2 == 0:
            result.append("Even")
        else:
            result.append("Odd")
    return result


# 8.
class DataProcessor:
    @staticmethod
    def process_data(data):
        return [x * 2 for x in data]

    def analyze_data(self, data):
        processed_data = self.process_data(data)
        return sum(processed_data)
