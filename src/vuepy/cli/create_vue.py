import os
import shutil
import argparse
import re


HERE = os.path.realpath(os.path.dirname(__file__))


def is_valid_package_name(package_name):
    if len(package_name) > 214:
        return False
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_]*$', package_name) is None:
        return False
    return True


def create_project(project_name, template='vue'):
    if not is_valid_package_name(project_name):
        print(f"Invalid package name: {project_name}")
        return

    pwd = os.getcwd()
    os.makedirs(os.path.join(pwd, project_name), exist_ok=True)

    # 拷贝模板
    template_dir = os.path.join(HERE, template)
    if not os.path.exists(template_dir):
        print(f"Template not found: {template}")
        return

    # TODO modified app.vue
    shutil.copytree(template_dir, project_name, dirs_exist_ok=True)


def add_arg_parser(parser: argparse.ArgumentParser):
    # create <your project name> [--template vue]
    subparsers = parser.add_subparsers(help='create vue help')
    p = subparsers.add_parser('create', help='create a new app')
    p.add_argument('project_name', type=str, help='The name of the project.')
    p.add_argument('--template', type=str, default='vue', help='The template to use.')
    p.set_defaults(func=create_project)


if __name__ == '__main__':
    # 创建项目
    parser = argparse.ArgumentParser(prog='PROG')
    add_arg_parser(parser)
    args = parser.parse_args()
    args.func(args)
