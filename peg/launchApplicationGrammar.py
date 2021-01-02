#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu, leftrec, nomemo
from tatsu.parsing import leftrec, nomemo  # noqa
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class LaunchApplicationGrammarBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(LaunchApplicationGrammarBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class LaunchApplicationGrammarParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=LaunchApplicationGrammarBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(LaunchApplicationGrammarParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa
        self._expr_()
        self._check_eof()

    @tatsumasu()
    def _expr_(self):  # noqa
        self._launchCode_()
        self.name_last_node('launch')
        self._application_()
        self.name_last_node('app')
        with self._optional():
            self._preposition_()
        self.name_last_node('prep')
        with self._optional():
            self._workspace_()
        self.name_last_node('workspaceWord')
        with self._optional():

            def block5():
                self._word_()
            self._positive_closure(block5)
        self.name_last_node('workingDirectory')
        self._check_eof()
        self.ast._define(
            ['app', 'launch', 'prep', 'workingDirectory', 'workspaceWord'],
            []
        )

    @tatsumasu()
    def _workspace_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('workspace')
            with self._option():
                with self._optional():
                    self._token('working')
                self._token('directory')
            with self._option():
                self._token('project')
                with self._optional():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('name')
                            with self._option():
                                self._token('title')
                            with self._option():
                                self._token('index')
                            self._error('no available options')
            self._error('no available options')

    @tatsumasu()
    def _preposition_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('in')
            with self._option():
                self._token('at')
            with self._option():
                self._token('with')
            with self._option():
                self._token('on')
            with self._option():
                self._token('within')
            with self._option():
                self._token('inside')
            with self._option():
                self._token('for')
            self._error('no available options')

    @tatsumasu()
    def _launchCode_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('open')
            with self._option():
                self._token('launch')
            self._error('no available options')

    @tatsumasu()
    def _application_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('code')
                self._token('composer')
                with self._optional():
                    self._token('studio')
            with self._option():
                self._token('spider')
            with self._option():
                self._token('jupiter')
            with self._option():
                self._word_()
            self._error('no available options')

    @tatsumasu()
    def _word_(self):  # noqa
        self._pattern('[a-z]+')


class LaunchApplicationGrammarSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def expr(self, ast):  # noqa
        return ast

    def workspace(self, ast):  # noqa
        return ast

    def preposition(self, ast):  # noqa
        return ast

    def launchCode(self, ast):  # noqa
        return ast

    def application(self, ast):  # noqa
        return ast

    def word(self, ast):  # noqa
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'start'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = LaunchApplicationGrammarParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, LaunchApplicationGrammarParser, name='LaunchApplicationGrammar')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
