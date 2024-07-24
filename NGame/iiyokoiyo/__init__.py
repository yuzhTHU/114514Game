from .env import *

def load_env(*args, **kwargs):
    return Iiyokoiyo(*args, **kwargs)


def load_model(name, env:Iiyokoiyo, *args, **kwargs):
    if name == 'GP':
        from .model.gp import GP
        return GP(env, *args, **kwargs)
    elif name == 'MCTS':
        from .model.mcts import MCTS
        return MCTS(env, *args, **kwargs)