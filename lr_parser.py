from typing import Dict, Tuple, List, Set, Optional
from collections import deque, defaultdict
from grammar import Grammar, Rule
from lr_item import LRItem, LRState
from first_follow import FirstFollowCalculator


class LR1Parser:
    def __init__(self):
        self.grammar: Optional[Grammar] = None
        self.first_follow: Optional[FirstFollowCalculator] = None
        self.states: List[LRState] = []
        self.action_table: Dict[Tuple[int, str], str] = {}
        self.goto_table: Dict[Tuple[int, str], int] = {}
        self.augmented_start: str = ""

    def fit(self, grammar: Grammar):
        self.grammar = grammar

        if not grammar.validate():
            raise ValueError("Invalid grammar")

        self.first_follow = FirstFollowCalculator(grammar)
        self.first_follow.compute()

        self.augmented_start = f"{grammar.start_symbol}'"

        self._build_canonical_collection()

        self._build_parsing_tables()

        self._check_lr1_conflicts()

    def _build_canonical_collection(self):
        start_rule = Rule(self.augmented_start, [self.grammar.start_symbol])
        start_item = LRItem(start_rule, 0, '$')
        start_state = self._closure({start_item})
        start_state.index = 0
        self.states = [start_state]

        queue = deque([start_state])
        visited = {start_state}

        while queue:
            state = queue.popleft()

            symbols = set()
            for item in state.items:
                next_sym = item.next_symbol()
                if next_sym:
                    symbols.add(next_sym)

            for symbol in symbols:
                new_state = self._goto(state, symbol)

                if new_state and new_state.items:
                    if new_state not in visited:
                        new_state.index = len(self.states)
                        self.states.append(new_state)
                        queue.append(new_state)
                        visited.add(new_state)

                    state_index = new_state.index
                    self.goto_table[(state.index, symbol)] = state_index

    def _closure(self, items: Set[LRItem]) -> LRState:
        closure_set = set(items)
        changed = True

        while changed:
            changed = False
            current_items = list(closure_set)

            for item in current_items:
                next_sym = item.next_symbol()

                if next_sym and self.grammar.is_nonterminal(next_sym):
                    beta = item.rule.rhs[item.dot_pos + 1:] if item.dot_pos + 1 < len(item.rule.rhs) else []

                    first_beta = self._compute_first_of_sequence(beta)

                    lookaheads = set()
                    if 'ε' in first_beta:
                        lookaheads.add(item.lookahead)
                        lookaheads.update(first_beta - {'ε'})
                    else:
                        lookaheads = first_beta - {'ε'}

                    for rule in self.grammar.get_rules_for(next_sym):
                        for lookahead in lookaheads:
                            if not rule.rhs or rule.rhs == ['ε']:
                                new_item = LRItem(rule, 1, lookahead)
                            else:
                                new_item = LRItem(rule, 0, lookahead)

                            if new_item not in closure_set:
                                closure_set.add(new_item)
                                changed = True

        return LRState(closure_set)

    def _compute_first_of_sequence(self, symbols: List[str]) -> Set[str]:
        result = set()

        for symbol in symbols:
            if symbol == 'ε':
                continue

            if self.grammar.is_terminal(symbol):
                result.add(symbol)
                return result

            if symbol in self.first_follow.first:
                first_set = self.first_follow.first[symbol]
                result.update(first_set - {'ε'})

                if 'ε' not in first_set:
                    return result
            else:
                result.add(symbol)
                return result

        result.add('ε')
        return result

    def _goto(self, state: LRState, symbol: str) -> Optional[LRState]:
        kernel_items = set()

        for item in state.items:
            next_sym = item.next_symbol()
            if next_sym == symbol:
                kernel_items.add(item.shift())

        if not kernel_items:
            return None

        return self._closure(kernel_items)

    def _build_parsing_tables(self):
        self.action_table = {}

        temp_goto = {}
        for i, state in enumerate(self.states):
            all_symbols = list(self.grammar.nonterminals | self.grammar.terminals)

            for symbol in all_symbols:
                new_state = self._goto(state, symbol)
                if new_state:
                    for j, existing_state in enumerate(self.states):
                        if existing_state == new_state:
                            temp_goto[(i, symbol)] = j
                            break

        self.goto_table.update(temp_goto)

        for i, state in enumerate(self.states):
            for item in state.items:
                if item.is_complete():
                    if item.rule.lhs == self.augmented_start and item.lookahead == '$':
                        self.action_table[(i, '$')] = 'accept'
                    else:
                        rule_num = self._get_rule_number(item.rule)
                        if rule_num >= 0:
                            self.action_table[(i, item.lookahead)] = f'r{rule_num}'
                else:
                    next_sym = item.next_symbol()
                    if next_sym and self.grammar.is_terminal(next_sym):
                        if (i, next_sym) in self.goto_table:
                            next_state = self.goto_table[(i, next_sym)]
                            self.action_table[(i, next_sym)] = f's{next_state}'

    def _get_rule_number(self, rule: Rule) -> int:
        for i, gr_rule in enumerate(self.grammar.rules):
            if gr_rule.lhs == rule.lhs and gr_rule.rhs == rule.rhs:
                return i
        return -1

    def _check_lr1_conflicts(self):
        conflict_keys = defaultdict(list)

        for key, action in self.action_table.items():
            conflict_keys[key].append(action)

        conflicts = []
        for key, actions in conflict_keys.items():
            if len(actions) > 1:
                has_shift = any(a.startswith('s') for a in actions)
                has_reduce = any(a.startswith('r') for a in actions)
                if has_shift and has_reduce:
                    conflicts.append(f"Shift-reduce conflict on {key}: {actions}")
                elif has_reduce and len([a for a in actions if a.startswith('r')]) > 1:
                    conflicts.append(f"Reduce-reduce conflict on {key}: {actions}")

        if conflicts:
            raise ValueError("\n".join(conflicts))

    def predict(self, word: str) -> bool:
        if not self.grammar:
            raise RuntimeError("Parser not fitted with grammar")

        state_stack = [0]
        symbol_stack = []
        input_tokens = list(word) + ['$']
        input_pos = 0

        while True:
            current_state = state_stack[-1]
            current_symbol = input_tokens[input_pos]

            action_key = (current_state, current_symbol)

            if action_key not in self.action_table:
                return False

            action = self.action_table[action_key]

            if action == 'accept':
                return True

            elif action.startswith('s'):
                next_state = int(action[1:])
                state_stack.append(next_state)
                symbol_stack.append(current_symbol)
                input_pos += 1

            elif action.startswith('r'):
                rule_num = int(action[1:])
                if rule_num < 0 or rule_num >= len(self.grammar.rules):
                    return False

                rule = self.grammar.rules[rule_num]

                if not rule.rhs or rule.rhs == ['ε']:
                    pass
                else:
                    for _ in range(len(rule.rhs)):
                        if not state_stack or not symbol_stack:
                            return False
                        state_stack.pop()
                        symbol_stack.pop()

                lhs = rule.lhs
                symbol_stack.append(lhs)

                # GOTO
                goto_state = state_stack[-1]
                goto_key = (goto_state, lhs)

                if goto_key not in self.goto_table:
                    return False

                next_state = self.goto_table[goto_key]
                state_stack.append(next_state)

            else:
                return False