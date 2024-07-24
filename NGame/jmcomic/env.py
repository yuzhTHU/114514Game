import random
from typing import List, Tuple
from ..eqtree import *

class Equal(Symbol):
    n_operands = 2
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.operands[0]}, {self.operands[1]})'

    def __str__(self):
        return f'{self.operands[0]} = {self.operands[1]}'
    
    def eval(self, res=False):
        x1, x2 = self.operands[0].eval(), self.operands[1].eval()
        if res: return x1 - x2
        else: return x1 == x2


class Jmcomic:
    """ 向一串数字（如 123456）中添加包含=的数学符号，使得等式成立 """
    def __init__(self, symbols:List[Symbol]=[Add, Sub, Mul, Div, Cat, Equal], digits:List[int]=[1,2,3,4,5,6]):
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
            if sym is Ln and state[idx].eval() <= 0: return False
            if sym is Sqrt and state[idx].eval() < 0: return False
        elif sym.n_operands == 2:
            if not (0 <= idx < len(state)-1): return False
            if sym is Div and state[idx+1].eval() == 0: return False
            if sym is Cat and not (state[idx].__class__ is Number and 
                                   state[idx+1].__class__ is Number): return False
            if sym is Pow and (state[idx].eval() < 0 and state[idx+1].eval() != 0): return False
            if sym is Pow and (state[idx].eval() == 0 and state[idx+1].eval() <= 0): return False
            if sym is Pow and state[idx+1].eval() > 30: return False
            if (sym is Equal) ^ (len(state) == 2): return False
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
        
    def reward(self, state:Symbol|List[Symbol]):
        if type(state) is list:
            assert len(state) == 1
            state = state[0]
        if state.__class__ is not Equal: return 0
        diff = abs(state.eval(res=True))
        return 1/(1+diff)
