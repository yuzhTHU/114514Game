from .symbols import *
from typing import List

def prefix2eqtree(prefix:List[str]):
    def foo(idx):
        item, idx = eval(prefix[idx]), idx+1
        operands = []
        if type(item) == int: 
            operands, item = [item], Number
    
        for _ in range(item.n_operands):
            operand, idx = foo(idx)
            operands.append(operand)
        return item(*operands), idx

    eqtree, idx = foo(0)
    assert idx == len(prefix)
    return eqtree
