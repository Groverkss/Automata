import sys

from TokenType import TokenType
from Token import Token
import Expr
from Scanner import Scanner


class Parser:
    """Parses a given string into a Abstract Syntax Tree"""

    def __init__(self):
        pass

    def parse(self, tokens):
        self.curr_pos = 0
        self.tokens = tokens
        return self._expression()

    def _expression(self):
        return self._union()

    def _union(self):
        left = self._concat()

        while self._match(TokenType.UNION):
            right = self._concat()
            left = Expr.Union(left, right)

        return left

    def _concat(self):
        left = self._kleene()

        while self._match(TokenType.CONCAT):
            right = self._kleene()
            left = Expr.Concat(left, right)

        return left

    def _kleene(self):
        left = self._literal()

        while self._match(TokenType.KLEENE):
            left = Expr.Kleene(left)

        return left

    def _literal(self):
        if self._match(TokenType.ALPHA):
            return Expr.Literal(self._previous().value)

        if self._match(TokenType.LEFT_PARAN):
            expr = self._expression()
            if self._match(TokenType.RIGHT_PARAN):
                return Expr.Grouping(expr)
            else:
                self.__error("Closing Paranthesis not found")

        self.__error("Unexpected Token")

    def _advance(self):
        ret_token = self.tokens[self.curr_pos]
        self.curr_pos += 1
        return ret_token

    def _previous(self):
        return self.tokens[self.curr_pos - 1]

    def _peek(self):
        return self.tokens[self.curr_pos]

    def _match(self, *args):
        for token in args:
            if self._peek().token_type == token:
                self.curr_pos += 1
                return True

        return False

    def __error(self, message):
        print("[Error]: " + message)
        sys.exit(1)


if __name__ == "__main__":
    scanner = Scanner()
    regex = input()

    tokens = scanner.scan(regex)

    parser = Parser()
    print(parser.parse(tokens))
