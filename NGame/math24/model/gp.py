import random
from typing import List
from ..env import Math24, Symbol, IndexedNumber


class GP:
    """ Genetic Programming """
    def __init__(self, env:Math24):
        self.env = env
        self.n_population = 100
        self.n_cross = 100
        self.n_mutate = 100
        self.n_keep = 50
    
    def solve(self, target:int, n_episode=1000, early_stop=False, quiet=False):
        self.population = self.init()
        self.best = (None, -1)

        for episode in range(1, n_episode+1):
            children = []

            for _ in range(self.n_cross):
                a = random.choice(self.population)
                b = random.choice(self.population)
                c = self.cross(a, b)
                children.append(c)
            
            for _ in range(self.n_mutate):
                a = random.choice(self.population)
                b = self.mutate(a)
                children.append(b)

            self.population = children + self.population[:self.n_keep]
            self.population = sorted(self.population, key=lambda x: self.env.reward(x, target), reverse=True)
            self.population = self.population[:self.n_population]

            best = self.env.reward(self.population[0], target)
            if best > self.best[1]: 
                self.best = (self.population[0], best)

            if early_stop and (self.population[0].eval() == target):
                break

            if not quiet and not episode % 10:
                print(f'====== Episode {episode} ======')
                for x in self.population:
                    print('{2:6.1%} {1:.4f} = {0}'.format(x, x.eval(), self.env.reward(x, target)))
        return self.best[0]

    def init(self, n_population=100):
        population = [self._fill(self.env.digits) for _ in range(n_population)]
        return population

    def cross(self, a:Symbol, b:Symbol):
        gene_a = [random.choice(self._break(a))]
        indexes = [x.idx for gene in gene_a for x in gene.preorder() if x.__class__ is IndexedNumber]
        assert len(indexes) == len(set(indexes))
        def foo(root):
            if root.__class__ is IndexedNumber:
                if root.idx not in indexes:
                    return [root], True
                else:
                    return [], False
            alleqtrees = []
            allflag = True
            for i in root.operands:
                eqtrees, flag = foo(i)
                alleqtrees += eqtrees
                allflag &= flag
            if allflag: return [root], True
            else: return alleqtrees, False
        gene_b = foo(b)[0]
        return self._fill(gene_a + gene_b)

    def mutate(self, a:Symbol):
        eqtrees = self._break(a)
        return self._fill(eqtrees)

    def _fill(self, eqtrees:List[Symbol]):
        while len(eqtrees) > 1:
            action = self.env.iter_valid_action(eqtrees, shuffle=True).__next__()
            eqtrees = self.env.action(eqtrees, action)
        return eqtrees[0]

    def _break(self, eqtree:Symbol) -> List[Symbol]:
        def foo(root, route=[]):
            if root.n_operands: yield [*route, root]
            for i in root.operands:
                yield from foo(i, [*route, root])
        route = random.choice(list(foo(eqtree))) # select route from root to random inner node
        def foo2(root):
            if root in route:
                for i in root.operands: yield from foo2(i)
            else:
                yield root
        eqtrees = list(foo2(eqtree)) # remove nodes in the route
        return eqtrees