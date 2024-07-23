from .env import Iiyokoiyo


def load_env(*args, **kwargs):
    return Iiyokoiyo(*args, **kwargs)


def load_model(name, env:Iiyokoiyo, *args, **kwargs):
    if name == 'GP':
        from .model.gp import GP
        return GP(env, *args, **kwargs)
