from lregex.re_to_lregex import re_to_lregex, indent


def test_digit():
    long = "digit"
    short = r"\d"
    assert re_to_lregex(short) == long


def test_x_digit():
    long = "x_digit"
    short = r"\D"
    assert re_to_lregex(short) == long


def test_two_items():
    long = "digit x_digit"
    short = r"\d\D"
    assert re_to_lregex(short) == long


def test_whitespace():
    long = "whitespace"
    short = r"\s"
    assert re_to_lregex(short) == long


def test_x_whitespace():
    long = "x_whitespace"
    short = r"\S"
    assert re_to_lregex(short) == long


def test_word():
    long = "word"
    short = r"\w"
    assert re_to_lregex(short) == long


def test_x_word():
    long = "x_word"
    short = r"\W"
    assert re_to_lregex(short) == long


def test_space():
    long = "space"
    short = ' '
    assert re_to_lregex(short) == long


def test_start():
    long = "start"
    short = '^'
    assert re_to_lregex(short) == long


def test_end():
    long = "end"
    short = '$'
    assert re_to_lregex(short) == long


def test_anychar():
    long = "any_char"
    short = '.'
    assert re_to_lregex(short) == long


def test_or():
    long = "or"
    short = "|"
    assert re_to_lregex(short) == long


def test_literal_string():
    long = "%newstring"
    short = "newstring"
    assert re_to_lregex(short) == long


def test_group_5():
    long = "group5"
    short = r"\5"
    assert re_to_lregex(short) == long


def test_string_start():
    long = "string_start"
    short = r"\A"
    assert re_to_lregex(short) == long


def test_string_end():
    long = "string_end"
    short = r"\Z"
    assert re_to_lregex(short) == long


def test_min0():
    long = "min0"
    short = r"*"
    assert re_to_lregex(short) == long


def test_max1():
    long = "max1"
    short = r"?"
    assert re_to_lregex(short) == long


def test_min1():
    long = "min1"
    short = r"+"
    assert re_to_lregex(short) == long


def test_boundary():
    long = "boundary"
    short = r"\b"
    assert re_to_lregex(short) == long


def test_x_boundary():
    long = "x_boundary"
    short = r"\B"
    assert re_to_lregex(short) == long


def test_choice():
    long = "choice ( digit )"
    short = r"[\d]"
    assert re_to_lregex(short) == long


def test_escaped_punctuation():
    long = r"%?|*+.()[]{}$^"
    short = r"\?\|\*\+\.\(\)\[\]\{\}\$\^"
    assert re_to_lregex(short) == long


def test_escape_backslash():
    long = r"%\\"
    short = r"\\"
    assert re_to_lregex(short) == long


def test_1_pound():
    long = r"%1"
    short = "1"
    assert re_to_lregex(short) == long


def test_x_greedy():
    long = r"min0 x_greedy"
    short = "*?"
    assert re_to_lregex(short) == long


def test_x_backtrack():
    long = r"min0 x_backtrack"
    short = "*+"
    assert re_to_lregex(short) == long


def test_range():
    long = "choice ( range ( 2 6 ) )"
    short = "[2-6]"
    assert re_to_lregex(short) == long


def test_repeat_exactly():
    long = "repeat_exactly 5"
    short = r"{5}"
    assert re_to_lregex(short) == long


def test_repeat_exactly_three_digit():
    long = "repeat_exactly 101"
    short = r"{101}"
    assert re_to_lregex(short) == long


def test_repeat_min():
    long = "repeat_min 7"
    short = "{7,}"
    assert re_to_lregex(short) == long


def test_repeat_min_three_digit():
    long = "repeat_min 123"
    short = "{123,}"
    assert re_to_lregex(short) == long


def test_repeat_between():
    long = "repeat_between ( 99 234 )"
    short = "{99,234}"
    assert re_to_lregex(short) == long


def test_capture():
    long = r"capture ( %x )"
    short = "(x)"
    assert re_to_lregex(short) == long


def test_x_capture():
    long = r"x_capture ( %z )"
    short = "(?:z)"
    assert re_to_lregex(short) == long


def test_look_ahead():
    long = r"look_ahead ( %a )"
    short = r"(?=a)"
    assert re_to_lregex(short) == long


def test_x_look_ahead():
    long = r"x_look_ahead ( %b )"
    short = r"(?!b)"
    assert re_to_lregex(short) == long


def test_reuse_capture():
    long = r"reuse_capture apple"
    short = r"(?P=apple)"
    assert re_to_lregex(short) == long


def test_capture_with_name():
    long = r"capture banana ( %t )"
    short = r"(?P<banana>t)"
    assert re_to_lregex(short) == long


def test_dash_non_range():
    long = r"%hello-world"
    short = r"hello-world"
    assert re_to_lregex(short) == long


def test_hat_in_choice():
    long = r"choice ( %a^ )"
    short = r"[a^]"
    assert re_to_lregex(short) == long


def test_indent():
    initial = "( apple )"
    expected = \
"""
(
    apple
)
"""
    assert indent(initial).strip() == expected.strip()


def test_double_indent():
    initial = "food ( apple ( banana ) citrus )"
    expected = \
"""
food (
    apple (
        banana
    )
    citrus
)
"""
    assert indent(initial).strip() == expected.strip()


def test_triple_indent():
    initial = "food ( apple ( ( banana ) ) citrus )"
    expected = \
"""
food (
    apple (
        (
            banana
        )
    )
    citrus
)
"""
    assert indent(initial).strip() == expected.strip()


def test_two_bracket_indent():
    initial = "( ( ) )"
    expected = \
"""
(
    (
    )
)
"""
    assert indent(initial).strip() == expected.strip()


def test_two_bracket_indent_with_word():
    initial = "( ( ) fox )"
    expected = \
"""
(
    (
    )
    fox
)
"""
    assert indent(initial).strip() == expected.strip()


def test_three_bracket_indent():
    initial = "( ( ( ) ) )"
    expected = \
"""
(
    (
        (
        )
    )
)
"""
    assert indent(initial).strip() == expected.strip()


def test_ampersand():
    long = "%&"
    short = r"\&"
    assert re_to_lregex(short) == long