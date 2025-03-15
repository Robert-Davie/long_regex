# possible operations

| Long Regex | Normal Regex | Explanation
| --- | --- | --- |
| start | ^ | Start of line |
| end | $ | End of line |
| digit | \d | digit |
| x_digit | \D | not a digit |
| space |   | a literal space character |
| whitespace | \s | a whitespace character |
| x_whitespace | \S | not a whitespace character |
| word | \w | a word character |
| x_word | \W | not a word character |
| %ABCabc | ABCabc | use % sign to write string of characters |
| literal ( ... ) | ... | copy a string exactly (useful for strings with spaces) |
| group2 | \2 | reference nth group from 1 to 9, here n=2 |
| string_start | \A | Start of line (differnt to ^ in multiline mode) |
| string_end | \Z | End of line (different to $ in multiline mode) |
| any_char | . | any character apart from newline |
| or | \| | or |
| look_ahead ( ... ) | (?=...) | lookahead |
| x_look_ahead ( ... ) | (?!...) | opposite of lookahead |
| ... min0 | ...* | appear any number of times including 0 |
| ... max1 | ...? | appear between 0 and 1 times |
| ... min1 | ...+ | appear at least once |
| boundary | \b | boundary of a word |
| x_boundary | \B | not a boundary of a word |
| repeat (... ...) | {...,...} | repeat between n1 and n2 times | 
| repeat_exactly ( ... ) | {...} | repeat exactly n times |
| at_least ... | {...,} | repeat minimum n times |
| range ( ... ... ) | ...-... | range of characters e.g. a-z |
| choice ( ... ) | [\...] | choose any option |
| x_choice ( ... ) | [\^...] | choose any option except |
| capture ( ... ) | (...) | capture a group |
| x_capture ( ... ) | (?:...) | ignore group for capturing |
| named_capture ( group_name ... ) | (?P\<group_name\>...) | name a capture group |
| reuse_capture ... | (?P=...) | reuse a captured group - alt to using group2 etc |
| x_greedy | "...?" | choose non greedily |
| x_backtrack | "...+" | to prevent backtracking behaviour |

note: long regex is case sensitive

in long regex % acts as the escape character rather backslash

# examples
match words containing pear:
```
%pear
```
match simple email address:
```
word min1 %@ word min1 %. choice ( %com or %co.uk ) 
```
