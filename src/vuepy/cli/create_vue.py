import os
import shutil
import argparse
import re
from pathlib import Path
from string import Template

from vuepy.cli import log_error
from vuepy.cli import log_info

HERE = Path(__file__).absolute().parent


def is_valid_package_name(package_name):
    if len(package_name) > 214:
        return False
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_]*$', package_name) is None:
        return False
    return True


def create_project(args):
    project_name = input("✔ Project_name: ")
    template = args.template
    if not is_valid_package_name(project_name):
        log_error(f"Create project failed, Invalid package name: {project_name}")
        return

    proj_dir = Path(os.getcwd()) / project_name
    if proj_dir.exists():
        log_error(f"Create project failed, dir already exists: {proj_dir}")
        return
    else:
        os.makedirs(proj_dir)

    # 拷贝模板
    template_dir = HERE / f"template_{template}"
    if not template_dir.exists():
        log_error(f"Create project failed, Template not found: {template}")
        return

    ipywui_components_path = HERE.parent.parent / 'ipywui' / 'components'
    if not ipywui_components_path.exists():
        log_error(f"Create Project failed, ipywui not found: {ipywui_components_path}")
        return

    shutil.copytree(ipywui_components_path, proj_dir / 'ipywui')
    shutil.copytree(template_dir, proj_dir, dirs_exist_ok=True)

    with open(proj_dir / 'App.vue', 'r') as f:
        app_vue = f.read()
    app_vue = Template(app_vue).substitute({
        'js_stubs_path': HERE.parent / 'js_stubs',
        'ipywui_path': './ipywui',
    })
    with open(proj_dir / 'App.vue', 'w') as f:
        f.write(app_vue)

    log_info("")
    log_info(f"Scaffolding project in ./{project_name}")
    log_info("Done.")


def add_arg_parser(parser: argparse.ArgumentParser):
    # create <your project name> [--template vue]
    subparsers = parser.add_subparsers(help='create vue help')
    p = subparsers.add_parser('create', help='create a new app')
    # p.add_argument('project_name', type=str, help='The name of the project.')
    p.add_argument('--template', type=str, default='vue', help='The template to use.')
    p.set_defaults(func=create_project)


if __name__ == '__main__':
    # 创建项目
    parser = argparse.ArgumentParser(prog='PROG')
    add_arg_parser(parser)
    args = parser.parse_args()
    args.func(args)
