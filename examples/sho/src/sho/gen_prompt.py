# coding: utf-8
from pathlib import Path

import jinja2

import ipynb_converter

HERE = Path(__file__).absolute().parent

PROMPT_TPL_DIR = HERE.parent.parent / 'prompts'
PROMPT_OUT_DIR = HERE / '_prompt'


def main():
    ipynb_file = PROMPT_TPL_DIR / 'system_prompt_ipywui_examples.ipynb'
    with open(ipynb_file) as f:
        ipywui_examples = ipynb_converter.ipynb_demo_to_markdown_prompt(f.read())
        md_file = PROMPT_OUT_DIR / (ipynb_file.name.rstrip('ipynb') + 'md')
        with open(md_file, 'w') as md_f:
            md_f.write(ipywui_examples)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PROMPT_TPL_DIR))
    sys_prompt_tpl = env.get_template('sys_prompt.html.jinja2')
    sys_prompt_out = sys_prompt_tpl.render(ipywui_examples=ipywui_examples)

    with open(PROMPT_OUT_DIR / 'system_prompt.html', 'w') as f:
        f.write(sys_prompt_out)


if __name__ == '__main__':
    main()
