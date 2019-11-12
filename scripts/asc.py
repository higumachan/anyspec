import argparse
from pathlib import Path

from anyspec.backend.python import PythonCompiler
from anyspec.frontend.parser import anyspec_parser


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('inputs', type=Path, nargs='+')
    parser.add_argument('output_dir', type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir  # type: Path

    compiler = PythonCompiler()
    for inp in args.inputs:  # type: Path
        with inp.open() as f:
            ast_root_nodes = anyspec_parser.parseFile(f)  # TODO(higumachan): create root parser
        code = compiler.compile(ast_root_nodes)
        with (output_dir / ("test_" + inp.stem + "_spec" + ".py")).open("w") as f:
            f.write(code)


if __name__ == '__main__':
    main()