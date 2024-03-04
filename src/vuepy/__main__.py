# coding: utf-8
import argparse

from vuepy.cli.create_vue import add_arg_parser


def main():
    parser = argparse.ArgumentParser(prog='PROG')
    add_arg_parser(parser)
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"error {e}")
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
