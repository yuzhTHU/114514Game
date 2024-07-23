import random
from typing import List, Tuple
from ..eqtree import *


class Iiyokoiyo:
    """ 向 114514 中插入数学符号以拟合目标值，如 (1 + 14) * 514 = 7710 """
    def __init__(self, symbols:List[Symbol]=[Add, Sub, Mul, Div, Cat], digits:List[int]=[1,1,4,5,1,4]):
        self.digits = [Number(i) for i in digits]
        self.symbols = symbols
        self.id2sym = [sym.__name__ for sym in symbols]
        self.sym2id = {sym:idx for idx, sym in enumerate(self.id2sym)}

    def check_valid_action(self, state:List[Symbol], action:Tuple[Symbol, int]):
        sym, idx = action
        if sym.n_operands == 0: 
            return False
        elif sym.n_operands == 1:
            if not (0 <= idx < len(state)): return False
        elif sym.n_operands == 2:
            if not (0 <= idx < len(state)-1): return False
            if sym is Div and state[idx+1].eval() == 0: return False
            if sym is Cat and not (state[idx].__class__ is Number and 
                                   state[idx+1].__class__ is Number): return False
        else:
            return False
        return True

    def iter_valid_action(self, state:List[Symbol], shuffle=False):
        sym_loader = self.symbols.copy()
        idx_loader = list(range(len(state)))
        if shuffle: 
            random.shuffle(sym_loader)
            random.shuffle(idx_loader)
        for sym in sym_loader:
            for idx in idx_loader:
                if self.check_valid_action(state, (sym, idx)):
                    yield sym, idx

    def action(self, state:List[Symbol], action:Tuple[Symbol, int]):
        sym, idx = action
        state = state.copy()
        if sym.n_operands == 1: state[idx] = sym(state[idx])
        if sym.n_operands == 2: state[idx] = sym(state[idx], state.pop(idx+1))
        return state
        
    def reward(self, state:List[Symbol], target:int):
        if type(state) is not list: state = [state]
        if len(state) != 1: 
            return 0
        else: 
            diff = abs(state[0].eval() - target)
            return 1/(1+diff)
        
