import itertools
from typing import List

from anyspec.frontend.ast.node import ASTNode, Describe, Example, CodeNode, ASTLeaf, NamedNode

INDENT = '    '  # TODO(higumachan): これをどうにかする


def align_indent(code: str) -> str:
    code = code.strip('\n\r')
    num_indent = len(list(itertools.takewhile(lambda x: x == '\t' or x == ' ', code)))
    lines = [INDENT + line[num_indent:] for line in code.splitlines()]
    return "\n".join(lines)


class TestCaseBuilder(object):
    def __init__(self) -> None:
        self.testcases = []

    def linearize_preorder(self, ast: ASTNode, agg: List[ASTNode]):
        if isinstance(ast, Example):
            self.add_testcase(agg, ast)
            return

        for child in ast.children:
            self.linearize_preorder(child, agg + [ast])

    def add_testcase(self, nodes: List[ASTNode], terminal: Example):
        function_name = "test_" +\
                        "_".join([node.name for node in nodes if isinstance(node, NamedNode)]) +\
                        "_" + terminal.name
        codes_related_describes = [align_indent(code_node.code) for dnode in nodes if isinstance(dnode, Describe) for code_node in dnode.children if isinstance(code_node, CodeNode) and not isinstance(code_node, Example)]
        codes = codes_related_describes + [align_indent(terminal.code)]
        code = '\n'.join(codes)

        self.testcases.append(f"def {function_name}():\n{code}")


class PythonCompiler(object):
    def compile(self, ast: ASTNode):
        testcase_builder = TestCaseBuilder()
        testcase_builder.linearize_preorder(ast, [])
        code = "\n\n".join(testcase_builder.testcases) + '\n'
        return code


if __name__ == '__main__':
    pc = PythonCompiler()
    pc.compile(Describe("nadeko", [Describe("rikka", [Example("noe", "print('HelloWorld')")])]))
