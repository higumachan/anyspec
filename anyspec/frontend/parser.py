from pyparsing import Word, OneOrMore, Literal, alphas, nums, alphanums, White, Combine, QuotedString, Optional, \
    Forward, ZeroOrMore
import pyparsing
import functools

from anyspec.frontend.ast.node import Example, Describe

space = OneOrMore(Word(' '))
prefix = '$'
name = (QuotedString("\"") | QuotedString("'"))
describe = Literal(f'{prefix}describe') + name
context = Literal(f'{prefix}context') + name
example = Literal(f'{prefix}example') + name
end = Literal(f'{prefix}end')

reserved = describe | context | end

code = Combine(OneOrMore(Optional(White()) + ~reserved + (Word(alphanums + '=+*%/@$#!^|\'\\"()[]{}:;   ') | White())))

example_block = example + code + end
example_block.setParseAction(Example.parse_action)

describe_block = Forward()
describe_block <<= describe + ZeroOrMore(describe_block | example_block) + end
describe_block.setParseAction(Describe.parse_action)

anyspec_parser = describe_block

if __name__ == '__main__':

    print(describe_block.parseString('''
$describe "test1"
    $describe "test2"
        $example "case1"
            print("test1")
            print("test2")
        $end
    $end
    $describe "test3"
    $end
$end
'''))
