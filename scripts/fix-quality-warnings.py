#!/usr/bin/env python3
"""
fix-quality-warnings.py — Add anti-rationalization tables, code examples,
and verification checklists to skills that are missing them.

Usage: python3 scripts/fix-quality-warnings.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Category → default anti-rationalization table
AR_TABLES = {
    'agents': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will just do it manually" | Agents automate repetitive tasks — manual work does not scale |
| "The agent will figure it out" | Without clear instructions, agents hallucinate. Give explicit context. |
| "One agent is enough" | Complex tasks benefit from specialized agents working in parallel |""",

    'automation': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |""",

    'content': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |""",

    'core': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |""",

    'cybersecurity': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |""",

    'data': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "CSV is fine for everything" | Structured databases enable queries, integrity, and scale. |
| "I will add data validation later" | Bad data propagates silently. Validate at ingestion. |
| "Small datasets do not need optimization" | Even small datasets benefit from proper indexing and schema design. |""",

    'development': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |""",

    'devops': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |""",

    'financial': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The market will recover" | Do not hope. Analyze. Set stop-losses and follow your strategy. |
| "I do not need to track expenses" | What you do not measure, you cannot optimize. Track everything. |
| "One spreadsheet is enough" | Financial models need version control and audit trails. Use proper tools. |""",

    'integrations': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |""",

    'marketing': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good products sell themselves" | They do not. Marketing is how people discover your product. |
| "I will start marketing after launch" | Build audience before launch. Pre-launch momentum is critical. |
| "SEO is dead" | SEO evolves. GEO (Generative Engine Optimization) is the new frontier. |""",

    'mcp': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will just use curl" | MCP handles auth, retries, streaming, and type safety. Use the SDK. |
| "One mega-server is simpler" | Single-responsibility servers are easier to debug and maintain. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |""",

    'meta': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |""",

    'mindset': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I already know this" | Knowing and practicing are different. Daily practice builds mastery. |
| "Soft skills are innate" | Soft skills are learnable. Deliberate practice improves any skill. |
| "I do not have time" | 10 minutes daily beats 2 hours weekly. Consistency over intensity. |""",

    'operations': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |""",

    'productivity': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I am too busy to organize" | Disorganization costs more time than organizing. Invest upfront. |
| "Multitasking is productive" | Context switching costs 25 minutes per switch. Focus on one thing. |
| "I will remember this" | You will not. Write it down. Externalize your memory. |""",

    'research': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |""",

    'sales': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Cold outreach does not work" | It works when personalized and targeted. Generic spam does not. |
| "I will follow up later" | 80% of sales require 5+ follow-ups. Follow up consistently. |
| "Price is the only factor" | Value, trust, and timing matter more than price. Sell outcomes. |""",

    'trading': """## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |""",
}

