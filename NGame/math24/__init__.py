from .env import *

def load_env(*args, **kwargs):
    return Math24(*args, **kwargs)


def load_model(name, env:Math24, *args, **kwargs):
    if name == 'GP':
        from .model.gp import GP
        return GP(env, *args, **kwargs)
