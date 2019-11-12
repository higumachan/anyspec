from pyparsing import Word, OneOrMore, Literal, alphas, nums, alphanums, White, Combine, QuotedString, Optional, \
    Forward, ZeroOrMore
import pyparsing
import functools

from anyspec.frontend.ast.node import Example, Describe, Before, Let, Import


def anyspec_literal(name):
    prefix = '$'
    return Literal(f'{prefix}{name}')


space = OneOrMore(Word(' '))
name = (QuotedString("\"") | QuotedString("'"))
describe = anyspec_literal('describe') + name
context = anyspec_literal('context') + name
example = anyspec_literal('example') + name
before = anyspec_literal('before')
let = anyspec_literal('let')
let_exc = anyspec_literal('let!')
_import = anyspec_literal('import')
subject = anyspec_literal('subject')
end = anyspec_literal('end')

reserved = describe | context | end

code = Combine(OneOrMore(Optional(White()) + ~reserved + (Word(alphanums + '_.=+-*%/@$#!^|\'\\"()[]{}:;   ') | White())))

import_block = _import + code + end
import_block.setParseAction(Import.parse_action)

example_block = example + code + end
example_block.setParseAction(Example.parse_action)

before_block = before + code + end
before_block.setParseAction(Before.parse_action)

let_block = (let + name + code + end)
let_block.setParseAction(Let.parse_action)

subject_block = (subject + code + end)
subject_block.setParseAction(Let.subject_parse_action)

describe_block = Forward()
context_block = Forward()

describe_block <<= describe + ZeroOrMore(context_block | describe_block | example_block | before_block | let_block | subject_block) + end
describe_block.setParseAction(Describe.parse_action)

context_block <<= context + ZeroOrMore(context_block | describe_block | example_block | before_block | let_block | subject_block) + end
context_block.setParseAction(Describe.parse_action)


anyspec_parser = Optional(import_block) + ZeroOrMore(describe_block | context_block)

if __name__ == '__main__':

    print(anyspec_parser.parseString('''
$import
    import test
$end
$describe "test1"
    $context "test2"
        $let "val" 
            return "test"
        $end
        $subject
            return "subject"
        $end
        $before
            print("before")
            print("before")
        $end
        $example "case1"
            print("test1")
            print("test2")
        $end
    $end
    $describe "test3"
    $end
$end
'''))

    print(anyspec_parser.parseString("""
$describe "PythonCompiler"
    $context "compile"
        $let "cmp"
            return "test"
        $end
        $subject
            return cmp().compile(anyspec_parser.parseString(spec)[0])
        $end
    $end
$end
"""))
