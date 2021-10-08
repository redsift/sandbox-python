"""Installer script run by dagger to init the environment.

   For each Python implementation found in the Sift, we are
   looking for a requirements.txt file in the dir of the implementation,
   when a requirements file is found, we are installing the listed
   libraries into a site-packages directory next to the source file.
   This site-packages dir is prepended to the Python path by run.py
   when loading the implementation.
"""
import os
import sys
import json
import uuid
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
            td = os.path.join(sift_json, d, "site-packages")
            if os.path.exists(poetry_file) and poetry_file not in cache:
                temp_file = f"/tmp/requirements_{uuid.uuid4()}.txt"
                ret = subprocess.check_call(
                    [
                        "/home/sandbox/.poetry/bin/poetry",
                        "export",
                        "-f",
                        "requirements.txt",
                        "--without-hashes",
                        "-o",
                        temp_file,
                    ],
                    cwd=os.path.join(sift_root, d),
                )
                if ret != 0:
                    print(f"poerty install returned code: {ret}")
                    sys.exit(ret)
                ret = subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--target=" + td,
                        "-r",
                        temp_file,
                    ]
                )
                if ret != 0:
                    print(f"pip install returned code: {ret}")
                    sys.exit(ret)
                os.unlink(temp_file)
                cache.add(poetry_file)
            requirements_file = os.path.join(sift_root, d, "requirements.txt")
            if os.path.exists(requirements_file) and requirements_file not in cache:
                ret = subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--target=" + td,
                        "-r",
                        requirements_file,
                    ],
                )
                cache.add(requirements_file)
                if ret != 0:
                    print(f"pip install returned code: {ret}")
                    sys.exit(ret)


if __name__ == "__main__":
    install()
