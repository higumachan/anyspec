import itertools
from _ast import Module, FunctionDef, AST, Expr, arguments
from typing import List
import codegen
import ast

from toolz import concat

from anyspec.frontend.spec_ast.node import ASTNode, Describe, Example, CodeNode, ASTLeaf, NamedNode, Before, Let, Import

INDENT = '    '  # TODO(higumachan): これをどうにかする


def align_indent(code: str, num_output_indent=1) -> str:
    code = f"def test():" + code
    parsed_tree = ast.parse(code)
    def_function_node = parsed_tree.body[0]
    assert isinstance(def_function_node, FunctionDef)
    code = "\n".join([codegen.to_source(expr_node) for expr_node in def_function_node.body])
    return indent_code(code, num_output_indent)


def parse_code(code: str) -> List[AST]:
    code = f"def test():" + code  # indentがあるとparseできないため一旦関数の中に入れる
    parsed_tree = ast.parse(code)
    def_function_node = parsed_tree.body[0]
    assert isinstance(def_function_node, FunctionDef)
    return def_function_node.body


def create_function_def(name, exprs: List[AST]):
    return FunctionDef(name=name, body=exprs, args=arguments(args=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[]), decorator_list=[], returns=None)


def create_module(nodes: List[AST]):
    return Module(body=nodes)


def transform_code(code: str, function_name: str) -> str:
    code = f"def {function_name}():" + code
    parsed_tree = ast.parse(code)
    code = codegen.to_source(parsed_tree)
    return code


def indent_code(code: str, num_indent: int) -> str:
    lines = [INDENT * num_indent + line for line in code.splitlines()]
    return "\n".join(lines)


def let_to_function(let: Let) -> FunctionDef:
    nodes = parse_code(let.code)
    return create_function_def(let.name, nodes)


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
        codes_related_describes = list(concat([parse_code(code_node.code) for dnode in nodes if isinstance(dnode, Describe) for code_node in dnode.children if isinstance(code_node, Before)]))
        codes = function_codes + codes_related_describes + parse_code(terminal.code)
        code = codegen.to_source(create_function_def(function_name, codes))

        self.testcases.append(code)


class PythonCompiler(object):
    def compile(self, ast_nodes: List[ASTNode]):
        testcase_builder = TestCaseBuilder(ast_nodes)
        testcase_builder.describe_linearize_preorder()
        code = testcase_builder.import_code + "\n\n".join(testcase_builder.testcases) + '\n'
        return code


if __name__ == '__main__':
    pc = PythonCompiler()
    print(pc.compile([Describe("nadeko", [Describe("rikka", [Example("noe", "print('HelloWorld')")])])]))
