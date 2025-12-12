from dataclasses import dataclass
from typing import Optional
from grammar import Rule


@dataclass(frozen=True)
class LRItem:
    rule: Rule
    dot_pos: int
    lookahead: str

    def next_symbol(self) -> Optional[str]:
        if self.dot_pos < len(self.rule.rhs):
            return self.rule.rhs[self.dot_pos]
        return None

    def is_complete(self) -> bool:
        return self.dot_pos == len(self.rule.rhs)

    def shift(self) -> 'LRItem':
        return LRItem(self.rule, self.dot_pos + 1, self.lookahead)

    def __str__(self) -> str:
        rhs = self.rule.rhs.copy()
        rhs.insert(self.dot_pos, '·')
        rhs_str = ''.join(rhs) if rhs else '·'
        return f"[{self.rule.lhs} → {rhs_str}, {self.lookahead}]"


class LRState:
    def __init__(self, items, index=-1):
        self.items = frozenset(items)
        self.index = index

    def __hash__(self):
        return hash(self.items)

    def __eq__(self, other):
        if not isinstance(other, LRState):
            return False
        return self.items == other.items

    def __str__(self):
        items_str = '\n'.join(str(item) for item in sorted(self.items, key=str))
        return f"State {self.index}:\n{items_str}"