import random

def compute(req):
    if random.random() < 0.08:
        raise Exception('crash')
    return 2
