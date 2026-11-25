# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from vuepy.version import VERSION


def show_version(_args):
    print(f"vuepy {VERSION}")


def register_subcommand(subparsers):
    parser = subparsers.add_parser('version', help='show vuepy version')
    parser.set_defaults(func=show_version)
