import os
import sys


def env_var_or_exit(n):
    if v := os.environ.get(n):
        return v
    print(f"{n} not set")
    sys.exit(1)