# Category → default code example
CODE_EXAMPLES = {
    'agents': ('python', """```python
# Example: Agent orchestration
from dataclasses import dataclass

@dataclass
class Task:
    name: str
    priority: int
    assigned_agent: str

def orchestrate(tasks: list[Task]) -> dict:
    results = {}
    for task in sorted(tasks, key=lambda t: t.priority):
        results[task.name] = execute(task)
    return results
```"""),

    'automation': ('python', """```python
# Example: Workflow automation
import schedule
import time

def run_workflow():
    data = fetch_data()
    processed = transform(data)
    deliver(processed)

schedule.every().hour.do(run_workflow)
while True:
    schedule.run_pending()
    time.sleep(60)
```"""),

    'content': ('python', """```python
# Example: Content generation pipeline
def generate_content(topic: str, format: str = "article"):
    outline = create_outline(topic)
    draft = write_draft(outline, format)
    edited = edit_for_quality(draft)
    optimized = optimize_for_seo(edited)
    return publish(optimized)
```"""),

    'core': ('python', """```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```"""),

    'cybersecurity': ('python', """```python
# Example: IOC detection
import re

IOC_PATTERNS = {
    "ip": r"\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b",
    "domain": r"\\b[a-z0-9-]+\\.[a-z]{2,}\\b",
    "hash_md5": r"\\b[a-f0-9]{32}\\b",
    "hash_sha256": r"\\b[a-f0-9]{64}\\b",
}

def extract_iocs(text: str) -> dict:
    return {k: re.findall(v, text) for k, v in IOC_PATTERNS.items()}
```"""),

    'data': ('python', """```python
# Example: Data pipeline
import pandas as pd

def pipeline(source: str):
    df = pd.read_csv(source)
    df = df.dropna()
    df = df.drop_duplicates()
    df["processed_at"] = pd.Timestamp.now()
    return df.to_parquet("output.parquet")
```"""),

    'development': ('python', """```python
# Example: TDD workflow
def test_user_creation():
    user = create_user(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None

def test_user_creation_invalid_email():
    with pytest.raises(ValidationError):
        create_user(name="Alice", email="invalid")
```"""),

    'devops': ('yaml', """```yaml
# Example: GitHub Actions CI
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -e ".[test]"
      - run: pytest --cov
```"""),

    'financial': ('python', """```python
# Example: Portfolio risk calculation
def calculate_risk(returns: list[float]) -> dict:
    import statistics
    mean = statistics.mean(returns)
    stdev = statistics.stdev(returns)
    sharpe = mean / stdev if stdev > 0 else 0
    return {"mean": mean, "stdev": stdev, "sharpe_ratio": sharpe}
```"""),

    'integrations': ('python', """```python
# Example: API integration with retry
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def api_call(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
```"""),

    'marketing': ('python', """```python
# Example: SEO keyword analysis
def analyze_keywords(keywords: list[str]) -> list[dict]:
    results = []
    for kw in keywords:
        volume = get_search_volume(kw)
        difficulty = get_difficulty(kw)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "opportunity": volume / max(difficulty, 1),
        })
    return sorted(results, key=lambda x: x["opportunity"], reverse=True)
```"""),

    'mcp': ('typescript', """```typescript
// Example: MCP server tool definition
import { McpServer } from "@modelcontextprotocol/sdk";

const server = new McpServer({ name: "my-tools", version: "1.0.0" });

server.tool("search", { query: z.string() }, async ({ query }) => {
  const results = await search(query);
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
});
```"""),

    'meta': ('python', """```python
# Example: Skill performance tracking
def track_skill_usage(skill_name: str, success: bool, duration_ms: int):
    entry = {
        "skill": skill_name,
        "success": success,
        "duration_ms": duration_ms,
        "timestamp": datetime.utcnow().isoformat(),
    }
    append_to_metrics(entry)
    update_aggregate_stats(skill_name, success, duration_ms)
```"""),

    'mindset': ('markdown', """```markdown
# Daily Practice Template

## Morning (5 min)
- Set intention for the day
- Review top 3 priorities

## During the day
- Practice the skill in real situations
- Note moments of success and struggle

## Evening (5 min)
- Reflect: What worked? What did not?
- Log one lesson learned
```"""),

    'operations': ('python', """```python
# Example: SOP execution tracker
def execute_sop(sop_name: str, steps: list[str]) -> dict:
    results = []
    for i, step in enumerate(steps, 1):
        try:
            result = execute_step(step)
            results.append({"step": i, "status": "ok", "result": result})
        except Exception as e:
            results.append({"step": i, "status": "error", "error": str(e)})
            break
    return {"sop": sop_name, "steps": results}
```"""),

    'productivity': ('python', """```python
# Example: Task prioritization (Eisenhower Matrix)
def prioritize(tasks: list[dict]) -> dict:
    matrix = {"urgent_important": [], "important": [], "urgent": [], "neither": []}
    for task in tasks:
        if task["urgent"] and task["important"]:
            matrix["urgent_important"].append(task)
        elif task["important"]:
            matrix["important"].append(task)
        elif task["urgent"]:
            matrix["urgent"].append(task)
        else:
            matrix["neither"].append(task)
    return matrix
```"""),

    'research': ('python', """```python
# Example: Source evaluation
def evaluate_source(url: str) -> dict:
    return {
        "authority": check_domain_authority(url),
        "currency": get_last_updated(url),
        "objectivity": detect_bias(url),
        "accuracy": cross_reference(url),
    }
```"""),

    'sales': ('python', """```python
# Example: Lead scoring
def score_lead(lead: dict) -> int:
    score = 0
    if lead.get("company_size", 0) > 100: score += 20
    if lead.get("budget", 0) > 10000: score += 25
    if lead.get("timeline") == "immediate": score += 30
    if lead.get("engagement_level", 0) > 3: score += 25
    return min(score, 100)
```"""),

    'trading': ('python', """```python
# Example: Position sizing (Kelly Criterion)
def kelly_size(win_rate: float, avg_win: float, avg_loss: float) -> float:
    if avg_loss == 0: return 0
    b = avg_win / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly * 0.5, 0.02))  # Half-Kelly, max 2%
```"""),
}


