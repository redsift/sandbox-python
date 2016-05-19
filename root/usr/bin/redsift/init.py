import os
import sys

def env_var_or_exit(n):
    v = os.environ.get(n)
    if not v:
        print(n + ' not set')
        sys.exit(1)
    return v
