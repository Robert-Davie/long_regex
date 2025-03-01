# LRegex (Long Regex)

An alternative to regex which avoids the cryptic strings. The module provides a function to convert LRegex into Standard Python Regex.

e.g. to find a two digit number in LRegex you could write:

```
digit repeatExactly 2
```

and then translate into normal regex using the ```from_lregex``` function.

```
example_text = "23 1 45 92 13 ABCdef"

pattern = from_lregex(r"digit repeatExactly 2")
re.findall(pattern, example_text)
```
returns
```["23", "45", "92", "13"]```