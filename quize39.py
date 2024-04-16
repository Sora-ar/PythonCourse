def process_strings(str1, str2, str3):
    """
    Process three different strings using various string methods and return a list of modified strings.

    :param str1: First string.
    :param str2: Second string.
    :param str3: Third string.
    :return: List containing modified strings.
    """

    def modify_string(string):
        """
        Apply various string methods to a given string and return the modified string.

        :param string: The input string to be modified.
        :return: The modified string.
        """
        modified_string = string.lower()
        modified_string = modified_string.strip()
        modified_string = modified_string.center(11, '-')
        modified_string = modified_string.split()
        return modified_string

    modified_str1 = modify_string(str1)
    modified_str2 = modify_string(str2)
    modified_str3 = modify_string(str3)

    return [modified_str1, modified_str2, modified_str3]


str_list = process_strings("  Cat   ", "Say", "  Meow  ")
print(str_list)
