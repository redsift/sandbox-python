"""Installer script run by dagger to init the environment.

   For each Python implementation found in the Sift, we are
   looking for a requirements.txt file in the dir of the implementation,
   when a requirements file is found, we are installing the listed
   libraries into a site-packages directory next to the source file.
   This site-packages dir is prepended to the Python path by run.py
   when loading the implementation.
"""

from __future__ import print_function

import init
import json
import os
import os.path
import sys, subprocess


sr = init.env_var_or_exit("SIFT_ROOT")
sj = init.env_var_or_exit("SIFT_JSON")
ir = init.env_var_or_exit("IPC_ROOT")

# Configure token to access github's private repos.
if token := os.environ.get("GITHUB_HTTP_TOKEN"):
    os.system(f'git config --global url."https://{token}:@github.com".insteadOf "https://github.com"')
    os.system(f'git config --global url."https://{token}:@github.com/".insteadOf "git@github.com:"')

with open(os.path.join(sr, sj)) as f:
    sift = json.load(f)

cache = set()

for n in sift["dag"]["nodes"]:
    if "implementation" in n and "python" in n["implementation"]:
        d = os.path.dirname(n["implementation"]["python"])
        requirements_file = os.path.join(sr, d, "requirements.txt")
        if os.path.exists(requirements_file) and requirements_file not in cache:
            td = os.path.join(sr, d, "site-packages")
            ret = subprocess.check_call([sys.executable, "-m", "pip", "install", "--target=" + td, "-r", requirements_file])
            cache.add(requirements_file)
            if ret != 0:
                print("pip install returned code: %s" % ret)
                sys.exit(ret)
