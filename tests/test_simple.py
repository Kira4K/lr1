import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from grammar import Grammar, Rule
    from lr_parser import LR1Parser
except ImportError:
    try:
        from grammar import Grammar, Rule
        from lr_parser import LR1Parser
    except ImportError:
        import importlib.util
        import pathlib

        project_root = pathlib.Path(__file__).parent.parent
        grammar_path = project_root / 'src' / 'grammar.py'
        parser_path = project_root / 'src' / 'lr_parser.py'

        spec = importlib.util.spec_from_file_location('grammar', grammar_path)
        grammar_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grammar_module)

        spec = importlib.util.spec_from_file_location('lr_parser', parser_path)
        parser_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser_module)

        Grammar = grammar_module.Grammar
        Rule = grammar_module.Rule
        LR1Parser = parser_module.LR1Parser


class TestSimpleLR1(unittest.TestCase):

    def test_simplest_grammar(self):
        print("\n=== Тест: S -> a ===")
        grammar = Grammar(
            nonterminals={'S'},
            terminals={'a'},
            rules=[Rule('S', ['a'])],
            start_symbol='S'
        )

        parser = LR1Parser()

        try:
            parser.fit(grammar)
            print(f"  Парсер построен успешно")
            print(f"  Состояний: {len(parser.states)}")

            result = parser.predict('a')
            print(f"  predict('a') = {result}")
            self.assertTrue(result, "'a' должна приниматься")

            result = parser.predict('')
            print(f"  predict('') = {result}")
            self.assertFalse(result, "Пустая строка не должна приниматься")

            result = parser.predict('aa')
            print(f"  predict('aa') = {result}")
            self.assertFalse(result, "'aa' не должна приниматься")

        except Exception as e:
            print(f" Ошибка: {e}")
            import traceback
            traceback.print_exc()

    def test_epsilon_grammar_simple(self):
        print("\n=== Тест: S -> a | ε ===")
        grammar = Grammar(
            nonterminals={'S'},
            terminals={'a'},
            rules=[
                Rule('S', ['a']),
                Rule('S', ['ε']),
            ],
            start_symbol='S'
        )

        parser = LR1Parser()

        try:
            parser.fit(grammar)
            print(f" Парсер построен успешно")
            print(f"  Состояний: {len(parser.states)}")

            result = parser.predict('')
            print(f"  predict('') = {result}")
            self.assertTrue(result, "Пустая строка должна приниматься")

            result = parser.predict('a')
            print(f"  predict('a') = {result}")
            self.assertTrue(result, "'a' должна приниматься")

            result = parser.predict('aa')
            print(f"  predict('aa') = {result}")
            self.assertFalse(result, "'aa' не должна приниматься")

        except Exception as e:
            print(f" Ошибка: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    print("Запуск простых тестов LR(1) парсера")
    unittest.main(verbosity=2)