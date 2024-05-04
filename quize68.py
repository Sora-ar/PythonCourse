def main():
    return 10/0


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, IsADirectoryError):
        print('The wrong path')
    except PermissionError:
        print("don't touch this file!")
    except UnicodeDecodeError:
        print('The system under attack!')
    except Exception as e:
        print('An unexpected error occurred: ', e)
