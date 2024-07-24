import random
from typing import List
from ..env import Iiyokoiyo, Symbol

class Node:
    def __init__(self, content:List[Symbol], parent=None, children=[]):
        self.content = content
        self.parent = parent
        self.children = children
        self.Q = 0
        self.N = 0

    def __repr__(self):
        return "[" + ", ".join(str(i) for i in self.content) + "]"

    def __str__(self):
        x1 = ", ".join(str(i) for i in self.content) 
        x2 = '\n'.join(str(i) for i in self.children)
        return x1 + ('\n    ' + x2.replace('\n', '\n    ') if x2 else '')

    
    
class MCTS:
    """ Monte Carlo Tree Search """
    def __init__(self, env:Iiyokoiyo):
        self.env = env
        self.n_playout = 100
        self.c = 1.41
    
    def solve(self, target:int, n_episode=1000, early_stop:float|None=None, quiet=False):
        self.MC_Tree = Node(self.env.digits)
        self.best = (None, -1)

        for episode in range(1, n_episode+1):
            leaf = self.select(self.MC_Tree)
            expand = self.expand(leaf)
            reward = self.simulate(expand, target)
            self.backpropagate(expand, reward)
            
            if reward > self.best[1]:
                self.best = (expand, reward)
    
            if early_stop is not None and self.best[1] >= early_stop:
                break

            if not quiet and not episode % 500:
                print(f'====== Episode {episode} ======')
                print('{} {}'.format(*self.best))
        return self.best[0].content
    
    def select(self, root:Node):
        node = root
        while node.children:
            node = max(node.children, key=lambda x: x.Q/(x.N+1e-6) + self.c*(2*node.N)**0.5/(1+x.N))
        return node

    def expand(self, node:Node):
        for action in self.env.iter_valid_action(node.content):
            child = Node(self.env.action(node.content, action), node, [])
            node.children.append(child)
        return random.choice(node.children)
    
    def simulate(self, node:Node, target:int):
        rewards = []
        for _ in range(self.n_playout):
            state = self._fill(node.content)
            rewards.append(self.env.reward(state, target))
        return sum(rewards) / len(rewards)

    def backpropagate(self, node:Node, reward:float):
        while node:
            node.N += 1
            node.Q += reward
            node = node.parent

    def _fill(self, state:List[Symbol]):
        while len(state) > 1:
            action = self.env.iter_valid_action(state, shuffle=True).__next__()
            state = self.env.action(state, action)
        return state[0]
