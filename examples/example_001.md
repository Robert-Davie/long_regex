find reddit threads

```
r"""
capture ( start %http %s max1 %:// ) max1
capture ( word min1 ) max1
%. max1
capture ( %reddit.com/ or %redd.it/ )
capture ( %r/ word min1 %/ ) max1
capture ( %comments/ ) max1
capture ( word min1 )
"""
```