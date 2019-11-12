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


def test_multi_line():
    spec = """
    $describe "simple_method" 
        $example "example1"
            print("HelloWorld")
            print("HelloWorld")
        $end
    $end
    """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec)[0])

    assert code == """def test_simple_method_example1():
    print("HelloWorld")
    print("HelloWorld")
"""


def test_before():
    spec = """
    $describe "simple_method" 
        $before
            print("before")
            print("before")
        $end
        $example "example1"
            print("HelloWorld")
            print("HelloWorld")
        $end
    $end
    """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec)[0])

    assert code == """def test_simple_method_example1():
    print("before")
    print("before")
    print("HelloWorld")
    print("HelloWorld")
"""
