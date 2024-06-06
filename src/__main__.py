import argparse
import os
import sys

from file import parse_json, get_obj
from forge import Forge
from metadata import VERSION


def path(value: str) -> str:
    if not os.path.exists(value) or not os.path.isfile(value):
        raise \
            argparse.ArgumentTypeError(
                "The path is not a file or doesn't exist.")
    return value


def args_parse(args: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('templatepath', type=path, nargs='*')
    parser.add_argument('--template-path', '-t', type=path,
                        dest='templatepath_arg', nargs='+',
                        default=[],
                        help=(
                            'This parameter stores '
                            'the template path.'
                        ))
    datagroup = parser.add_mutually_exclusive_group(required=True)
    datagroup.add_argument('--data', '-d', type=str, dest='data',
                           help='This parameter stores the json of the data.')
    datagroup.add_argument('--data-path', '--json' '-dp', '-j', type=path,
                           dest='datapath',
                           help=(
                               'This parameter stores the '
                               'json path of the data.'
                           ))
    parser.add_argument('--prefix', '-p', type=str, dest='prefix',
                        default='',
                        help=(
                            'This parameter stores the prefix to add '
                            'to the filename'
                        ))
    parser.add_argument('--suffix', '-s', type=str, dest='suffix',
                        default='',
                        help=(
                            'This parameter stores the suffix to add '
                            'to the filename'
                        ))
    parser.add_argument('--extension', '-e', type=str, dest='extension',
                        default='',
                        help=(
                            'This parameter stores the extension to '
                            'add to the filename'
                        ))
    parser.add_argument('--out-dir', '-o', type=str, dest='outdir',
                        default='.',
                        help=(
                            'This parameter stores the output path '
                            'directory'
                        ))
    parser.add_argument('--version', action='version', version=VERSION,
                        help='Shows the version of the TextForge')
    return parser.parse_args(args=args)


def main() -> None:
    args = args_parse(args=sys.argv[1:])
    templates = list(set(args.templatepath + args.templatepath_arg))
    data = parse_json(args.data) \
        if args.data is not None \
        else get_obj(args.datapath)
    forge = Forge()
    forge.forge(templatespath=templates, data=data,
                prefix=args.prefix, suffix=args.suffix,
                ext=args.extension, outdir=args.outdir)


if __name__ == '__main__':
    main()
