import unittest
import io
import sys
from grammar_parser import GrammarParser


class TestGrammarParser(unittest.TestCase):
    def test_parse_simple_grammar(self):
        input_text = """2 2 3
S A
a b
S -> a S b
S -> 
A -> b A
S
2
aabb
abb"""

        sys.stdin = io.StringIO(input_text)

        grammar, words = GrammarParser.parse_from_stdin()

        self.assertEqual(grammar.start_symbol, 'S')
        self.assertEqual(len(grammar.nonterminals), 2)
        self.assertEqual(len(grammar.terminals), 2)
        self.assertEqual(len(grammar.rules), 3)
        self.assertEqual(words, ['aabb', 'abb'])

        sys.stdin = sys.__stdin__

    def test_invalid_input_raises_exception(self):
        input_text = """1 1"""
        sys.stdin = io.StringIO(input_text)

        with self.assertRaises(ValueError):
            GrammarParser.parse_from_stdin()

        sys.stdin = sys.__stdin__


if __name__ == '__main__':
    unittest.main()