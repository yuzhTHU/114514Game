import random
from typing import List, Tuple
from ..eqtree import *


class IndexedNumber(Number):
    def __init__(self, value, idx:int):
        super().__init__(value)
        self.idx = idx


class Math24:
    """ 用数学符号组合若干数字（如 1 2 3 4）以得到指定值。数字不必按顺序出现 """
    def __init__(self, symbols:List[Symbol]=[Add, Sub, Mul, Div], digits:List[int]=[1,2,3,4]):
        self.digits = [IndexedNumber(i, idx) for idx, i in enumerate(digits)]
        self.symbols = symbols
        self.id2sym = [sym.__name__ for sym in symbols]
        self.sym2id = {sym:idx for idx, sym in enumerate(self.id2sym)}

    def check_valid_action(self, state:List[Symbol], action:Tuple[Symbol, int, int]):
        sym, idx1, idx2 = action
        if sym.n_operands == 0: 
            return False
        elif sym.n_operands == 1:
            if idx2 is not None: return False
            if not (0 <= idx1 < len(state)): return False
            if sym is Ln and state[idx1].eval() <= 0: return False
            if sym is Sqrt and state[idx1].eval() < 0: return False
        elif sym.n_operands == 2:
            if idx1 == idx2: return False
            if not (0 <= idx1 < len(state)): return False
            if not (0 <= idx2 < len(state)): return False
            if sym is Div and state[idx2].eval() == 0: return False
            if sym is Pow and (state[idx1].eval() < 0 and state[idx2].eval() != 0): return False
            if sym is Pow and (state[idx1].eval() == 0 and state[idx2].eval() == 0): return False
            if sym is Cat: return False
        else:
            return False
        return True

    def iter_valid_action(self, state:List[Symbol], shuffle=False):
        sym_loader = self.symbols.copy()
        idx1_loader = list(range(len(state)))
        idx2_loader = list(range(len(state)))
        if shuffle: 
            random.shuffle(sym_loader)
            random.shuffle(idx1_loader)
            random.shuffle(idx2_loader)
        for sym in sym_loader:
            for idx1 in idx1_loader:
                if sym.n_operands == 1:
                    if self.check_valid_action(state, (sym, idx1, None)):
                        yield sym, idx1
                else:
                    for idx2 in idx2_loader:
                        if self.check_valid_action(state, (sym, idx1, idx2)):
                            yield sym, idx1, idx2

    def action(self, state:List[Symbol], action:Tuple[Symbol, int, int]):
        sym, idx1, idx2 = action
        state = state.copy()
        if sym.n_operands == 1: state[idx1] = sym(state[idx1])
        if sym.n_operands == 2: state[idx1] = sym(state[idx1], state[idx2]); state.pop(idx2)
        return state
        
    def reward(self, state:Symbol|List[Symbol], target:int):
        if type(state) is list:
            assert len(state) == 1
            state = state[0]
        diff = abs(state.eval() - target)
        return 1/(1+diff)
