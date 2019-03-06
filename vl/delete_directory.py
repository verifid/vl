#!/usr/bin/env python3

import shutil
import os

directory = os.getcwd() + '/testsets/'
if os.path.exists(directory) and os.path.isdir(directory):
    shutil.rmtree(directory)
