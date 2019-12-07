import ast

from pyparsing import Word, OneOrMore, Literal, alphas, nums, alphanums, White, Combine, QuotedString, Optional, \
    Forward, ZeroOrMore, Token
import pyparsing
import functools

from anyspec.frontend.spec_ast.node import Example, Describe, Before, Let, Import


def anyspec_literal(name):
    prefix = '$'
    return Literal(f'{prefix}{name}')


class PythonCode(Token):
    def __init__(self):
        super().__init__()
        self.name = "PythonCode"

    def parseImpl(self, instring, loc, doActions=True):
        indent = instring[:loc].splitlines()[-1]
        lines = instring[loc:].splitlines()
        ll = ""
        result = ""
        next_loc = loc
        result_loc = loc
        for i, l in enumerate(lines):
            lt = l
            if l.startswith(indent):
                lt = lt[len(indent):]
            ll_tmp = ll + lt + '\n'
            next_loc += len(l) + 1
            try:
                #print('(' + ll_tmp + ')')
                ast.parse(ll_tmp)
            except SyntaxError as e:
                pass
            else:
                result = ll_tmp
                result_loc = next_loc
            ll = ll_tmp
        #print(f"result='{result}'")
        return result_loc, instring[loc:result_loc]


space = OneOrMore(Word(' '))
name = (QuotedString("\"") | QuotedString("'"))
describe = anyspec_literal('describe') + name
context = anyspec_literal('context') + name
example = anyspec_literal('example') + name
it = anyspec_literal('it') + name
before = anyspec_literal('before')
let = anyspec_literal('let')
let_exc = anyspec_literal('let!')
_import = anyspec_literal('import')
subject = anyspec_literal('subject')
end = anyspec_literal('end')

reserved = describe | context | end

code = Combine(White() + PythonCode())

import_block = _import + code + end
import_block.setParseAction(Import.parse_action)

example_block = example + code + end
example_block.setParseAction(Example.parse_action)

it_block = it + code + end
it_block.setParseAction(Example.parse_action)

before_block = before + code + end
before_block.setParseAction(Before.parse_action)

let_block = (let + name + code + end)
let_block.setParseAction(Let.parse_action)

subject_block = (subject + code + end)
subject_block.setParseAction(Let.subject_parse_action)

describe_block = Forward()
context_block = Forward()

describe_block <<= describe + ZeroOrMore(context_block | describe_block | example_block | it_block | before_block | let_block | subject_block) + end
describe_block.setParseAction(Describe.parse_action)

context_block <<= context + ZeroOrMore(context_block | describe_block | example_block | it_block | before_block | let_block | subject_block) + end
context_block.setParseAction(Describe.parse_action)


anyspec_parser = Optional(import_block) + OneOrMore(describe_block | context_block)

if __name__ == '__main__':

    print(anyspec_parser.parseString('''
$import
    import test
$end
$describe "Hello"
    $let "test"
        print("test")
        a = """
        $end
        """
    $end
$end
'''))
