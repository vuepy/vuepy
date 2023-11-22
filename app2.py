from pprint import pprint
import enum
from pyvue import *


class Role(enum.Enum):
    user = 'USER'
    bot = 'BOT'

    def __invert__(self):
        return Role.user if self == Role.bot else Role.bot


class Methods:
    def __init__(self, vm: 'Vue'):
        self.vm = vm

    def is_bot(self, val):
        return val == Role.bot.value

    def handle_change_role(self, owner):
        print(owner)
        owner.description = (~Role(owner.description)).value

    def handle_add_msg(self, owner):
        role = ~Role(self.vm.messages[-1]['role']) if len(self.vm.messages) else Role.user
        msg = {'role': role.value, 'content': ''}
        self.vm.messages.append(msg)
        # TODO 实现自动更新
        # self.vm.render()

    def handle_edit_msg(self, owner):
        if owner.icon == 'edit':
            state = 'eye'
        else:
            state = 'edit'
        owner.icon = state

    def handle_del_msg(self, i):
        with self.vm.options.el:
            msg = self.vm.messages.pop(i)
            # self.vm.render()
            print(f'del {i} {msg}')

    def handle_on_submit(self):
        with self.vm.options.el:
            clear_output()
            display(self.vm.dom)
            pprint(self.vm._data)


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

# data = {
#     'models': ['llama', 'llama2', 'llama2-chat'],
#     'model': 'llama',
#
#     'attr_options': attr_chain_list,
#     'option': attr_chain_list[0][1],
#
#     'top_p': 1,
#     'messages': [
#         {'role': Role.user.value, 'content': 'hello bot'},
#         {'role': Role.bot.value, 'content': '## h2 \nhello user'},
#         {'role': Role.user.value, 'content': 'world bot'},
#     ],
#     'on_edit': True,
# }


def setup(props, ctx, vm):
    models = ['llama', 'llama2', 'llama2-chat']
    model = ref('llama')
    attr_options = attr_chain_list
    option = ref(attr_chain_list[0][1])
    top_p = ref(1)
    messages = reactive([
        {'role': Role.user.value, 'content': 'hello bot'},
        {'role': Role.bot.value, 'content': '## h2 \nhello user'},
        {'role': Role.user.value, 'content': 'world bot'},
    ])
    on_edit = ref(True)

    _data = {
        'models': models,
        'model': model,
        'attr_options': attr_options,
        'option': option,
        'top_p': top_p,
        'messages': messages,
        'on_edit': on_edit,
    }

    def is_bot(val):
        return val == Role.bot.value

    def handle_change_role(owner):
        print(owner)
        owner.description = (~Role(owner.description)).value

    def handle_add_msg():
        role = ~Role(messages[-1]['role']) if len(messages) else Role.user
        msg = {'role': role.value, 'content': ''}
        messages.append(msg)

    def handle_edit_msg(owner):
        if owner.icon == 'edit':
            state = 'eye'
        else:
            state = 'edit'
        owner.icon = state

    def handle_del_msg(i):
        with vm.options.el:
            msg = messages.pop(i)
            print(f'del {i} {msg}')

    def handle_on_submit():
        with vm.options.el:
            clear_output()
            display(vm.dom)
            pprint(vm._data)

    return {
        **_data,

        'handle_change_role': handle_change_role,
        'handle_add_msg': handle_add_msg,
        'handle_edit_msg': handle_edit_msg,
        'handle_del_msg': handle_del_msg,
        'handle_on_submit': handle_on_submit,
        'is_bot': is_bot,
    }


vue = Vue({
    'el': widgets.Output(),
    # 'data': data,
    # 'methods': Methods,
    'setup': setup,
    'template': get_template_from_vue('ipywidgets_vue/app.vue'),
    # 'template': template,
}, debug=True)
display(vue.options.el)
display(vue.debug_log)
