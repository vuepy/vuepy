from vuepy import ref

md_src = """
# H1
## H2

```python
def foo():
    print("hello world")
    
```
"""


def setup(props, ctx, vm):
    md = ref(md_src)

    return locals()
