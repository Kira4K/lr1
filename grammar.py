from dataclasses import dataclass
from typing import List, Set, Dict
from collections import defaultdict


@dataclass(frozen=True)
class Rule:
    lhs: str
    rhs: List[str]

    def __str__(self) -> str:
        return f"{self.lhs} -> {''.join(self.rhs) if self.rhs else 'ε'}"

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs)))


class Grammar:
    def __init__(self, nonterminals: Set[str], terminals: Set[str],
                 rules: List[Rule], start_symbol: str):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol
        self._rules_by_lhs: Dict[str, List[Rule]] = defaultdict(list)

        for rule in rules:
            self._rules_by_lhs[rule.lhs].append(rule)

    def get_rules_for(self, nonterminal: str) -> List[Rule]:
        return self._rules_by_lhs.get(nonterminal, [])

    def is_nonterminal(self, symbol: str) -> bool:
        return symbol in self.nonterminals

    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.terminals

    def validate(self) -> bool:
        if self.start_symbol not in self.nonterminals:
            return False
        if self.nonterminals & self.terminals:
            return False
        return True

    def __str__(self) -> str:
        rules_str = '\n'.join(str(rule) for rule in self.rules)
        return f"Grammar(S={self.start_symbol}, rules={len(self.rules)})\n{rules_str}"