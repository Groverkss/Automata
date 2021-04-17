from enum import Enum

TOKENS = [
    "UNION",
    "CONCAT",
    "KLEENE",
    "LEFT_PARAN",
    "RIGHT_PARAN",
    "ALPHA",
    "EPSILON",
    "EOF",
]

TokenType = Enum("TokenType", " ".join(TOKENS))
