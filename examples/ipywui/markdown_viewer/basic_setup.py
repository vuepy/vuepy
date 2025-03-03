from vuepy import ref

md_src = r"""
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

### LaTeX
$$
a > b,b > c \Rightarrow a > c 
$$

$$
\begin{array}{c} 
  \forall A \in S \\ 
  P \left( A \right) \ge 0 
\end{array}
$$
"""

def setup(props, ctx, vm):
    md = ref(md_src)
    return locals()
