from pyparsing import Word, OneOrMore, Literal, alphas, nums, alphanums, White, Combine, QuotedString, Optional
import pyparsing
import functools

space = OneOrMore(Word(' '))
prefix = '$'
name = (QuotedString("\"") | QuotedString("'"))
describe = Literal(f'{prefix}describe') + name
context = Literal(f'{prefix}context') + name
end = Literal(f'{prefix}end')

reserved = describe | context | end

code = Combine(OneOrMore(Optional(White()) + ~reserved + (Word(alphanums + '=+*%/@$#!^|\'\\"()[]{}:;   ') | White())))

describe_block = describe + code + end

if __name__ == '__main__':

    print(describe_block.parseString('''
$describe "test"
    print("test")
    test = 100
        test
$end
'''))
