import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Lexer:

    def __init__(self, input_text):
        self.tokens = []
        self.current_token_number = 0
        for token in self.tokenize(input_text):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {'version', 'services', 'build', 'ports', 'image', 'volumes', 'environment', 'deploy', 'EOF',
                    'networks', 'environment'}

        token_specification = [
            ('ASSIGN', r'(: )|(:(?!.))'),  # Assignment operator (colon)
            # ('ID', r'([A-Za-z]+)|(^"$"[A-Za-z]+)|(\d+(\.\d*)?)|("(?:[^"\\]|\\.)*")')
            ('NEWLINE', r'\n'),  # Line endings and statement terminator
            # ('INDENTATION', r'[( {2}|\t)]'),  # Tab or 2 spaces
            ('INDENTATION', r'(( {2}|\t))'),  # Tab or 2 spaces
            ('LIST_INDICATOR', r'( - )|( -)|(- )|(-)'),  # Indicates a list
            ('SPACE', r' +'),  # spaces
            ('ID', r'(([A-Za-z]|(-)|(\d)|(\/)|(:(?! |\n))|(_))+)|(^"$"[A-Za-z]+)|(\d+(\.\d*)?)|("(?:[^"\\]|\\.)*")'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1
                value = match.group(type)
                yield Token(type, value, line_number, match.start() - line_start)
            elif type != 'SKIP':
                value = match.group(type)
                if type == 'ID' and value in keywords:
                    type = value
                yield Token(type, value, line_number, match.start() - line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' %
                               (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position - line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError('Error: No more tokens')
