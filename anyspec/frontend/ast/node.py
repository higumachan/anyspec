from typing import List


class ASTNode(object):
    @property
    def children(self) -> List['ASTNode']:
        return self._children

    def traverse_preorder(self) -> List['ASTNode']:
        result = [self]
        for child in self.children:
            result.extend(child.traverse_preorder())
        return result


class ASTLeaf(ASTNode):
    @property
    def children(self) -> List['ASTNode']:
        return []


class CodeNode(object):
    @property
    def code(self) -> str:
        return self._code


class NamedNode(object):
    @property
    def name(self):
        return self._name


class Describe(ASTNode, NamedNode):
    def __init__(self, name, children):
        self._name = name
        self._children = children

    @classmethod
    def parse_action(cls, string, locs, tokens):
        name = tokens[1]
        children = tokens[2:-1]

        return cls(name, children)

    def __repr__(self):
        return f'Describe(name={self._name}, children={self._children}'


class Example(ASTLeaf, CodeNode, NamedNode):
    def __init__(self, name, code):
        self._name = name
        self._code = code

    @classmethod
    def parse_action(cls, string, locs, tokens):
        name = tokens[1]
        code = tokens[2]
        return cls(name, code)

    def __repr__(self):
        return f'Example(name={self._name}, code={self._code}'


class Before(ASTLeaf, CodeNode):
    def __init__(self, code):
        self._code = code

    @classmethod
    def parse_action(cls, string, locs, tokens):
        code = tokens[2]
        return cls(code)

    def __repr__(self):
        return f'Before(code={self._code}'
