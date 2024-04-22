import pathlib
from glob import glob
from vuepy import *


def setup(props, ctx, vm):
    Compile = import_sfc(pathlib.Path(__file__).parent / 'Compile.vue')
    m = ref('xxx')

    comp = ref(None)

    def on_compile_submit():
        print("on_compile_submit")

    def get_gguf_models(model_dir):
        return glob(f"{model_dir}/*.gguf")

    QUANTIZE_OPTS = ['q4_0', 'q4_1', 'q4_k', 'q5_0', 'q5_1', 'q5_k', 'q6_k', 'q8_0']
    hf_models_path = ref('/Users/kuroro/CMC/models/codellama/instruct/7b')
    org_models = ref(get_gguf_models(hf_models_path.value))
    org_model = ref(None)
    quantize_opt = ref('q4_0')

    def calc_quantize_model():
        org_model_value = org_model.value or ""
        value = f".{quantize_opt.value}.".join(org_model_value.rsplit('.', 1))
        return value if org_model_value else ''

    quantize_model = computed(calc_quantize_model)

    chat_models = ref(get_gguf_models(hf_models_path.value))
    chat = reactive({
        'model': None,
        'system': 'You are a helpful assistant. 你是一个乐于助人的助手。',
        'first_instruction': '',
        'ctx_size': 2048,  # // size of the prompt context (default: 512, 0 = loaded from model)
        'threads': 8,
        'temp': 0.1,  # // temperature (default: 0.8
        'top_k': 1000,  # // top-k sampling (default: 40, 0=disabled
        'top_p': 0.99,  # // top-p sampling (default: 0.9, 1.0=disabled
        'repeat_penalty': 2.0,  # // penalize repeat sequence of tokens (default: 1.1, 1.0 = disabled)
    })

    def compile_llama_cpp():
        print('bash build.sh')
        # !bash build.sh

    def convert_model():
        print(f'python convert.py {hf_models_path.value}')
        # !python convert.py {model_path.value}
        # print(_exit_code)

    def quantify_model():
        """
        https://github.com/ggerganov/llama.cpp/pull/1684
        :return:
        """
        print(f"bash build-metal/bin/quantize {org_model.value} {quantize_model.value} {quantize_opt.value}")

    def refresh_models():
        chat_models.value = get_gguf_models(hf_models_path.value)

    def exec_chat():
        print(f"bash chat.sh -m {chat.model} -i {chat.first_instruction}")
        # with vm.options.el:
        #     clear_output()
        #     display(vm.dom)
        #     pprint(vm._data)

    return locals()


# vue = Vue({
#     'el': widgets.Output(),
#     'setup': setup,
#     'template': get_template_from_vue('examples/app-llamacpp-dev.vue'),
# }, debug=False)
# display(vue.options.el)
# display(vue.debug_log)
