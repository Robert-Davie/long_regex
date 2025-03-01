from from_lregex import *
import re


def test_start():
    long = "start"
    short = "^"
    assert from_lregex(long) == short


def test_choice():
    long = "option ( %ab )"
    short = "[ab]"
    assert from_lregex(long) == short


def test_range():
    long = "range ( 1 7 )"
    short = "1-7"
    assert from_lregex(long) == short


def test_poker_hands():
    long = "start option ( %a range ( 2 9 ) %tjqk ) repeatExactly 5 end"
    short = "^[a2-9tjqk]{5}$"
    assert from_lregex(long) == short


def test_long_match_2():
    long = "anyChar min0 capture ( anyChar ) anyChar min0 group1"
    short = r".*(.).*\1"
    assert from_lregex(long) == short


def test_get_number():
    # e.g. -7, 3, 4 -10 etc
    long = "option ( %-+ ) max1 digit min1"
    short = r"[-+]?\d+"
    assert from_lregex(long) == short


def test_long_match_3():
    long = ""
    long += "option ( %-+ ) max1 "
    a = r"%0 option ( %xX ) option ( digit range ( A F ) range ( a f ) ) min1 "
    b = r"%0 option ( range ( 0 7 ) ) min0 "
    c = "digit min1 "
    long += f"capture ( {a} or {b} or {c})"
    short = r"[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)"
    assert from_lregex(long) == short


def test_non_greedy():
    long = "%1 min1 nonGreedy"
    short = "1+?"
    assert from_lregex(long) == short


def test_non_backtrack():
    long = "%1 min0 xBacktrack"
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
    long = "%B atLeast 12"
    short = "B{12,}"
    assert from_lregex(long) == short


def test_boundary():
    long = "boundary %class boundary"
    short = r"\bclass\b"
    assert from_lregex(long) == short


def test_detect_double_words():
    long = "boundary capture ( word min1 ) space min1 group1 boundary"
    short = from_lregex(long)
    assert short == r'\b(\w+)\s+\1\b'
    p = re.compile(short)
    assert p.search('Paris in the the spring').group() == 'the the'


def test_negative_lookahead():
    long = r"anyChar min0 option ( anyChar ) xLookAhead ( %bat end ) xOption ( anyChar ) min0 end"
    short = r".*[.](?!bat$)[^.]*$"
    assert from_lregex(long) == short


def test_positive_lookahead():
    long = r"lookAhead ( %G )"
    short = r"(?=G)"
    assert from_lregex(long) == short


def test_non_capture():
    long = r"xCapture ( %Hello )"
    short =r"(?:Hello)"
    assert from_lregex(long) == short


def test_named_capture():
    long = r"namedCapture ( myGroup %Apple )"
    short = r"(?P<myGroup>Apple)"
    assert from_lregex(long) == short


def test_reuse_capture():
    long = r"namedCapture ( myGroup %Apple ) reuseCapture myGroup"
    short = r"(?P<myGroup>Apple)(?P=myGroup)"
    assert from_lregex(long) == short


def test_string_start_and_end():
    long = r"stringStart stringEnd"
    short = "\\A\\Z"
    assert from_lregex(long) == short


def test_example_readme_code_1():
    example_text = "23 1 45 92 13 ABCdef"
    pattern = from_lregex(r"digit repeatExactly 2")
    assert re.findall(pattern, example_text) == ["23", "45", "92", "13"]


def test_email_example():
    long = r"word min1 %@ word min1 %. option ( %com or %co.uk )"
    short = r"\w+@\w+\.[com|co\.uk]"
    assert from_lregex(long) == short


def test_escape_backslash():
    long = "%\\"
    short = "\\"
    assert from_lregex(long) == short


def test_escaped_punctuation():
    long = r"%.^$|?*()[]{}+"
    short = r"\.\^\$\|\?\*\(\)\[\]\{\}\+"