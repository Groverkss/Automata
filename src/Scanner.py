from TokenType import TokenType
from Token import Token

import sys

from pprint import pprint


class Scanner:
    """ Scans a given regex to tokens """

    def __init__(self):
        self.keys = {
            "+": TokenType.UNION,
            "*": TokenType.KLEENE,
            "(": TokenType.LEFT_PARAN,
            ")": TokenType.RIGHT_PARAN,
        }

        self.no_concat_left = ["(", "+"]
        self.no_concat_right = [")", "+", "*", "EOF"]

    def scan(self, regex):
        """Tokenizes the regex into Token class"""

        self.regex = regex
        self.tokens = []
        self.curr_pos = 0

        while self.curr_pos != len(regex):
            curr_char = self._advance()

            # Add current token
            if curr_char in self.keys:
                self._add_token(self.keys[curr_char])
            elif curr_char.isalnum():
                self._add_token(TokenType.ALPHA, curr_char)
            else:
                self._scan_error()

            # Check if a concat token needs to be added
            if (
                self._previous() not in self.no_concat_left
                and self._peek() not in self.no_concat_right
            ):
                self._add_token(TokenType.CONCAT)

        self._add_token(TokenType.EOF)

        return self.tokens

    def _previous(self):
        """Returns previous character. Assums not at start position"""

        return self.regex[self.curr_pos - 1]

    def _peek(self):
        """Returns current character"""

        if self.curr_pos >= len(self.regex):
            return "EOF"

        return self.regex[self.curr_pos]

    def _advance(self):
        """Returns current character and moves forward"""

        ret_char = self.regex[self.curr_pos]
        self.curr_pos += 1
        return ret_char

    def _add_token(self, token_type, value=None):
        """Adds a new token to list of tokens"""

        token = Token(token_type, self.curr_pos, value)
        self.tokens.append(token)

    def _scan_error(self):
        """Reports a scan error at current position"""

        print(f"[Error]: Invalid Character at position {self.curr_pos}")
        sys.exit(1)


if __name__ == "__main__":
    scanner = Scanner()
    regex = input()

    for token in scanner.scan(regex):
        pprint(token)
