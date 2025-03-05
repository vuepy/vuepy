# coding: utf-8
from pathlib import Path

import jinja2

import ipynb_converter

HERE = Path(__file__).absolute().parent
PROMPT_TPL_DIR = HERE.parent.parent / 'prompts'
PROMPT_OUT_DIR = HERE / '_prompt'


def main():
    ipynb_file = PROMPT_TPL_DIR / 'llms-ctx-ipywui.ipynb'
    with open(ipynb_file) as f:
        ipywui_examples = ipynb_converter.ipynb_demo_to_markdown_prompt(f.read())
        md_file = PROMPT_OUT_DIR / (ipynb_file.name.rstrip('ipynb') + 'md')
        with open(md_file, 'w') as md_f:
            md_f.write(ipywui_examples)

    vue_file = PROMPT_TPL_DIR / 'llms-ctx-vuepy.ipynb'
    with open(vue_file) as f:
        vue_doc = ipynb_converter.ipynb_demo_to_markdown_prompt(f.read())
        md_file = PROMPT_OUT_DIR / (vue_file.name.rstrip('ipynb') + 'md')
        with open(md_file, 'w') as md_f:
            md_f.write(vue_doc)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PROMPT_TPL_DIR))

    llms_ctx = env.get_template('llms-ctx.txt.jinja2')
    out = llms_ctx.render(**{
        'vuepy_doc': vue_doc,
        'ipywui_examples': ipywui_examples,
    })
    with open(PROMPT_OUT_DIR / 'llms-ctx.txt', 'w') as f:
        f.write(out)

    sys_prompt_tpl = env.get_template('sys-prompt.html.jinja2')
    sys_prompt_out = sys_prompt_tpl.render(**{
        'vuepy_doc': vue_doc,
        'ipywui_examples': ipywui_examples,
    })

    with open(PROMPT_OUT_DIR / 'system-prompt.html', 'w') as f:
        f.write(sys_prompt_out)


if __name__ == '__main__':
    main()
