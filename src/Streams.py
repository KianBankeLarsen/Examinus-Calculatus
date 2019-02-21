import sys


class InputStream:
    def __init__(self, text: str):
        self.text = text

        self.pos = 0
        self.row = 1
        self.col = 1

        self.current_char = self.text[0]

    def advance(self):
        # Tries to advance to the next character. If EOF is reached current_char will be None.
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
            return
        else:
            self.current_char = self.text[self.pos]
            self.col += 1

            if self.current_char == "\n":
                self.col = 1
                self.row += 1

    def peek(self):
        # Tries to peek at the next character without advancing in position. Returns None if EOF is reached.

        peek_pos = self.pos + 1

        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]


class FileStream(InputStream):
    def __init__(self, path: str):
        file_content = self.load_file(path)
        super().__init__(file_content)

    @staticmethod
    def load_file(path: str) -> str:
        try:
            with open(path) as file:
                result = file.read()

            return result
        except IOError:
            print("Unable to read file: '{}'".format(path))
            sys.exit()
