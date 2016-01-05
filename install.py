"""Installer script run by dagger to init the environment."""

import os
import os.path
import pip


sr = os.environ.get('SIFT_ROOT', '')
requirements_file = os.path.join(sr, 'server/requirements.txt')

if os.path.exists(requirements_file):
    pip.main(['install', '--target='+os.path.join(sr, 'server/site-packages'), '-r', requirements_file])
