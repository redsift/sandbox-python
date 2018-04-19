"""Installer script run by dagger to init the environment.

   For each Python implementation found in the Sift, we are
   looking for a requirements.txt file in the dir of the implementation,
   when a requirements file is found, we are installing the listed
   libraries into a site-packages directory next to the source file.
   This site-packages dir is perpended to the Python path by run.py
   when loading the implementation.
"""
from __future__ import print_function

import json
import os
import os.path

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

import sys

import init

sr = init.env_var_or_exit('SIFT_ROOT')
sj = init.env_var_or_exit('SIFT_JSON')
ir = init.env_var_or_exit('IPC_ROOT')

sift = json.load(open(os.path.join(sr, sj)))
for n in sift['dag']['nodes']:
    if 'implementation' in n and 'python' in n['implementation']:
        d = os.path.dirname(n['implementation']['python'])
        requirements_file = os.path.join(sr, d, 'requirements.txt')
        if os.path.exists(requirements_file):
            td = os.path.join(sr, d, 'site-packages')
            ret = pipmain(['install', '--target='+td, '-r', requirements_file])
            if ret != 0:
                print('pip install returned code: %s' % ret)
                sys.exit(ret)
