import itertools

from anyspec.frontend.ast.node import ASTNode, Describe, Example, CodeNode


def align_indent(code: str) -> str:
    code = code.strip('\n\r')
    num_indent = len(list(itertools.takewhile(lambda x: x == '\t' or x == ' ', code)))
    lines = [line[num_indent:] for line in code.splitlines()]
    return "\n".join(lines)


class PythonCompiler(object):
    def compile(self, ast: ASTNode):
        code = '\n'.join([n.code for n in ast.traverse_preorder() if isinstance(n, CodeNode)])
        return align_indent(code)


if __name__ == '__main__':
    pc = PythonCompiler()
    pc.compile(Describe("nadeko", [Describe("rikka", [Example("noe", "print('HelloWorld')")])]))
