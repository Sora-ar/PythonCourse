import argparse


def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    return num1 * num2


def divide(num1, num2):
    if num2 == 0:
        return "Error: Division by zero!"
    else:
        return num1 / num2


# python calculator.py --num1 5 --num2 3 --operation add
parser = argparse.ArgumentParser(prog='Calculator', usage='quize32.py [-h] [--num1 number1 --num2 number2 --operation selected_operation]',
                                 description="Simple calculator supporting addition, subtraction, multiplication, and division.")
parser.add_argument("--num1", metavar='NUM1', type=float, help="First number", required=True)
parser.add_argument("--num2", metavar='NUM2', type=float, help="Second number", required=True)
parser.add_argument("--operation", choices=['add', 'subtract', 'multiply', 'divide'], help="Operation",
                    required=True)

args = parser.parse_args()

match args.operation:
    case 'add':
        result = add(args.num1, args.num2)
        print("Result:", result)
    case 'subtract':
        result = subtract(args.num1, args.num2)
        print("Result:", result)
    case 'multiply':
        result = multiply(args.num1, args.num2)
        print("Result:", result)
    case 'divide':
        result = divide(args.num1, args.num2)
        print("Result:", result)
