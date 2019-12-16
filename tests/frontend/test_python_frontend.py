from anyspec.frontend.spec_ast.node import Describe, Example, Before, Let


def test_simple_case():
    spec = """
with describe("simple method"):
    with example("example"):
        print("HelloWorld")
    """

    ast = python_frontend(spec)

    assert ast == [
        Describe("simple method", [
            Example("example", 'print("HelloWorld")')
        ])
    ]


def test_before():
    spec = """
with describe("simple method"):
    with before():
        print("before")
    with example("example1")
        print("HelloWorld")
"""

    ast = python_frontend(spec)

    assert ast == [
        Describe("simple method", [
            Before('print("before")'),
            Example("example1", 'print("HelloWorld")')
        ])
    ]


def test_let():
    spec = """
with describe("simple_method"):
    let.val = "test"
    with example("example1")
        print(let.val)
    $end
$end
    """
    ast = python_frontend(spec)

    assert ast == [
        Describe("simple method", [
            Let("test", 'return "test"'),
            Example("example1", 'print("HelloWorld")'),
        ])
    ]


def test_let_block():
    spec = """
with describe("simple_method"):
    def val():
        a = "not test"
        return "test"
    with example("example1"):
        print(val())
    """
    ast = python_frontend(spec)

    assert ast == [
        Describe("simple method", [
            Let("val", 'a = "not test"\nreturn "test"'),
            Example("example1", 'print("HelloWorld")'),
        ])
    ]
