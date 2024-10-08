import threading
import time
from pprint import pprint
import enum
import pandas as pd
from IPython.display import clear_output
from IPython.display import display

from vuepy import reactive
from vuepy import ref


class Role(enum.Enum):
    user = 'USER'
    bot = 'BOT'

    def __invert__(self):
        return Role.user if self == Role.bot else Role.bot


attr_chain_list = [
    ('op1', {
        'name': 'l1',
        'in': [1, 2, 4],
    }),
    ('op2', {
        'name': 'l2',
        'in': [5, 6, 7],
    }),
]

md_str = '''
## h2
hello world
```python
def f():
  print("hello world!")
  
f()
>>> hello world!

```

'''


def setup(props, ctx, app):
    models = ['llama', 'llama2', 'llama2-chat']
    model = ref('llama')
    attr_options = attr_chain_list
    option = ref(attr_chain_list[0][1])
    top_p = ref(1)
    show_dialog = ref(True)
    messages = ref(reactive([
        {'role': Role.user.value, 'content': 'hello bot'},
        {'role': Role.bot.value, 'content': '## h2 \nhello user'},
        {'role': Role.user.value, 'content': 'world bot'},
    ]))
    on_edit = ref(True)
    df = ref(pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]}))

    def is_bot(val):
        return val == Role.bot.value

    def handle_change_role(owner):
        print(owner)
        owner.description = (~Role(owner.description)).value

    def handle_add_msg():
        role = ~Role(messages.value[-1]['role']) if len(messages.value) else Role.user
        msg = reactive({'role': role.value, 'content': ''})
        messages.value.append(msg)

    def handle_edit_msg(owner):
        def edit_work():
            msg = messages.value[1]
            msg.content = ''
            for s in md_str:
                msg.content += s
                time.sleep(0.05)

        if owner.icon == 'edit':
            state = 'eye'
            thread = threading.Thread(target=edit_work, args=())
            thread.start()
        else:
            state = 'edit'

        owner.icon = state

    def handle_del_msg(i):
        # with vm.options.el:
            msg = messages.value.pop(i)
            print(f'del {i} {msg}')

    def handle_on_submit():
        df.value = pd.concat([df.value, df.value])
        with app.options.el:
            clear_output()
            display(app.dom)
            pprint(app._data)

    def send_msg():
        app.message.success({'message': 'hello world!', 'duration': 0, 'show_close': True})

    def switch_dialog():
        show_dialog.value = not show_dialog.value


    return locals()
