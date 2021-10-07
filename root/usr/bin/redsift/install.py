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
import shutil
import os.path
import subprocess

import init


def install():
    cache = set()
    sift_root = init.env_var_or_exit("SIFT_ROOT")
    sift_json = init.env_var_or_exit("SIFT_JSON")

    sift = json.load(open(os.path.join(sift_root, sift_json)))
    for node in sift["dag"]["nodes"]:
        if "implementation" in node and "python" in node["implementation"]:
            d = os.path.dirname(node["implementation"]["python"])
            poetry_file = os.path.join(sift_root, d, "pyproject.toml")
            if os.path.exists(poetry_file) and poetry_file not in cache:
                ret = subprocess.check_call(
                    [
                        "poetry",
                        "install",
                    ],
                    cwd=os.path.join(sift_root, d),
                )
                cache.add(poetry_file)
                if ret != 0:
                    print(f"poerty install returned code: {ret}")
                    sys.exit(ret)
            requirements_file = os.path.join(sift_root, d, "requirements.txt")
            if os.path.exists(requirements_file) and requirements_file not in cache:
                ret = subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        requirements_file,
                    ]
                )
                cache.add(requirements_file)
                if ret != 0:
                    print(f"pip install returned code: {ret}")
                    sys.exit(ret)

    # Persistence for run.py
    if src := os.environ.get("VIRTUAL_ENV"):
        shutil.copytree(src, os.path.join(sift_root, "venv"))


if __name__ == "__main__":
    install()
