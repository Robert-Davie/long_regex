from enum import Enum


class ValidWords(Enum):
    START = "start"
    END = "end"
    DIGIT = "digit"
    X_DIGIT = "x_digit"
    WHITESPACE = "whitespace"
    X_WHITESPACE = "x_whitespace"
    WORD = "word"
    X_WORD = "x_word"
    PERCENT = "%"
    STRING_START = "string_start"
    STRING_END = "string_end"
    ANY_CHAR = "any_char"
    OR = "or"
    LOOK_AHEAD = "look_ahead"
    X_LOOK_AHEAD = "x_look_ahead"
    MIN0 = "min0"
    MAX1 = "max1"
    MIN1 = "min1"
    BOUNDARY = "boundary"
    X_BOUNDARY = "x_boundary"
    REPEAT = "repeat"
    REPEAT_EXACTLY = "repeat_exactly"
    AT_LEAST = "at_least"
    RANGE = "range"
    CHOICE = "choice"
    X_CHOICE = "x_choice"
    CAPTURE = "capture"
    X_CAPTURE = "x_capture"
    NAMED_CAPTURE = "named_capture"
    REUSE_CAPTURE = "reuse_capture"
    X_GREEDY = "x_greedy"
    X_BACKTRACK = "x_backtrack"
