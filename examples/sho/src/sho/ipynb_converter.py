# coding: utf-8
import json


def ipynb_demo_to_markdown_prompt(nb_content: str) -> str:
    nb = json.loads(nb_content)
    out = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type')
        if cell_type == 'markdown':
            out.append('\n'.join(cell.get('source', [])))
        elif cell_type == 'code':
            try:
                prompt = ''
                code_out, widget_out = cell.get('outputs', ['', ''])
                code_out = json.loads(code_out['text'][0])
                vue_code = code_out.get('vue')
                if vue_code:
                    prompt += f'```vue\n{vue_code}\n```\n'

                setup_code = code_out.get('setup')
                if setup_code:
                    prompt += f'```python\n{setup_code}\n```\n'
            except Exception as e:
                print(e)
                continue

            out.append(prompt)

    return '\n'.join(out)
