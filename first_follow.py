from typing import Dict, Set, List
from grammar import Grammar


class FirstFollowCalculator:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first: Dict[str, Set[str]] = {}
        self.follow: Dict[str, Set[str]] = {}

    def compute(self):
        self._compute_first()
        self._compute_follow()

    def _compute_first(self):
        for nt in self.grammar.nonterminals:
            self.first[nt] = set()
        for t in self.grammar.terminals:
            self.first[t] = {t}

        if 'ε' not in self.first:
            self.first['ε'] = {'ε'}

        changed = True
        while changed:
            changed = False

            for rule in self.grammar.rules:
                lhs = rule.lhs

                if not rule.rhs or (len(rule.rhs) == 1 and rule.rhs[0] == 'ε'):
                    if 'ε' not in self.first[lhs]:
                        self.first[lhs].add('ε')
                        changed = True
                    continue

                all_epsilon = True
                for symbol in rule.rhs:
                    if symbol == 'ε':
                        continue

                    if symbol in self.grammar.terminals:
                        to_add = {symbol}
                        if to_add - self.first[lhs]:
                            self.first[lhs].update(to_add)
                            changed = True
                        all_epsilon = False
                        break

                    if symbol in self.first:
                        to_add = self.first[symbol] - {'ε'}
                        if to_add - self.first[lhs]:
                            self.first[lhs].update(to_add)
                            changed = True

                        if 'ε' not in self.first[symbol]:
                            all_epsilon = False
                            break

                if all_epsilon and 'ε' not in self.first[lhs]:
                    self.first[lhs].add('ε')
                    changed = True

    def _compute_follow(self):
        for nt in self.grammar.nonterminals:
            self.follow[nt] = set()

        self.follow[self.grammar.start_symbol].add('$')

        changed = True
        while changed:
            changed = False

            for rule in self.grammar.rules:
                rhs = rule.rhs

                if not rhs or (len(rhs) == 1 and rhs[0] == 'ε'):
                    continue

                for i in range(len(rhs)):
                    symbol = rhs[i]

                    if not self.grammar.is_nonterminal(symbol):
                        continue

                    if i + 1 < len(rhs):
                        remaining = rhs[i + 1:]
                        first_of_remaining = self._first_of_string(remaining)

                        to_add = first_of_remaining - {'ε'}
                        if to_add - self.follow[symbol]:
                            self.follow[symbol].update(to_add)
                            changed = True

                        if 'ε' in first_of_remaining:
                            to_add = self.follow[rule.lhs] - self.follow[symbol]
                            if to_add:
                                self.follow[symbol].update(to_add)
                                changed = True
                    else:
                        to_add = self.follow[rule.lhs] - self.follow[symbol]
                        if to_add:
                            self.follow[symbol].update(to_add)
                            changed = True

    def _first_of_string(self, symbols: List[str]) -> Set[str]:
        if not symbols:
            return {'ε'}

        result = set()

        for symbol in symbols:
            if symbol == 'ε':
                continue

            if symbol in self.grammar.terminals:
                result.add(symbol)
                return result

            if symbol in self.first:
                result.update(self.first[symbol] - {'ε'})

                if 'ε' not in self.first[symbol]:
                    return result
            else:
                return result

        result.add('ε')
        return result

    def get_first(self, symbol: str) -> Set[str]:
        if symbol in self.first:
            return self.first[symbol]
        elif symbol in self.grammar.terminals:
            return {symbol}
        else:
            return set()

    def get_follow(self, nonterminal: str) -> Set[str]:
        return self.follow.get(nonterminal, set())