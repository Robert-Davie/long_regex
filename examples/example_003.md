us currency format ( based on regex101.com answer )

```
r"""
start
%$ max1
x_capture (
        digit repeat_between ( 1 3 )
        %,
        x_capture (
            digit repeat_exactly 3
            %,
        ) min0
        digit repeat_exactly 3
    or
        digit min1
)
x_capture (
    %. digit repeat_exactly 2
) max1
end
"""
```