$import
    from anyspec.backend.python import PythonCompiler
    from anyspec.frontend.parser import anyspec_parser
$end

$describe "PythonCompiler"
    $describe "compile"
        $let "cmp"
            return PythonCompiler()
        $end

        $subject
            return cmp().compile(anyspec_parser.parseString(spec()))
        $end

        $describe "simple_case"
            $let "spec"
                return """
$describe "simple_method"
    $example "example1"
        print("HelloWorld")
    $end
$end
                """
            $end

            $example "compile"
                assert subject() == '''def test_simple_method_example1():
    print('HelloWorld')
'''
            $end
        $end

        $describe "multi_line"
            $let "spec"
                return """
$describe "simple_method"
    $example "example1"
        print("HelloWorld")
        print("HelloWorld")
    $end
$end
                """
            $end

            $example "compile"
                assert subject() == '''def test_simple_method_example1():
    print('HelloWorld')
    print('HelloWorld')
'''
            $end
        $end

        $describe "before"
            $let "spec"
                return """
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
            $end
            $example "compile"
                assert subject() == """def test_simple_method_example1():
    print('before')
    print('before')
    print('HelloWorld')
    print('HelloWorld')
"""
            $end
        $end
        $describe "let"
            $let "spec"
                return """
    $describe "simple_method"
        $let "val"
            return "test"
        $end
        $example "example1"
            print(val())
        $end
    $end
     """
            $end
            $example "compile"
                assert subject() == """def test_simple_method_example1():

    def val():
        return 'test'
    print(val())
"""
            $end
        $end
        $describe "let_multi_set"
            $let "spec"
                return """
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
            $end
            $example "compile"
                assert subject() == """def test_simple_method_simple_method2_example1():

    def val():
        return 'nadeko'
    print(val())
"""
            $end
        $end

        $describe "subject"
            $let "spec"
                return """
$describe "simple_method"
    $subject
        return "test"
    $end
    $example "example1"
        print(subject())
    $end
$end
 """
            $end
            $example "compile"
                assert subject() == """def test_simple_method_example1():

    def subject():
        return 'test'
    print(subject())
"""
            $end
        $end

        $describe "import"
            $let "spec"
                return """
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
            $end
            $example "compile"
                assert subject() == """import itertools
import functools

def test_simple_method_example1():
    print('HelloWorld')
"""
            $end
        $end
    $end
$end