from lregex.lregex_to_regex import lregex_to_regex, LregexSyntaxException
import re
import pytest


def test_start():
    long = "start"
    short = "^"
    assert lregex_to_regex(long) == short


def test_choice():
    long = "choice ( %ab )"
    short = "[ab]"
    assert lregex_to_regex(long) == short


def test_range():
    long = "choice ( range ( 1 7 ) )"
    short = "[1-7]"
    assert lregex_to_regex(long) == short


def test_poker_hands():
    long = "start choice ( %a range ( 2 9 ) %tjqk ) repeat_exactly 5 end"
    short = "^[a2-9tjqk]{5}$"
    assert lregex_to_regex(long) == short


def test_long_match_2():
    long = "any_char min0 capture ( any_char ) any_char min0 group1"
    short = r".*(.).*\1"
    assert lregex_to_regex(long) == short


def test_get_number():
    # e.g. -7, 3, 4 -10 etc
    long = "choice ( %-+ ) max1 digit min1"
    short = r"[-\+]?\d+"
    assert lregex_to_regex(long) == short


def test_long_match_3():
    long = ""
    long += "choice ( %-+ ) max1 "
    a = r"%0 choice ( %xX ) choice ( digit range ( A F ) range ( a f ) ) min1 "
    b = r"%0 choice ( range ( 0 7 ) ) min0 "
    c = "digit min1 "
    long += f"capture ( {a} or {b} or {c})"
    short = r"[-\+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)"
    assert lregex_to_regex(long) == short


def test_long_match_pretty_format():
    long = r"""
        choice ( %-+ ) max1
        capture (
                %0 
                choice ( %xX ) 
                choice ( 
                    digit 
                    range ( A F ) 
                    range ( a f ) 
                ) min1 
            or 
                %0 
                choice ( 
                    range ( 0 7 ) 
                ) min0 
            or 
                digit min1
        )
"""

    short = r"[-\+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)"
    assert lregex_to_regex(long) == short


def test_x_greedy():
    long = "%1 min1 x_greedy"
    short = "1+?"
    assert lregex_to_regex(long) == short


def test_x_backtrack():
    long = "%1 min0 x_backtrack"
    short = "1*+"
    assert lregex_to_regex(long) == short


def test_escaped_percent():
    long = "%%"
    short = "%"
    assert lregex_to_regex(long) == short


def test_repeat_between():
    long = "%A repeat ( 2 5 )"
    short = "A{2,5}"
    assert lregex_to_regex(long) == short


def test_at_least():
    long = "%B at_least 12"
    short = "B{12,}"
    assert lregex_to_regex(long) == short


def test_boundary():
    long = "boundary %class boundary"
    short = r"\bclass\b"
    assert lregex_to_regex(long) == short


def test_detect_double_words():
    long = "boundary capture ( word min1 ) whitespace min1 group1 boundary"
    short = lregex_to_regex(long)
    assert short == r"\b(\w+)\s+\1\b"
    p = re.compile(short)
    assert p.search("Paris in the the spring").group() == "the the"


def test_negative_lookahead():
    long = r"any_char min0 choice ( any_char ) x_look_ahead ( %bat end ) x_choice ( any_char ) min0 end"
    short = r".*[.](?!bat$)[^.]*$"
    assert lregex_to_regex(long) == short


def test_positive_lookahead():
    long = r"look_ahead ( %G )"
    short = r"(?=G)"
    assert lregex_to_regex(long) == short


def test_non_capture():
    long = r"x_capture ( %Hello )"
    short = r"(?:Hello)"
    assert lregex_to_regex(long) == short


def test_named_capture():
    long = r"named_capture ( my_group %Apple )"
    short = r"(?P<my_group>Apple)"
    assert lregex_to_regex(long) == short


def test_reuse_capture():
    long = r"named_capture ( my_group %Apple ) reuse_capture my_group"
    short = r"(?P<my_group>Apple)(?P=my_group)"
    assert lregex_to_regex(long) == short


def test_string_start_and_end():
    long = r"string_start string_end"
    short = "\\A\\Z"
    assert lregex_to_regex(long) == short


def test_example_readme_code_1():
    example_text = "23 1 45 92 13 ABCdef"
    pattern = lregex_to_regex(r"digit repeat_exactly 2")
    assert re.findall(pattern, example_text) == ["23", "45", "92", "13"]


def test_email_example():
    long = r"word min1 %@ word min1 %. choice ( %com or %co.uk )"
    short = r"\w+@\w+\.[com|co\.uk]"
    assert lregex_to_regex(long) == short


def test_escape_backslash():
    long = "%\\"
    short = "\\"
    assert lregex_to_regex(long) == short


def test_escaped_punctuation():
    long = r"%.^$|?*()[]{}+"
    short = r"\.\^\$\|\?\*\(\)\[\]\{\}\+"
    assert lregex_to_regex(long) == short


def test_invalid_syntax():
    # fails as %abc is valid but not abc on its own
    with pytest.raises(LregexSyntaxException) as e:
        lregex_to_regex("abc")
    assert str(e.value) == "'abc' is not a valid word in lregex"


def test_pattern_extra_space():
    assert lregex_to_regex("%a  %b") == "ab"


def test_pattern_with_internal_newline():
    string = """
             %a

             %b
             """
    assert (
        lregex_to_regex(string)
        == "ab"
    )


def test_x_boundary():
    assert lregex_to_regex("x_boundary") == r"\B"


def test_x_digit():
    assert lregex_to_regex("x_digit") == r"\D"


def test_x_whitespace():
    assert lregex_to_regex("x_whitespace") == r"\S"


def test_x_word():
    assert lregex_to_regex("x_word") == r"\W"


def test_space():
    assert lregex_to_regex("space") == r" "


def test_two_words():
    assert lregex_to_regex("%two space %words") == r"two words"


def test_literal():
    assert lregex_to_regex("literal ( two words )") == r"two words"


def test_literal_three_words():
    assert lregex_to_regex("literal ( three words given )") == r"three words given"


def test_literal_with_percent_and_hyphen():
    assert lregex_to_regex(r"literal ( 100% complex-literal )") == r"100% complex-literal"


def test_range_not_inside_choice_invalid():
    with pytest.raises(LregexSyntaxException) as e:
        lregex_to_regex(r"range ( a z )")
    assert str(e.value) == "range may only be used inside choice or x_choice"