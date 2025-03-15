ipv4 addresses (based on https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp )

```
r"""
start
capture (
    capture (
            %25
            choice ( range ( 0 5 ) )
        or
            capture (
                    %2 choice ( range ( 0 4 ) )
                or
                    %1 digit
                or
                    choice ( range ( 1 9 ) )
                or
            )
        digit
    )
    %. max1
    boundary
) repeat_exactly 4
end
"""
```