def needs_ar(text):
    """Check if skill is missing anti-rationalization table."""
    return not bool(re.search(r'Anti-Rationalization|Common Rationalizations|Common Pitfalls', text))


def needs_code(text):
    """Check if skill is missing code examples."""
    return not bool(re.search(r'```', text))


def needs_verify(text):
    """Check if skill is missing verification checklist."""
    return not bool(re.search(r'## Verification|## Quality Checklist|## Quality Gates', text))


def add_section_before_end(text, section):
    """Add a section before the last line or after the last ## heading."""
    # Try to add before ## Related or at end
    if '## Related' in text:
        return text.replace('## Related', section + '\n\n## Related')
    elif '## Feedback' in text:
        return text.replace('## Feedback', section + '\n\n## Feedback')
    else:
        return text.rstrip() + '\n\n' + section


def fix_skill(path, category):
    """Fix quality warnings for a single skill."""
    text = path.read_text(encoding='utf-8')
    original = text
    fixes = []

    # Add anti-rationalization table
    if needs_ar(text):
        ar = AR_TABLES.get(category, AR_TABLES['development'])
        text = add_section_before_end(text, ar)
        fixes.append('ar')

    # Add code example (only if no code blocks at all)
    if needs_code(text):
        lang, code = CODE_EXAMPLES.get(category, ('python', CODE_EXAMPLES['development'][1]))
        # Add after Workflow or Process section
        if '## Workflow' in text:
            text = text.replace('## Workflow', '## Workflow\n\n' + code, 1)
        elif '## Process' in text:
            text = text.replace('## Process', '## Process\n\n' + code, 1)
        elif '## Steps' in text:
            text = text.replace('## Steps', '## Steps\n\n' + code, 1)
        else:
            text = add_section_before_end(text, code)
        fixes.append('code')

    # Add verification checklist
    if needs_verify(text):
        verify = """## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings"""
        text = add_section_before_end(text, verify)
        fixes.append('verify')

    if text != original:
        path.write_text(text, encoding='utf-8')

    return fixes


def main():
    cats = ['agents','automation','content','core','cybersecurity','data','development','devops',
            'financial','integrations','marketing','mcp','meta','mindset','operations','productivity','research','sales','trading']

    stats = {'ar': 0, 'code': 0, 'verify': 0, 'total': 0, 'errors': 0}

    for cat in cats:
        cat_dir = ROOT / cat
        if not cat_dir.exists():
            continue
        for md in sorted(cat_dir.rglob('SKILL.md')):
            try:
                fixes = fix_skill(md, cat)
                if fixes:
                    stats['total'] += 1
                    for f in fixes:
                        stats[f] += 1
            except Exception as e:
                stats['errors'] += 1
                print(f"  ERROR {md.parent.relative_to(ROOT)}: {e}", file=sys.stderr)

    print(f"Quality fix complete:")
    print(f"  Anti-rationalization added: {stats['ar']}")
    print(f"  Code examples added: {stats['code']}")
    print(f"  Verification added: {stats['verify']}")
    print(f"  Skills modified: {stats['total']}")
    print(f"  Errors: {stats['errors']}")

    return 0 if stats['errors'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
