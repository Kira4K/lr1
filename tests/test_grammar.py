import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from grammar import Grammar, Rule
except ImportError:
    try:
        from grammar import Grammar, Rule
    except ImportError:
        import importlib.util
        import pathlib

        project_root = pathlib.Path(__file__).parent.parent
        grammar_path = project_root / 'src' / 'grammar.py'

        if not grammar_path.exists():
            grammar_path = project_root / 'grammar.py'

        spec = importlib.util.spec_from_file_location('grammar', grammar_path)
        grammar_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grammar_module)

        Grammar = grammar_module.Grammar
        Rule = grammar_module.Rule


class TestGrammar(unittest.TestCase):

    def test_grammar_creation(self):
        grammar = Grammar(
            nonterminals={'S', 'A'},
            terminals={'a', 'b'},
            rules=[
                Rule('S', ['A', 'S']),
                Rule('S', ['a']),
                Rule('A', ['b']),
            ],
            start_symbol='S'
        )

        self.assertEqual(len(grammar.nonterminals), 2)
        self.assertEqual(len(grammar.terminals), 2)
        self.assertEqual(len(grammar.rules), 3)
        self.assertEqual(grammar.start_symbol, 'S')

    def test_grammar_validation(self):
        grammar = Grammar(
            nonterminals={'S'},
            terminals={'a'},
            rules=[Rule('S', ['a'])],
            start_symbol='S'
        )
        self.assertTrue(grammar.validate())

        grammar = Grammar(
            nonterminals={'S'},
            terminals={'a'},
            rules=[Rule('S', ['a'])],
            start_symbol='X'
        )
        self.assertFalse(grammar.validate())

    def test_epsilon_rule(self):
        grammar = Grammar(
            nonterminals={'S'},
            terminals={'a'},
            rules=[
                Rule('S', ['a']),
                Rule('S', ['ε']),
            ],
            start_symbol='S'
        )

        self.assertEqual(len(grammar.rules), 2)
        self.assertEqual(str(grammar.rules[1]), "S -> ε")

    def test_get_rules_for(self):
        grammar = Grammar(
            nonterminals={'S', 'A'},
            terminals={'a', 'b'},
            rules=[
                Rule('S', ['A', 'S']),
                Rule('S', ['a']),
                Rule('A', ['b']),
                Rule('A', ['a', 'b']),
            ],
            start_symbol='S'
        )

        s_rules = grammar.get_rules_for('S')
        self.assertEqual(len(s_rules), 2)

        a_rules = grammar.get_rules_for('A')
        self.assertEqual(len(a_rules), 2)

        x_rules = grammar.get_rules_for('X')
        self.assertEqual(len(x_rules), 0)


if __name__ == '__main__':
    unittest.main()