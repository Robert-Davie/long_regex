# possible operations

| Long Regex | Normal Regex | Explanation
| --- | --- | --- |
| start | ^ | Start of line |
| end | $ | End of line |
| digit | \d | digit |
| xDigit | \D | not a digit |
| space | \s | a space character |
| xSpace | \S | not a space character |
| word | \w | a word character |
| xWord | \W | not a word character |
| %ABCabc | ABCabc | use % sign to write string of characters |
| group2 | \2 | reference nth group from 1 to 9, here n=2 |
| stringStart | \A | Start of line (differnt to ^ in multiline mode) |
| stringEnd | \Z | End of line (different to $ in multiline mode) |
| anyChar | . | any character apart from newline |
| or | \| | or |
| lookAhead ( ... ) | (?=...) | lookahead |
| xLookAhead (...) | (?!...) | opposite of lookahead |
| ... min0 | ...* | appear any number of times including 0 |
| ... max1 | ...? | appear between 0 and 1 times |
| ... min1 | ...+ | appear at least once |
| boundary | \b | boundary of a word |
| xBoundary | \B | not a boundary of a word |
| repeat (... ...) | {...,...} | repeat between n1 and n2 times | 
| repeatExactly ( ... ) | {...} | repeat exactly n times |
| atLeast ( ... ) | {...,} | repeat minimum n times |
| range ( ... ... ) | ...-... | range of characters e.g. a-z |
| option (...) | [\...] | choose any option |
| xOption (...) | [\^...] | choose any option except |
| capture ( ... ) | (...) | capture a group |
| xCapture ( ... ) | (?:...) | ignore group for capturing |
| namedCapture ( [groupName] ...) | (?P<groupName>...) | name a capture group |
| reuseCapture ... | (?P=...) | reuse a captured group - alt to using group2 etc |
| nonGreedy | "...?" | choose non greedily |
| xBacktrack | "...+" | to prevent backtracking behaviour |

note: long regex is case sensitive

in long regex % acts as the escape character rather backslash

# examples
match words containing pear:
```
%pear
```
match simple email address:
```
word min1 %@ word min1 %. option ( %com or %co.uk ) 
```
