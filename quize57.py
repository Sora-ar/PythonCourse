import random


class FileTextManipulator:
    def __init__(self, filename):
        self.filename = filename
        self.text = None

    def read_text_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")

    def modify_text(self):
        modification_type = random.choice(["uppercase", "reverse", "add_emoji"])

        if modification_type == "uppercase":
            self.text = self.text.upper()
        elif modification_type == "reverse":
            self.text = self.text[::-1]
        elif modification_type == "add_emoji":
            emojis = ["😊", "🚀", "💡", "🎉"]
            random_emoji = random.choice(emojis)
            self.text += f" {random_emoji}"''

        return self.text

    def get_text(self):
        self.read_text_from_file()
        text = self.modify_text()
        return f"TEXT -- {text}"
