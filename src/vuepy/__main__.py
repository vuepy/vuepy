# coding: utf-8
# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import argparse

from vuepy.cli.create_vue import register_subcommand as register_create
from vuepy.cli.run_vue import register_subcommand as register_run


def main():
    parser = argparse.ArgumentParser(prog='vuepy')
    subparsers = parser.add_subparsers(help='sub-command help')
    register_create(subparsers)
    register_run(subparsers)
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        exit(0)
    try:
        args.func(args)
    except Exception as e:
        print(f"error {e}")
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
