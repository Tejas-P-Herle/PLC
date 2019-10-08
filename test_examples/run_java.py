#!/usr/bin/env python3

import os
import sys

filename = sys.argv[1]
os.system("javac " + filename)
os.system("java " + os.path.splitext(filename)[0].title())
