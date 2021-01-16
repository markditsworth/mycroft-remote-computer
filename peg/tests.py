# -*- coding: utf-8 -*-
import json
from tatsu import parse
from tatsu.util import asjson


tests = '''open code composer in environment monitoring
open code composer studio with workspace solar charger
launch jupiter at temporary project
launch spider in project mycroft remote computer
open jupiter with working directory statistics
open app
open something on workspace test
launch code composer studio for project name sparky
open visual studio in mycroft remote computer
launch visual studio code with project title new thing
launch spider with project title scumbag'''

test_lines = tests.split('\n')

def main():
    with open('launchApplicationGrammar.ebnf', 'r') as fObj:
        GRAMMAR = fObj.read()
    
    for x in test_lines:
        print("line: '{}'".format(x))
        ast = asjson(parse(GRAMMAR, x))
        print('dir:  {}'.format(ast['workingDirectory']))
        print()
        


if __name__ == '__main__':
    main()

