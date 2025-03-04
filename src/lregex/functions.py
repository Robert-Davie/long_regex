import re
from src.lregex.from_lregex import from_lregex


def full_compile(pattern):
    pattern = from_lregex(pattern)
    return re.compile(pattern)


def escape(pattern):
    return re.escape(pattern)


def findall(pattern, string):
    pattern = from_lregex(pattern)
    return re.findall(pattern, string)


def finditer(pattern, string):
    pattern = from_lregex(pattern)
    return re.finditer(pattern, string)


def fullmatch(pattern, string):
    pattern = from_lregex(pattern)
    return re.fullmatch(pattern, string)


def match(pattern, string):
    pattern = from_lregex(pattern)
    return re.match(pattern, string)


def purge():
    return re.purge()


def search(pattern, string):
    pattern = from_lregex(pattern)
    return re.search(pattern, string)


def split(pattern, string):
    pattern = from_lregex(pattern)
    return re.split(pattern, string)


def sub(pattern, repl, string, count):
    pattern = from_lregex(pattern)
    return re.sub(pattern, repl, string, count)


def subn(pattern, repl, string, count):
    pattern = from_lregex(pattern)
    return re.subn(pattern, repl, string, count=count)