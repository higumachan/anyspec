import itertools
from typing import List

from anyspec.frontend.ast.node import ASTNode, Describe, Example, CodeNode, ASTLeaf, NamedNode, Before, Let, Import

INDENT = '    '  # TODO(higumachan): これをどうにかする


def align_indent(code: str, num_output_indent=1) -> str:
    code = code.strip('\n\r')
    num_indent = len(list(itertools.takewhile(lambda x: x == '\t' or x == ' ', code)))
    lines = [INDENT * num_output_indent + line[num_indent:] for line in code.splitlines()]
    return "\n".join(lines)


def let_to_function(let):
    return f"""{INDENT}def {let.name}():
{align_indent(let.code, num_output_indent=2)}"""  # TODO(higumachan): 2度呼び出したときは再利用する


class TestCaseBuilder(object):
    def __init__(self, root_nodes: List[ASTNode]) -> None:
        self._root_nodes = root_nodes
        self.testcases = []
        self.import_code = ""
        first_node = self._root_nodes[0]
        if isinstance(first_node, Import):
            self.import_code = align_indent(first_node.code, 0) + '\n\n'

    def describe_linearize_preorder(self):
        for root_node in [root_node for root_node in self._root_nodes if isinstance(root_node, Describe)]:
            self._linearize_preorder(root_node, [])

    def _linearize_preorder(self, ast: ASTNode, agg: List[ASTNode]):
        if isinstance(ast, Example):
            self.add_testcase(agg, ast)
            return

        for child in ast.children:
            self._linearize_preorder(child, agg + [ast])

    # TODO(higumachan): letで定義した変数は関数の形じゃなくても使えるようにする
    def add_testcase(self, nodes: List[ASTNode], terminal: Example):
        let_nodes = [let_node for dnode in nodes if isinstance(dnode, Describe) for let_node in dnode.children if isinstance(let_node, Let)]
        let_context = {}
        for ln in let_nodes:
            let_context[ln.name] = ln

        function_codes = [let_to_function(v) for v in let_context.values()]

        function_name = "test_" +\
                        "_".join([node.name for node in nodes if isinstance(node, NamedNode)]) +\
                        "_" + terminal.name
        codes_related_describes = [align_indent(code_node.code) for dnode in nodes if isinstance(dnode, Describe) for code_node in dnode.children if isinstance(code_node, Before)]
        codes = function_codes + codes_related_describes + [align_indent(terminal.code)]
        code = '\n'.join(codes)

        self.testcases.append(f"def {function_name}():\n{code}")


class PythonCompiler(object):
    def compile(self, ast_nodes: List[ASTNode]):
        testcase_builder = TestCaseBuilder(ast_nodes)
        testcase_builder.describe_linearize_preorder()
        code = testcase_builder.import_code + "\n\n".join(testcase_builder.testcases) + '\n'
        return code


if __name__ == '__main__':
    pc = PythonCompiler()
    pc.compile(Describe("nadeko", [Describe("rikka", [Example("noe", "print('HelloWorld')")])]))
