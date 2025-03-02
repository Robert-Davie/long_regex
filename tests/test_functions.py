import lregex
import re


def test_full_compile():
    assert lregex.full_compile("digit") == re.compile("\\d")


def test_escape():
    assert lregex.escape(r"%[]?") == r"%\[\]\?"


def test_findall():
    assert lregex.findall(r"%abc word min0", r"abcDEF abc ab ZabcZ") == ["abcDEF", "abc", "abcZ"]


def test_finditer():
    pattern = "digit"
    string = "123"
    matches = lregex.finditer(pattern, string)
    match_list = [match.group() for match in matches]
    assert match_list == ["1", "2", "3"]


def test_fullmatch():
    pattern = "%ab or digit"
    assert lregex.fullmatch(pattern, "3").group() == "3"


def test_not_fullmatch():
    pattern = "%abc"
    assert lregex.fullmatch(pattern, "ZabcZ") == None


def test_match():
    assert lregex.match("%abc", "abcZ").group() == re.match("abc", "abcZ").group()
    assert lregex.match("%abc", "abcZ").group() == "abc"


def test_search():
    assert lregex.search("%a any_char %c", "eabcd").group() == "abc"


def test_split():
    assert lregex.split("digit", "ab1cd") == ["ab", "cd"]


def test_sub():
    assert lregex.sub("%ab", "cd", "eabababf", 2) == "ecdcdabf"


def test_sub():
    assert lregex.subn("%ab", "cd", "eabababf", 0) == ("ecdcdcdf", 3)