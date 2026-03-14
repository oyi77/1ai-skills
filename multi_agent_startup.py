#!/usr/bin/env python3
"""
MULTI-AGENT STARTUP - Auto-Check Parallelization
Auto-executes at start of every session (via SOUL.md)
"""

def check_parallelizable_tasks(tasks):
    """
    Check if tasks can run in parallel

    Returns:
        bool: True if parallelizable, False if sequential
    """
    if not tasks:
        return False

    # Single task = sequential
    if len(tasks) == 1:
        return False

    # Check for dependencies
    dependencies_found = False

    dependency_keywords = [
        'depends on', 'after', 'then', 'next', 'follows',
        'require output from', 'need result from',
        'step 1', 'step 2', 'step 3', 'phase 1', 'phase 2',
        'sequential', 'must be completed first', 'wait for'
    ]

    for task in tasks:
        if isinstance(task, str):
            task_lower = task.lower()
            for keyword in dependency_keywords:
                if keyword in task_lower:
                    dependencies_found = True
                    break
        if dependencies_found:
            break

    # No dependencies = parallelizable
    return not dependencies_found

def calculate_optimal_agent_count(tasks):
    """
    Calculate optimal number of agents for tasks

    Returns:
        int: Optimal agent count
    """
    if not tasks:
        return 0

    # Single task = 1 agent
    if len(tasks) == 1:
        return 1

    # Check if parallelizable
    if not check_parallelizable_tasks(tasks):
        return 1  # Use single agent for sequential

    # Parallelizable = use multiple agents
    # Rule: 1 agent per task, max reasonable limit
    optimal_count = len(tasks)

    # Cap at reasonable number (20)
    MAX_AGENTS = 20
    if optimal_count > MAX_AGENTS:
        optimal_count = MAX_AGENTS

    return optimal_count

def multi_agent_available():
    """
    Check if multi-agent tools are available

    Returns:
        bool: True if multi-agent capability available
    """
    # In OpenClaw environment, multi-agent tools are always available
    # Built-in capabilities:
    # - sessions_spawn: Always available
    # - sessions_send: Always available
    # - subagents: Always available
    # - sessions_list: Always available
    # - sessions_history: Always available

    return True

def recommend_parallelization(tasks, task_description=""):
    """
    Recommend parallelization strategy for tasks

    Args:
        tasks: List of task descriptions
        task_description: Overall task description

    Returns:
        dict: Recommendation with strategy and reasoning
    """
    if not tasks:
        return {
            "recommendation": "no_tasks",
            "parallelizable": False,
            "agent_count": 0,
            "reasoning": "No tasks to analyze"
        }

    is_parallelizable = check_parallelizable_tasks(tasks)
    optimal_count = calculate_optimal_agent_count(tasks)

    recommendation = {
        "parallelizable": is_parallelizable,
        "agent_count": optimal_count,
        "available": multi_agent_available()
    }

    if is_parallelizable and optimal_count > 1:
        recommendation["recommendation"] = "parallel"
        recommendation["reasoning"] = f"""
        Tasks are independent and can run in parallel.
        Recommended: Spawn {optimal_count} parallel agents.
        Expected speedup: {optimal_count}x faster than sequential.
        """
    else:
        recommendation["recommendation"] = "sequential"
        if not is_parallelizable:
            recommendation["reasoning"] = """
            Tasks have dependencies and need sequential execution.
            Recommended: Use single agent with sequential task flow.
            """
        else:
            recommendation["reasoning"] = """
            Single task or sequential dependencies.
            Recommended: Single agent execution.
            """

    # Add crisis mode context if applicable
    if task_description and "crisis" in task_description.lower():
        if is_parallelizable:
            recommendation["crisis_mode"] = "ALWAYS parallelize in crisis"
        else:
            recommendation["crisis_mode"] = "Sequential required, but optimize"

    return recommendation

# Global auto-executed function
def auto_check_parallelization(tasks, task_description=""):
    """
    Auto-check and log recommendation for parallelization

    This function is called automatically at session start via SOUL.md

    Usage:
        tasks = ["Task A", "Task B", "Task C"]
        recommendation = auto_check_parallelization(tasks, "Morning automation")

        if recommendation["parallelizable"]:
            # Spawn parallel agents
            for task in tasks:
                sessions_spawn(task=task, runtime="subagent")
        else:
            # Use single agent
            sessions_spawn(task="\n".join(tasks), runtime="subagent")
    """
    recommendation = recommend_parallelization(tasks, task_description)

    # Log recommendation (in real implementation)
    # print(f"[MULTI-AGENT CHECK] Recommendation: {recommendation['recommendation']}")
    # print(f"[MULTI-AGENT CHECK] Parallelizable: {recommendation['parallelizable']}")
    # print(f"[MULTI-AGENT CHECK] Agent Count: {recommendation['agent_count']}")

    return recommendation

# Export functions for global use
__all__ = [
    'check_parallelizable_tasks',
    'calculate_optimal_agent_count',
    'multi_agent_available',
    'recommend_parallelization',
    'auto_check_parallelization'
]

# Auto-check on module load (optional, can be called manually)
# if __name__ != "__main__":
#     print("[MULTI-AGENT STARTUP] Multi-agent capability initialized")
#     print("[MULTI-AGENT STARTUP] Use auto_check_parallelization() for task analysis")