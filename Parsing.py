import re

class Parsing:

    raw_content = ""
    puzzle = []
    error_message = ""

    def get_puzzle_from_input(self):
        """Get the puzzle from user input on stdin"""
        print("""Please enter your puzzle following the right format
    Exemple:

        # this is a comment
        3
        1 2 3
        4 5 6
        7 8 0
        """)
        content = []
        while True:
            try:
                line = input()
                if line == 'EOF' or line == 'end':
                    break
                content.append(line)
            except EOFError:
                break
        if len(content) == 0:
            return None, "empty file"
        return content, None

    def get_puzzle_from_file(self, filename):
        """Read a file to get the puzzle"""
        try:
            file = open(filename, "r")
            content = []
            for line in file.readlines():
                content.append(line.strip())
            file.close()
            if len(content) == 0:
                return None, "empty file"
            return content, None
        except (FileNotFoundError):
            err = "file not found: %s" % filename
        except (PermissionError):
            err = "permission denied: %s" % filename
        except:
            err = "can't read the file: %s" % filename
        return None, err

    def set_raw_puzzle(self, filename_arg):
        """Set the raw_content attribute with the puzzle come from user input or file"""
        if filename_arg:
            self.raw_content, err = self.get_puzzle_from_file(filename_arg)
        else:
            self.raw_content, err = self.get_puzzle_from_input()
        if err:
            return err
        return None

    def validation_puzzle(self):
        """Check if the self.puzzle list is valid for the parsing"""
        if len(self.puzzle[0]) != 1:
            return "the size should be specified first"
        size = self.puzzle[0][0]
        if size != len(self.puzzle[1:]):
            return "bad size"
        dict_validity = {i:False for i in range(size * size)}
        for line in self.puzzle[1:]:
            if len(line) != size:
                return "bad size"
            for col in line:
                if col in dict_validity:
                    if dict_validity[col] == True:
                        return "duplicate number: %d" % col
                    dict_validity[col] = True
                else:
                    return "bad number: %d" % col
        return None

    def parse(self, filename):
        """
            Parse the n-puzzle file format and checking errors
            Returns:
                - 2 dimensions list with the final puzzle
                - an error message
        """
        err = self.set_raw_puzzle(filename)
        if err:
            return None, "parsing error: %s" % err
        rx_dict = {
            'nb_line': re.compile(r'^((\s*\d+\s*)+)(\s+#(\s|\w)*)*$'),
            'comment': re.compile(r'^\s*#(\s|\w)*')
        }
        nb_line = 0
        for line in self.raw_content:
            nb_line += 1
            match = None
            for key, rx in rx_dict.items():
                match = rx.search(line)
                if match:
                    if key == 'nb_line':
                        line_list = []
                        for word in match.group().split():
                            if word.isdigit():
                                line_list.append(int(word))
                        self.puzzle.append(line_list)
                    break

            if match == None:
                return None, "parsing error: format error on line %d: %s" % (nb_line, line)
        err = self.validation_puzzle()
        if err:
            return None, "validation error: %s" % err
        self.puzzle = self.puzzle[1:]
        return self.puzzle, None
