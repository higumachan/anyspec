from pyparsing import Word, OneOrMore, Literal, alphas, nums, alphanums, White, Combine, QuotedString, Optional, \
    Forward, ZeroOrMore
import pyparsing
import functools

from anyspec.frontend.ast.node import Example, Describe, Before


def anyspec_literal(name):
    prefix = '$'
    return Literal(f'{prefix}{name}')

space = OneOrMore(Word(' '))
name = (QuotedString("\"") | QuotedString("'"))
describe = anyspec_literal('describe') + name
context = anyspec_literal('context') + name
example = anyspec_literal('example') + name
end = anyspec_literal('end')
before = anyspec_literal('before')

reserved = describe | context | end

code = Combine(OneOrMore(Optional(White()) + ~reserved + (Word(alphanums + '=+*%/@$#!^|\'\\"()[]{}:;   ') | White())))

example_block = example + code + end
example_block.setParseAction(Example.parse_action)

before_block = before + code + end
before_block.setParseAction(Before.parse_action)

describe_block = Forward()
describe_block <<= describe + ZeroOrMore(describe_block | example_block | before_block) + end
describe_block.setParseAction(Describe.parse_action)


anyspec_parser = describe_block

if __name__ == '__main__':

    print(describe_block.parseString('''
$describe "test1"
    $describe "test2"
        $before
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
