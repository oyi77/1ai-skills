#!/usr/bin/env python3
"""
VILONA WRAPPER - Fix import issue by adding current dir to sys.path
"""

import sys
import os

# Add current directory to sys.path SEBELUM import strategy
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# NOW import and run strategy
if __name__ == "__main__":
    # Import the real strategy
    exec(open("strategy/templates/forex/holy_grail.py").read())
