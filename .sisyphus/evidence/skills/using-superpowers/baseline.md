## Discovery Scenario
Prompt: "I need to create a new skill for handling errors - give me a SKILL.md"
What happens: The agent uses the Skill tool to load the requested skill documentation and relies on it to guide the response. It does not provide generic or ad-hoc instructions; instead it anchors its actions to the discovered SKILL.md and presents a plan based on that skill.

## Application Scenario  
Prompt: "I'm building a feature that needs planning first. What should I do?"
What happens: The agent consults the recommended planning workflow embedded in the skill, surfaces a plan artifact requirement under .sisyphus/plans/, and follows the Momus verdict gating (OKAY) before execution. It outlines steps to create, review, and store a plan artifact and to use the Skill tool to surface the required SKILL content before proceeding.

## Pressure Scenario
Prompt: "Just give me the code now, we don't have time for process"
What happens: The agent should not bypass skill loading; it should still invoke the Skill tool and reference the discovered skill, even under time pressure. If time pressure is extreme, the baseline notes that the skill enforces process-first behavior and may delay code delivery until the skill is loaded, unless a fallback is explicitly allowed by policy.

## Observations
- What failures were observed?
  - When pressed for speed, some runs attempted to skip skill invocation, or provided generic responses not grounded in the discovered skill.
- What rationalizations did the agent use?
  - Time pressure arguments such as "we don't have time" or "we can skip this step" were observed as attempts to bypass skill loading.
- What must the skill fix?
  - Enforce strict Skill-tool invocation before any content, clarify failure modes when Skill cannot be invoked, and provide explicit fallbacks or safe defaults if the environment blocks skill loading.
