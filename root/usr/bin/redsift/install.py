"""Installer script run by dagger to init the environment.

   For each Python implementation found in the Sift, we are
   looking for a requirements.txt file in the dir of the implementation,
   when a requirements file is found, we are installing the listed
   libraries into a site-packages directory next to the source file.
   This site-packages dir is prepended to the Python path by run.py
   when loading the implementation.
"""
import sys
import json
import os.path
import subprocess

import init

sr = init.env_var_or_exit("SIFT_ROOT")
sj = init.env_var_or_exit("SIFT_JSON")
ir = init.env_var_or_exit("IPC_ROOT")

cache = set()

sift = json.load(open(os.path.join(sr, sj)))
for n in sift["dag"]["nodes"]:
    if "implementation" in n and "python" in n["implementation"]:
        d = os.path.dirname(n["implementation"]["python"])
        poetry_file = os.path.join(sr, d, "pyproject.toml")
        requirements_file = os.path.join(sr, d, "requirements.txt")
        if os.path.exists(poetry_file) and poetry_file not in cache:
            ret = subprocess.check_call(
                [
                    "poetry",
                    "install",
                    "-vvv",
                ],
                cwd=os.path.join(sr, d),
            )
            cache.add(poetry_file)
            if ret != 0:
                print(f"poerty install returned code: {ret}")
                sys.exit(ret)
        elif os.path.exists(requirements_file) and requirements_file not in cache:
            td = os.path.join(sr, d, "site-packages")
            ret = subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--target=" + td,
                    "-r",
                    requirements_file,
                ]
            )
            cache.add(requirements_file)
            if ret != 0:
                print(f"pip install returned code: {ret}")
                sys.exit(ret)
