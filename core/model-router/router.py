#!/usr/bin/env python3
"""
Model Router - Intelligent task routing for optimal model selection
"""

import re
import sys
from typing import Optional, Dict, List

# Model tier configuration
MODEL_TIERS = {
    "fast": "nvidia/meta/llama-3.2-1b-instruct",
    "balanced": "nvidia/minimaxai/minimax-m2.1", 
    "advanced": "nvidia/moonshotai/kimi-k2.5",
    "reasoning": "nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b",
    "code": "nvvidia/qwen/qwen2.5-coder-32b-instruct"
}

# Task patterns for auto-detection
TASK_PATTERNS = {
    "fast": [
        r"^(hi|hello|hey)",
        r"^how are you",
        r"^what('s| is) your name",
        r"^(ok|okay|thanks|thank you)",
        r"^(yes|no|maybe)$",
        r"^status",
        r"^help$",
    ],
    "balanced": [
        r"(analyze|analysis).*(summary|overview)",
        r"(explain|tell me about).*(concept|topic)",
        r"(what|how).*(is|are|does).*(work|function)",
        r"(market|price).*(update|status)",
        r"(compare|contrast).*(simple|brief)",
    ],
    "advanced": [
        r"(develop|create|build).*(strategy|plan|system)",
        r"(detailed|comprehensive|deep).*(analysis|review)",
        r"(trading|investment).*(strategy|approach|method)",
        r"(multi-step|complex|sophisticated)",
        r"(backtest|optimize).*(performance|strategy)",
        r"XAUUSD.*(breakout|strategy|analysis)",
    ],
    "reasoning": [
        r"(prove|proof|demonstrate).*(theorem|concept)",
        r"(calculate|compute).*(complex|difficult)",
        r"(logic|logical|reasoning).*(puzzle|problem)",
        r"(mathematical|mathematics|math).*(problem|proof)",
        r"(step-by-step|detailed reasoning)",
    ],
    "code": [
        r"(fix|debug|optimize).*(code|script|program)",
        r"(write|create).*(function|script|program|code)",
        r"(Python|JavaScript|TypeScript|C\+\+|Java|Go|Rust).*(code|script)",
        r"(error|bug|exception|traceback)",
        r"(refactor|rewrite).*(code|function|class)",
        r"(implement|build).*(feature|solution)",
        r"```.*```",  # Code blocks
    ]
}

# ⚡ Bolt Optimization: Pre-compile regex patterns to avoid recompilation on every call
COMPILED_PATTERNS = {
    tier: [re.compile(p, re.IGNORECASE) for p in patterns]
    for tier, patterns in TASK_PATTERNS.items()
}


def detect_tier(task: str) -> str:
    """Detect the appropriate model tier based on task content."""
    task_lower = task.lower()
    
    # Check from most complex to simplest
    for tier in ["reasoning", "code", "advanced", "balanced", "fast"]:
        for pattern in COMPILED_PATTERNS.get(tier, []):
            if pattern.search(task_lower):
                return tier
    
    # Default to fast for simple queries
    return "balanced"


def format_spawn_command(task: str, tier: str, timeout: int = 120) -> str:
    """Generate subagent spawn command."""
    model = MODEL_TIERS.get(tier, MODEL_TIERS["balanced"])
    
    # Create a focused task description
    task_clean = task.strip().replace('"', '\\"')
    
    return f'''sessions_spawn(task="{task_clean}", model="{model}", runTimeoutSeconds={timeout})'''


def should_spawn(task: str) -> bool:
    """Determine if task should spawn a subagent."""
    tier = detect_tier(task)
    # Only spawn for balanced and above
    return tier in ["balanced", "advanced", "reasoning", "code"]


def get_model_for_task(task: str) -> tuple[str, str]:
    """Get appropriate model and tier for task."""
    tier = detect_tier(task)
    model = MODEL_TIERS.get(tier, MODEL_TIERS["balanced"])
    return tier, model


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: router.py <task> [--model tier] [--timeout seconds]")
        sys.exit(1)
    
    task = sys.argv[1]
    
    # Parse args
    specified_tier = None
    timeout = 120
    
    for i, arg in enumerate(sys.argv):
        if arg == "--model" and i + 1 < len(sys.argv):
            specified_tier = sys.argv[i + 1]
        if arg == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1])
    
    # Determine tier
    if specified_tier:
        tier = specified_tier if specified_tier in MODEL_TIERS else "balanced"
    else:
        tier = detect_tier(task)
    
    # Output result
    print(f"TIER: {tier}")
    print(f"MODEL: {MODEL_TIERS[tier]}")
    print(f"SPAWN: {should_spawn(task)}")
    print(f"COMMAND: {format_spawn_command(task, tier, timeout)}")


if __name__ == "__main__":
    main()
