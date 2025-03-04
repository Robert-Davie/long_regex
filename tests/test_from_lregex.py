from src.lregex.from_lregex import from_lregex, LregexSyntaxException
import re
import pytest


def test_start():
    long = "start"
    short = "^"
    assert from_lregex(long) == short


def test_choice():
    long = "choice ( %ab )"
    short = "[ab]"
    assert from_lregex(long) == short


def test_range():
    long = "range ( 1 7 )"
    short = "1-7"
    assert from_lregex(long) == short


def test_poker_hands():
    long = "start choice ( %a range ( 2 9 ) %tjqk ) repeat_exactly 5 end"
    short = "^[a2-9tjqk]{5}$"
    assert from_lregex(long) == short


def test_long_match_2():
    long = "any_char min0 capture ( any_char ) any_char min0 group1"
    short = r".*(.).*\1"
    assert from_lregex(long) == short


def test_get_number():
    # e.g. -7, 3, 4 -10 etc
    long = "choice ( %-+ ) max1 digit min1"
    short = r"[-\+]?\d+"
    assert from_lregex(long) == short


def test_long_match_3():
    long = ""
    long += "choice ( %-+ ) max1 "
    a = r"%0 choice ( %xX ) choice ( digit range ( A F ) range ( a f ) ) min1 "
    b = r"%0 choice ( range ( 0 7 ) ) min0 "
    c = "digit min1 "
    long += f"capture ( {a} or {b} or {c})"
    short = r"[-\+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)"
    assert from_lregex(long) == short


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
    assert from_lregex(long) == short



def test_x_greedy():
    long = "%1 min1 x_greedy"
    short = "1+?"
    assert from_lregex(long) == short


def test_x_backtrack():
    long = "%1 min0 x_backtrack"
    short = "1*+"
    assert from_lregex(long) == short


def test_escaped_percent():
    long = "%%"
    short = "%"
    assert from_lregex(long) == short


def test_repeat_between():
    long = "%A repeat ( 2 5 )"
    short = "A{2,5}"
    assert from_lregex(long) == short


def test_at_least():
    long = "%B at_least 12"
    short = "B{12,}"
    assert from_lregex(long) == short


def test_boundary():
    long = "boundary %class boundary"
    short = r"\bclass\b"
    assert from_lregex(long) == short


def test_detect_double_words():
    long = "boundary capture ( word min1 ) whitespace min1 group1 boundary"
    short = from_lregex(long)
    assert short == r'\b(\w+)\s+\1\b'
    p = re.compile(short)
    assert p.search('Paris in the the spring').group() == 'the the'


def test_negative_lookahead():
    long = r"any_char min0 choice ( any_char ) x_look_ahead ( %bat end ) x_choice ( any_char ) min0 end"
    short = r".*[.](?!bat$)[^.]*$"
    assert from_lregex(long) == short


def test_positive_lookahead():
    long = r"look_ahead ( %G )"
    short = r"(?=G)"
    assert from_lregex(long) == short


def test_non_capture():
    long = r"x_capture ( %Hello )"
    short =r"(?:Hello)"
    assert from_lregex(long) == short


def test_named_capture():
    long = r"named_capture ( my_group %Apple )"
    short = r"(?P<my_group>Apple)"
    assert from_lregex(long) == short


def test_reuse_capture():
    long = r"named_capture ( my_group %Apple ) reuse_capture my_group"
    short = r"(?P<my_group>Apple)(?P=my_group)"
    assert from_lregex(long) == short


def test_string_start_and_end():
    long = r"string_start string_end"
    short = "\\A\\Z"
    assert from_lregex(long) == short


def test_example_readme_code_1():
    example_text = "23 1 45 92 13 ABCdef"
    pattern = from_lregex(r"digit repeat_exactly 2")
    assert re.findall(pattern, example_text) == ["23", "45", "92", "13"]


def test_email_example():
    long = r"word min1 %@ word min1 %. choice ( %com or %co.uk )"
    short = r"\w+@\w+\.[com|co\.uk]"
    assert from_lregex(long) == short


def test_escape_backslash():
    long = "%\\"
    short = "\\"
    assert from_lregex(long) == short


def test_escaped_punctuation():
    long = r"%.^$|?*()[]{}+"
    short = r"\.\^\$\|\?\*\(\)\[\]\{\}\+"
    assert from_lregex(long) == short


def test_invalid_syntax():
    # fails as %abc is valid but not abc on its own
    with pytest.raises(LregexSyntaxException) as e:
        from_lregex("abc")
    assert str(e.value) == "'abc' is not a valid word in lregex"


def test_pattern_extra_space():
    assert from_lregex("%a  %b") == "ab"

def test_pattern_with_internal_newline():
    assert from_lregex("""
%a

%b
""") == "ab"
    
def test_x_boundary():
    assert from_lregex("x_boundary") == r"\B"


def test_x_digit():
    assert from_lregex("x_digit") == r"\D"


def test_x_whitespace():
    assert from_lregex("x_whitespace") == r"\S"


def test_x_word():
    assert from_lregex("x_word") == r"\W"