# coding: utf-8
import json


def ipynb_demo_to_markdown_prompt(file_path, nb_content: str) -> str:
    nb = json.loads(nb_content)
    out = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type')
        if cell_type == 'markdown':
            out.append(''.join(cell.get('source', [])))
        elif cell_type == 'code':
            code_source = '\n'.join(cell.get('source', []))
            if code_source.startswith('##ignore'):
                continue
            prompt = ''
            try:
                cell_output = cell.get('outputs')
                if not cell_output:
                    continue
                for code_out in cell_output:
                    if 'text' not in code_out:
                        print('no text in code_out')
                        continue
                    code_text = code_out['text'][0]
                    code_out = json.loads(code_text)
                    vue_code = code_out.get('vue')
                    if vue_code:
                        prompt += f'```vue\n{vue_code}\n```\n'

                    setup_code = code_out.get('setup')
                    if setup_code:
                        prompt += f'```python\n{setup_code}\n```\n'
            except json.JSONDecodeError as e:
                msg = f"convert {file_path} error: {repr(e)}, code_text: {code_text}"
                print(msg)
            except Exception as err:
                msg = f"convert {file_path} error: {repr(err)}"
                print(msg)

            out.append(prompt)

    return '\n'.join(out)
