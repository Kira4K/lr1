import sys
from typing import Tuple, List
from grammar import Grammar, Rule


class GrammarParser:
    @staticmethod
    def parse_from_stdin() -> Tuple[Grammar, List[str]]:
        """Парсинг грамматики из stdin в формате задания."""
        lines = [line.strip() for line in sys.stdin if line.strip()]

        if not lines:
            raise ValueError("Empty input")

        # Парсинг размеров
        try:
            n_nt, n_t, n_rules = map(int, lines[0].split())
        except ValueError:
            raise ValueError("Invalid format in first line")

        # Нетерминалы
        nonterminals = set(lines[1].split())
        if len(nonterminals) != n_nt:
            raise ValueError(f"Expected {n_nt} nonterminals, got {len(nonterminals)}")

        # Терминалы
        terminals = set(lines[2].split())
        if len(terminals) != n_t:
            raise ValueError(f"Expected {n_t} terminals, got {len(terminals)}")

        rules = []
        rule_lines = lines[3:3 + n_rules]

        for rule_line in rule_lines:
            if '->' not in rule_line:
                raise ValueError(f"Invalid rule format: {rule_line}")

            lhs, rhs_str = rule_line.split('->', 1)
            lhs = lhs.strip()
            rhs_str = rhs_str.strip()

            if rhs_str == '':
                rhs = ['ε']
            else:
                rhs = list(rhs_str.replace(' ', ''))

            rules.append(Rule(lhs, rhs))

        start_symbol = lines[3 + n_rules].strip()

        try:
            m = int(lines[3 + n_rules + 1])
        except ValueError:
            raise ValueError("Invalid number of words")

        words = lines[3 + n_rules + 2:3 + n_rules + 2 + m]

        grammar = Grammar(nonterminals, terminals, rules, start_symbol)

        if not grammar.validate():
            raise ValueError("Invalid grammar")

        return grammar, words