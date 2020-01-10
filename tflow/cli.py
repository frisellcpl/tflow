import sys

from .cli_args import Arg


args = [
    Arg(
        name='name',
        data_type='str',
        required=True,
    ),
    Arg(
        name='version',
        data_type='int',
        required=True,
    ),
]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    """
    Initialize args and renders file.
    Use sys.exit to terminate program.
    """

    # parse cli args
    from .cli_args import parse_args, ValidationError
    try:
        parsed_args = parse_args(args)
        print(parsed_args)
    except ValidationError as e:
        eprint('Argument error: {msg}'.format(msg=e))
        sys.exit(1)

    name = parsed_args['name']
    version = parsed_args['version']
    
    # render CI file
    from .render import render
    render(
        name=name,
        version=version,
    )

    import subprocess
    # git tag current commit with version, then push.
    subprocess.run(['git', 'tag', str(version)])
    subprocess.run(['git', 'push', '--tags'])
    
    sys.exit(0)
