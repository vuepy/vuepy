from vuepy import ref

md_src = """
### H3

This is a **bold** text and this is an *italic* text.   
link to [vuepy](https://github.com/vuepy)

### Code

    def foo():
        print("hello world")
        return 1

### List

- item1
- item2

"""

def setup(props, ctx, vm):
    md = ref(md_src)

    return locals()
