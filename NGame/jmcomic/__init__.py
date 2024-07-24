from .env import Jmcomic

def load_env(*args, **kwargs):
    return Jmcomic(*args, **kwargs)

def load_model(name, env:Jmcomic, *args, **kwargs):
    if name == 'GP':
        from .model.gp import GP
        return GP(env, *args, **kwargs)
