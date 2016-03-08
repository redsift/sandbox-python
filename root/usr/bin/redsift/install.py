"""Installer script run by dagger to init the environment.

   For each Python implementation found in the Sift, we are
   looking for a requirements.txt file in the dir of the implementation,
   when a requirements file is found, we are installing the listed
   libraries into a site-packages directory next to the source file.
   This site-packages dir is perpended to the Python path by bootstrap.py
   when loading the implementation.
"""

import json
import os
import os.path
import pip


sr = os.environ.get('SIFT_ROOT', '')
sift = json.load(open(os.path.join(sr, 'sift.json')))
for n in sift['dag']['nodes']:
    if 'implementation' in n and 'python' in n['implementation']:
        d = os.path.dirname(n['implementation']['python'])
        requirements_file = os.path.join(sr, d, 'requirements.txt')
        if os.path.exists(requirements_file):
            td = os.path.join(sr, d, 'site-packages')
            pip.main(['install', '--target='+td, '-r', requirements_file])
