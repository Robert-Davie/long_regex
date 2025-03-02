# lregex (Long Regex)

An alternative to regex which avoids the cryptic strings. lregex provides a wrapper around the regex (re) module, but uses an alternative syntax. 

for example, the lregex syntax to find a two digit number is:

```
digit repeat_exactly 2
```

so to find all matches on a string you can use the findall function: 
```
import lregex

lregex.findall("digit repeat_exactly 2", "23 1 45 92 13 ABCdef")
```
returns
```["23", "45", "92", "13"]```

a full list of all possible commands is given in the MANUAL.md