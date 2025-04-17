# coding: utf-8
from pathlib import Path

import jinja2

import ipynb_converter

HERE = Path(__file__).absolute().parent
VLEAFLET_DIR = HERE.parent.parent.parent.parent / 'examples' / 'vleaflet'
PROMPT_TPL_DIR = HERE.parent.parent / 'prompts'
PROMPT_OUT_DIR = HERE / '_prompt'


def convert_ipynb_to_md(ipynb_path):
    with open(ipynb_path) as f:
        return ipynb_converter.ipynb_demo_to_markdown_prompt(f.read())


def gen_vleaflet_ctx():
    ipynb_files = []
    
    main_files = ['Map.ipynb', 'Basemaps.ipynb']
    for file in main_files:
        ipynb_files.append(VLEAFLET_DIR / file)
    
    layers_dir = VLEAFLET_DIR / 'layers'
    ipynb_files.extend(layers_dir.glob('*.ipynb'))
    
    controls_dir = VLEAFLET_DIR / 'controls'
    ipynb_files.extend(controls_dir.glob('*.ipynb'))
    
    all_content = []
    for ipynb_file in ipynb_files:
        if ipynb_file.name.startswith('.'):
            continue
        md_content = convert_ipynb_to_md(ipynb_file)
        all_content.append(f"{md_content}\n\n")
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PROMPT_TPL_DIR))
    llms_ctx = env.get_template('llms-ctx-vleaflet.txt.jinja2')
    out = llms_ctx.render(**{
        'docs': '\n'.join(all_content),
    })
    output_file = PROMPT_OUT_DIR / 'llms-ctx-vleaflet.md'
    with open(output_file, 'w') as f:
        f.write(out)


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
    
    gen_vleaflet_ctx()

    # final out
    sys_prompt_tpl = env.get_template('sys-prompt.html.jinja2')
    sys_prompt_out = sys_prompt_tpl.render(**{
        'vuepy_doc': vue_doc,
        'ipywui_examples': ipywui_examples,
    })

    with open(PROMPT_OUT_DIR / 'system-prompt.html', 'w') as f:
        f.write(sys_prompt_out)


if __name__ == '__main__':
    main()
