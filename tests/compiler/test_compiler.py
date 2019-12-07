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
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():
    print('HelloWorld')
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
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():
    print('HelloWorld')
    print('HelloWorld')
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
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():
    print('before')
    print('before')
    print('HelloWorld')
    print('HelloWorld')
"""


def test_let():
    spec = """
    $describe "simple_method" 
        $let "val"
            return "test"
        $end
        $example "example1"
            print(val())
        $end
    $end
     """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():

    def val():
        return 'test'
    print(val())
"""


def test_let_multi_set():
    spec = """
        $describe "simple_method" 
            $let "val"
                return "test"
            $end
            $describe "simple_method2" 
                $let "val"
                    return "nadeko"
                $end
                $example "example1"
                    print(val())
                $end
            $end
        $end
         """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_simple_method2_example1():

    def val():
        return 'nadeko'
    print(val())
"""


def test_subject():
    spec = """
    $describe "simple_method" 
        $subject
            return "test"
        $end
        $example "example1"
            print(subject())
        $end
    $end
     """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():

    def subject():
        return 'test'
    print(subject())
"""


def test_import():
    spec = """
    $import
        import itertools
        import functools
    $end
    
    $describe "simple_method" 
        $example "example1"
            print("HelloWorld")
        $end
    $end
    """
    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """import itertools
import functools

def test_simple_method_example1():
    print('HelloWorld')
"""


def test_name_with_space():
    spec = """
    $describe "simple method" 
        $example "example1"
            print("HelloWorld")
        $end
    $end
    """

    cmp = PythonCompiler()
    code = cmp.compile(anyspec_parser.parseString(spec))

    assert code == """def test_simple_method_example1():
    print('HelloWorld')
"""
