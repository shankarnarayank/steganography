from argparse import ArgumentParser, RawTextHelpFormatter
from filetype import is_image
from os import path


def _consent(args, output):
    if path.exists(args[output]):
        args[output] = path.abspath(args[output])
        consent_ = input(f"Warning!!! \nThe '{args[output]}' file already exists."
                         f"\nDo you wish to overwrite?(y/n)[Default=n] ").lower() or 'n'
        if consent_ in ['y', 'yes']:
            pass
        elif consent_ in ['n', 'no']:
            print("Exiting...")
            exit(0)
        else:
            print("Invalid option.")
            _consent(args, output)
    return args


def is_valid_file(arg) -> str:
    if not path.isfile(arg):
        return arg
    else:
        with open(arg, 'r') as f:
            return f.read()


def get_args():
    my_args = ArgumentParser(fromfile_prefix_chars='_',
                             description="Hide/extract messages from an image using LSB encoding.\n"
                                         "(LSB = Least Significant Bit)",
                             # usage="python lsb.py [-h] en|de ...",
                             formatter_class=RawTextHelpFormatter,
                             epilog="Made by [shankar12789](https://github.com/shankar12789)")
    my_args.version = version_info
    my_args.add_argument('-v', '--version',
                         action='version')
    action = my_args.add_subparsers(title="Action",
                                    dest='action',
                                    required=True,
                                    metavar="encode|decode",
                                    help="Choose one of the two operation.")

    encode = action.add_parser(name='encode',
                               aliases=['en'],
                               help='Do encoding operation.\nFor more info: "python %(prog)s encode -h"',
                               formatter_class=RawTextHelpFormatter,
                               description="Encode a MESSAGE inside an IMAGE.\nSupported Image Formats: "
                                           "'CMYK', 'HSV', 'LAB', 'RGB', 'RGBA', 'RGBX', 'YCbCr'."
                                           "\nAny other format will result in error.",
                               epilog="Made by [shankar12789](https://github.com/shankar12789)")

    en_required = encode.add_argument_group("Required")
    en_required.add_argument('-i', '--input',
                             action='store',
                             type=str,
                             required=True,
                             metavar='IP_IMAGE',
                             help="Path of the IP_IMAGE into which the MESSAGE will be encoded."
                                  "\nNote: Has been tested with PNG images only."
                                  "\nOther extensions are NOT TESTED and may produce errors.")
    en_required.add_argument('-t', '--text',
                             action='store',
                             type=lambda x: is_valid_file(x),
                             required=True,
                             metavar="MESSAGE|FILE",
                             help='The MESSAGE to be encoded. The MESSAGE can be entered directly within quotes(" ") '
                                  '\nor from a file by appending \'@\' before the path of the FILE.'
                                  '\nEx: -t @/home/USER/Desktop/sample.txt'
                                  '\nNote: 1. Only full path and relative path are supported.'
                                  '\n      2. "~" and other environment variables are not resolved.'
                                  '\n      3. MESSAGE can be anything as long as their size is less than the IMAGE '
                                  '\n         itself,including the PASSWORD.')

    en_optional = encode.add_argument_group("Optional")
    en_optional.add_argument('-p', '--passwd',
                             action='store',
                             type=str,
                             metavar="PASSWORD",
                             help="The PASSWORD to encode your message. Default: IP_IMAGE name."
                                  "\nNote: 1. For maximum security generate a random string of minimum 8 characters."
                                  "\n      2. There is no password recovery method. "
                                  "\n         So, be sure to store your password.")
    en_optional.add_argument('-o', '--output',
                             action='store',
                             type=str,
                             metavar='OP_IMAGE',
                             dest="op_image",
                             help="Name of the resultant OP_IMAGE file. Default: \"encoded.png\"")

    decode = action.add_parser('decode',
                               aliases=['de'],
                               help='Do decoding operation. \nFor more info: "python %(prog)s decode -h"',
                               formatter_class=RawTextHelpFormatter,
                               description="Decode a MESSAGE from an IMAGE (if it exists).",
                               epilog="Made by [shankar12789](https://github.com/shankar12789)")

    de_required = decode.add_argument_group("Required")
    de_required.add_argument('-i', '--input',
                             action='store',
                             type=str,
                             required=True,
                             metavar="IP_IMAGE",
                             help="Path of the IP_IMAGE to be decoded.")
    de_required.add_argument('-p', '--passwd',
                             action='store',
                             type=str,
                             required=True,
                             metavar="PASSWORD",
                             help="The PASSWORD to decode the MESSAGE. "
                                  "\nDefault: The original name of the IMAGE before Encoding.")

    de_optional = decode.add_argument_group("Optional")
    de_optional.add_argument('-o', '--output',
                             action='store',
                             type=str,
                             metavar="FILE",
                             dest="op_text",
                             help="The path of the FILE where the decoded MESSAGE will be written to. "
                                  "\nDefault: The terminal itself")

    args = my_args.parse_args()
    args = vars(args)

    if not (path.exists(args['input']) and is_image(args['input'])):
        print(f"{args['input']} doesn't exist or unsupported.")
        exit(1)

    if args['passwd'] is None:
        args['passwd'] = path.basename(args['input'])

    if 'op_image' in args:
        if args['op_image'] is None:
            args['op_image'] = path.join(path.curdir, 'outputs', 'encoded.png')
        return _consent(args, 'op_image')

    if 'op_text' in args and args['op_text'] is not None and path.exists(args['op_text']):
        return _consent(args, 'op_text')

    return args


version_info = '1.0.5'

if __name__ == '__main__':
    print(get_args())
