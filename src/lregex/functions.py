import re
from .lregex_to_regex import lregex_to_regex


def full_compile(pattern):
    pattern = lregex_to_regex(pattern)
    return re.compile(pattern)


def escape(pattern):
    return re.escape(pattern)


def findall(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.findall(pattern, string)


def finditer(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.finditer(pattern, string)


def fullmatch(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.fullmatch(pattern, string)


def match(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.match(pattern, string)


def search(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.search(pattern, string)


def split(pattern, string):
    pattern = lregex_to_regex(pattern)
    return re.split(pattern, string)


def sub(pattern, repl, string, count):
    pattern = lregex_to_regex(pattern)
    return re.sub(pattern, repl, string, count=count)


def subn(pattern, repl, string, count):
    pattern = lregex_to_regex(pattern)
    return re.subn(pattern, repl, string, count=count)
