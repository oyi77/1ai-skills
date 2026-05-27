#!/usr/bin/env python3
"""
Test cases for model router
"""

from router import detect_tier, should_spawn, get_model_for_task

test_cases = [
    # Fast tier
    ("hi there", "fast"),
    ("what's your name?", "fast"),
    ("thanks!", "fast"),
    ("status", "fast"),
    
    # Balanced tier
    ("analyze market summary", "balanced"),
    ("explain this concept", "balanced"),
    ("what is XAUUSD", "balanced"),
    
    # Advanced tier
    ("develop a trading strategy for XAUUSD", "advanced"),
    ("comprehensive analysis of gold market", "advanced"),
    ("create a breakout system", "advanced"),
    
    # Reasoning tier
    ("calculate the expected value", "reasoning"),
    ("step-by-step proof", "reasoning"),
    ("logical puzzle solving", "reasoning"),
    
    # Code tier
    ("fix this Python error", "code"),
    ("write a function to calculate", "code"),
    ("debug this script", "code"),
]

print("🧪 Model Router Test Cases")
print("=" * 60)

for task, expected in test_cases:
    detected = detect_tier(task)
    spawn = should_spawn(task)
    status = "✅" if detected == expected else "❌"
    print(f"{status} Task: '{task[:40]}...' " if len(task) > 40 else f"{status} Task: '{task}' ")
    print(f"    Expected: {expected}, Got: {detected}, Spawn: {spawn}")
    print()

print("=" * 60)
print("All tests completed!")
