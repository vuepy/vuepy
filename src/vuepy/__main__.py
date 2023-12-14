# coding: utf-8
import argparse

from cli.create_vue import add_arg_parser


def main():
    parser = argparse.ArgumentParser(prog='PROG')
    add_arg_parser(parser)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
