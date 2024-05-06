class FileTextManipulator:
    def __init__(self, filename):
        self.filename = filename
        self.text = None

    def read_text_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            return "Error: File not found."

    def get_text(self):
        text = self.read_text_from_file()
        return f"TEXT -- {text}"
