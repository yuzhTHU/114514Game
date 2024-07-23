from typing import List

class Symbol:
    n_operands = None
    def __init__(self, *operands):
        self.operands = operands
        assert len(operands) == self.n_operands
    
    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(self.operands)})'
    
    def __str__(self):
        return self.__repr__()
    
    def eval(self):
        raise NotImplementedError


class Number(Symbol):
    n_operands = 0
    def __init__(self, value):
        self.operands = []
        self.value = value
        assert type(value) == int
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return str(self.value)
    
    def eval(self):
        return self.value


class Empty(Symbol):
    n_operands = 0
    def __init__(self):
        pass
    
    def __repr__(self):
        return f'{self.__class__.__name__}'
    
    def __str__(self):
        return '?'
    
    def eval(self):
        raise ValueError('Incomplete Equation Tree')


class Add(Symbol):
    n_operands = 2
    def __str__(self):
        return f'{self.operands[0]} + {self.operands[1]}'

    def eval(self):
        return self.operands[0].eval() + self.operands[1].eval()


class Sub(Symbol):
    n_operands = 2
    def __str__(self):
        x1, x2 = str(self.operands[0]), str(self.operands[1])
        if self.operands[1].__class__ == Add: x2 = f'({x2})'
        return f'{x1} - {x2}'

    def eval(self):
        return self.operands[0].eval() - self.operands[1].eval()


class Mul(Symbol):
    n_operands = 2
    def __str__(self):
        x1, x2 = str(self.operands[0]), str(self.operands[1])
        if self.operands[0].__class__ in [Add, Sub]: x1 = f'({x1})'
        if self.operands[1].__class__ in [Add, Sub]: x2 = f'({x2})'
        if self.operands[1].__class__ in [Add, Sub]: 
            return f'{x1}{x2}'
        else:
            return f'{x1} * {x2}'
    
    def eval(self):
        return self.operands[0].eval() * self.operands[1].eval()


class Div(Symbol):
    n_operands = 2
    def __str__(self):
        x1, x2 = str(self.operands[0]), str(self.operands[1])
        if self.operands[0].__class__ in [Add, Sub]: x1 = f'({x1})'
        if self.operands[1].__class__ in [Add, Sub, Mul]: x2 = f'({x2})'
        return f'{x1} / {x2}'
    
    def eval(self):
        return self.operands[0].eval() / self.operands[1].eval()


class Cat(Symbol):
    n_operands = 2
    def __init__(self, *operands):
        super().__init__(*operands)
        assert all([type(operand) is Number for operand in operands])

    def __str__(self):
        return f'{self.operands[0]}{self.operands[1]}'

    def eval(self):
        return int(str(self))

class Sin(Symbol):
    n_operands = 1
    def __str__(self):
        return f'sin({self.operands[0]})'

    def eval(self):
        from math import sin
        return sin(self.operands[0].eval())
