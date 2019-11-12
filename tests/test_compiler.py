from anyspec.backend.python import PythonCompiler
from anyspec.frontend.parser import anyspec_parser


def test_simple_case():
    spec = """
$describe "simple_method" 
    $example "example1"
        print("HelloWorld")
    $end
$end
"""
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec)[0])

    assert code == """def test_simple_method_example1():
    print("HelloWorld")
"""
