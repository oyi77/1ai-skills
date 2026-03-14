#!/usr/bin/env python3
"""
Interactive helper script for tasks that need input
"""
import sys

print("Interactive helper ready")
print("----------------------------------------")
print("Example usage: script.py --interactive")
print("----------------------------------------")

if "interactive" in sys.argv:
    # Run in interactive mode
    response = input("Enter your input: ")
    print(f"You entered: {response}")
else:
    print("Running in non-interactive mode")