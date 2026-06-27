#!/usr/bin/env python3
"""
fix-remaining-placeholders.py
Replace template placeholder content in all non-cybersecurity, non-mindset categories.
"""

import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATS = ['agents','automation','content','core','data','development','devops',
  'financial','integrations','marketing','mcp','meta','operations','productivity','research','sales','trading']

# ── Category → context mapping ──
CAT_CONTEXT = {
    'agents': ('AI agent', 'agent orchestration', 'autonomous task execution'),
    'automation': ('automation', 'workflow automation', 'process optimization'),
    'content': ('content creation', 'content production', 'media generation'),
    'core': ('core infrastructure', 'system foundation', 'platform capabilities'),
    'data': ('data processing', 'data analysis', 'data management'),
    'development': ('software development', 'coding practices', 'engineering workflows'),
    'devops': ('DevOps', 'infrastructure management', 'deployment automation'),
    'financial': ('financial analysis', 'finance operations', 'financial management'),
    'integrations': ('platform integration', 'system connectivity', 'API integration'),
    'marketing': ('marketing', 'growth marketing', 'audience engagement'),
    'mcp': ('MCP server', 'Model Context Protocol', 'tool integration'),
    'meta': ('meta-skills', 'skill management', 'system self-improvement'),
    'operations': ('business operations', 'operational efficiency', 'process management'),
    'productivity': ('productivity', 'workflow optimization', 'task management'),
    'research': ('research', 'investigation', 'knowledge discovery'),
    'sales': ('sales', 'revenue generation', 'customer acquisition'),
    'trading': ('trading', 'market analysis', 'financial markets'),
}


def has_placeholder(text: str) -> bool:
    body = text.split('---', 2)[-1] if text.count('---') >= 2 else text
    return (
        'Section content — see SKILL.md body for full details' in body or
        ('This section covers core rules for the' in body and 'Refer to the skill overview' in body)
    )


def parse_skill_info(name: str, category: str) -> dict:
    """Parse skill name into actionable components."""
    parts = name.split('-')

    # Common action verbs
    actions = {
        'agent': 'agent-based', 'bot': 'automated bot', 'builder': 'builder',
        'monitor': 'monitoring', 'scraper': 'data scraping', 'tracker': 'tracking',
        'analyzer': 'analysis', 'generator': 'generation', 'optimizer': 'optimization',
        'manager': 'management', 'scheduler': 'scheduling', 'publisher': 'publishing',
        'workflow': 'workflow', 'pipeline': 'pipeline', 'engine': 'engine',
    }

    topic = name.replace('-', ' ')
    cat_topic, cat_focus, cat_domain = CAT_CONTEXT.get(category, (category, 'operations', 'general'))

    # Determine action type from name
    action_type = 'implementation'
    for key, val in actions.items():
        if key in parts:
            action_type = val
            break

    return {
        'topic': topic,
        'category_topic': cat_topic,
        'category_focus': cat_focus,
        'category_domain': cat_domain,
        'action_type': action_type,
        'name': name,
    }


def generate_content(info: dict, category: str) -> str:
    """Generate category-appropriate content."""
    t = info['topic']
    ct = info['category_topic']
    cf = info['category_focus']
    at = info['action_type']

    # Category-specific content templates
    if category == 'agents':
        return f"""## Overview

{t.replace('-', ' ').title()} is an AI agent skill for {cf}. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step {t} workflows independently
- **Context awareness** — Adapt behavior based on current state and history
- **Error recovery** — Handle failures gracefully with retry and fallback logic
- **Integration** — Connect with external tools and services as needed

## Workflow

1. **Initialize** — Set up the agent context and load required resources
2. **Plan** — Break down the task into executable steps
3. **Execute** — Run each step, monitoring for errors and adapting as needed
4. **Verify** — Validate results against acceptance criteria
5. **Report** — Summarize outcomes and suggest next steps

## Configuration

- Define task objectives and constraints clearly
- Set appropriate timeout and retry limits
- Configure tool access and permissions
- Enable logging for debugging and audit

"""

    elif category == 'automation':
        return f"""## Overview

{t.replace('-', ' ').title()} automates {cf} to reduce manual effort and increase reliability.

## Workflow

1. **Define triggers** — Set up events or schedules that initiate the automation
2. **Configure inputs** — Specify data sources and parameters
3. **Design pipeline** — Define the sequence of automated steps
4. **Add error handling** — Set up retries, alerts, and fallback paths
5. **Test end-to-end** — Validate the full automation with realistic data
6. **Deploy and monitor** — Activate and track performance

## Configuration

- Set trigger conditions (schedule, webhook, event)
- Define input validation rules
- Configure notification channels for alerts
- Set retry policies and timeout limits

## Best Practices

- Start with simple automations and iterate
- Add logging at every step for debugging
- Use idempotent operations where possible
- Test with edge cases before deploying

"""

    elif category == 'content':
        return f"""## Overview

{t.replace('-', ' ').title()} enables {cf} with professional quality and consistency.

## Workflow

1. **Define brief** — Set objectives, audience, and style guidelines
2. **Research and gather** — Collect source material and reference content
3. **Create draft** — Generate initial content following the brief
4. **Refine and edit** — Polish for quality, accuracy, and engagement
5. **Publish and distribute** — Deploy to target platforms
6. **Track performance** — Monitor engagement and iterate

## Quality Checklist

- [ ] Content matches the defined brief and audience
- [ ] All facts verified against authoritative sources
- [ ] Formatting consistent with style guidelines
- [ ] SEO/distribution optimization applied
- [ ] Call-to-action clear and compelling

## Tools

- Content management system for publishing
- Analytics platform for performance tracking
- Design tools for visual assets
- Collaboration tools for review cycles

"""

    elif category in ('core', 'meta'):
        return f"""## Overview

{t.replace('-', ' ').title()} is a foundational {ct} skill that provides {cf} capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for {cf}
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

"""

    elif category == 'data':
        return f"""## Overview

{t.replace('-', ' ').title()} handles {cf} with support for multiple data formats and sources.

## Workflow

1. **Connect** — Establish connection to data sources
2. **Extract** — Pull data from source systems
3. **Transform** — Apply cleaning, normalization, and enrichment
4. **Load** — Write processed data to target destinations
5. **Validate** — Verify data quality and completeness
6. **Document** — Record schema changes and data lineage

## Data Quality Checks

- [ ] No null values in required fields
- [ ] Data types match schema definitions
- [ ] Referential integrity maintained
- [ ] Duplicate detection applied
- [ ] Outlier handling documented

## Supported Formats

- JSON, CSV, Parquet, Avro
- SQL databases (PostgreSQL, MySQL, SQLite)
- REST APIs and webhooks
- File systems (local, S3, GCS)

"""

    elif category == 'development':
        return f"""## Overview

{t.replace('-', ' ').title()} supports {cf} with best practices and proven patterns.

## Workflow

1. **Understand requirements** — Clarify acceptance criteria and constraints
2. **Design solution** — Plan architecture and identify patterns
3. **Implement** — Write code following project conventions
4. **Test** — Unit tests, integration tests, edge cases
5. **Review** — Code review for quality, security, and performance
6. **Document** — Update relevant docs and changelogs

## Quality Gates

- [ ] All tests passing
- [ ] No lint errors or warnings
- [ ] Code coverage meets threshold (≥70%)
- [ ] No security vulnerabilities detected
- [ ] Documentation updated

## Best Practices

- Follow SOLID principles and KISS
- Write self-documenting code with clear naming
- Handle errors explicitly — no silent failures
- Keep functions small and focused (<50 lines)
- Use immutable data patterns where possible

"""

    elif category == 'devops':
        return f"""## Overview

{t.replace('-', ' ').title()} manages {cf} with reliability and scalability.

## Workflow

1. **Define infrastructure** — Specify resources and configuration
2. **Version control** — Store all configurations in Git
3. **Automate deployment** — CI/CD pipeline for consistent releases
4. **Monitor** — Set up observability (metrics, logs, traces)
5. **Respond** — Incident response procedures and runbooks
6. **Optimize** — Performance tuning and cost management

## Configuration

- Environment variables for secrets and config
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- Container orchestration (Docker, Kubernetes)
- CI/CD pipeline (GitHub Actions, GitLab CI, ArgoCD)

## Reliability Checklist

- [ ] Health checks configured
- [ ] Auto-scaling policies defined
- [ ] Backup and recovery tested
- [ ] Rollback procedure documented
- [ ] Monitoring alerts configured

"""

    elif category == 'financial':
        return f"""## Overview

{t.replace('-', ' ').title()} provides {cf} with accuracy and compliance.

## Workflow

1. **Gather data** — Collect financial data from authoritative sources
2. **Analyze** — Apply financial models and calculations
3. **Validate** — Cross-check results against benchmarks
4. **Report** — Generate clear, actionable financial reports
5. **Recommend** — Provide data-driven suggestions

## Key Metrics

- Revenue and growth rates
- Profit margins (gross, operating, net)
- Cash flow and burn rate
- Return on investment (ROI)
- Risk-adjusted returns

## Compliance

- Follow GAAP/IFRS standards where applicable
- Maintain audit trail for all calculations
- Redact sensitive financial data in reports
- Document assumptions and methodologies

"""

    elif category == 'integrations':
        return f"""## Overview

{t.replace('-', ' ').title()} connects with external platforms via {cf}.

## Setup

1. **Authenticate** — Configure API keys, OAuth tokens, or webhooks
2. **Map data** — Define field mappings between systems
3. **Test connection** — Verify connectivity and permissions
4. **Sync data** — Initial data synchronization
5. **Monitor** — Track sync health and error rates

## Configuration

- API credentials (stored securely, never hardcoded)
- Rate limiting and retry policies
- Webhook endpoints for real-time updates
- Data transformation rules

## Error Handling

- Retry with exponential backoff on transient failures
- Alert on auth failures or rate limit hits
- Log all API requests/responses for debugging
- Graceful degradation when external service is down

"""

    elif category == 'marketing':
        return f"""## Overview

{t.replace('-', ' ').title()} drives {cf} with data-driven strategies.

## Workflow

1. **Research** — Analyze market, competitors, and audience
2. **Strategy** — Define goals, channels, and messaging
3. **Create** — Develop content and creative assets
4. **Launch** — Deploy campaigns across channels
5. **Optimize** — A/B test and iterate based on data
6. **Report** — Track KPIs and ROI

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

"""

    elif category == 'mcp':
        return f"""## Overview

{t.replace('-', ' ').title()} implements a Model Context Protocol server for {cf}.

## Architecture

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio or HTTP transport layer
- **Tools** — Callable functions with JSON Schema definitions
- **Resources** — Readable data sources with URI-based access

## Setup

1. Install the MCP server package
2. Configure environment variables and credentials
3. Register the server in MCP client configuration
4. Test tool invocations and resource access

## Configuration

- Server name and version
- Transport type (stdio, SSE, HTTP)
- Tool definitions with input/output schemas
- Resource URI patterns
- Authentication and rate limiting

## Integration

- Compatible with Claude, Cursor, and other MCP clients
- Supports streaming responses for large payloads
- Handles errors with standard MCP error codes

"""

    elif category == 'operations':
        return f"""## Overview

{t.replace('-', ' ').title()} streamlines {cf} for operational excellence.

## Workflow

1. **Assess** — Evaluate current state and identify gaps
2. **Design** — Plan improved processes and workflows
3. **Implement** — Roll out changes with team alignment
4. **Measure** — Track operational KPIs
5. **Iterate** — Continuous improvement based on data

## SOP Template

- **Purpose** — Why this process exists
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions
- **Escalation** — When and how to escalate
- **Review** — Schedule for periodic updates

## Key Metrics

- Process completion time
- Error/rework rate
- Team satisfaction scores
- Cost per operation
- SLA compliance rate

"""

    elif category == 'productivity':
        return f"""## Overview

{t.replace('-', ' ').title()} enhances {cf} with proven systems and tools.

## Daily Workflow

1. **Plan** — Review priorities and set daily objectives
2. **Execute** — Focus blocks with minimal interruptions
3. **Review** — End-of-day reflection and tomorrow's prep

## Frameworks

- **GTD (Getting Things Done)** — Capture, clarify, organize, reflect, engage
- **Pomodoro** — 25min focus + 5min break cycles
- **Eisenhower Matrix** — Urgent/Important prioritization
- **Time Blocking** — Dedicated blocks for deep work

## Tools

- Task management (Todoist, Notion, Linear)
- Calendar blocking for focus time
- Note-taking for capture and reference
- Automation for repetitive tasks

## Tips

- Batch similar tasks together
- Protect deep work time ruthlessly
- Review and adjust systems weekly
- Eliminate before optimizing

"""

    elif category == 'research':
        return f"""## Overview

{t.replace('-', ' ').title()} enables thorough {cf} with structured methodology.

## Workflow

1. **Define question** — Clarify the research objective
2. **Gather sources** — Collect primary and secondary data
3. **Analyze** — Apply analytical frameworks to findings
4. **Synthesize** — Combine insights into actionable conclusions
5. **Present** — Deliver findings in clear, compelling format
6. **Archive** — Store research for future reference

## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

"""

    elif category == 'sales':
        return f"""## Overview

{t.replace('-', ' ').title()} drives {cf} with systematic processes.

## Pipeline Stages

1. **Prospect** — Identify and qualify potential customers
2. **Connect** — Initial outreach and conversation
3. **Discover** — Understand needs and pain points
4. **Propose** — Present tailored solution
5. **Close** — Negotiate and finalize agreement
6. **Onboard** — Hand off to success team

## Key Metrics

- Pipeline velocity (deals × value × win rate ÷ cycle time)
- Conversion rate per stage
- Average deal size
- Customer lifetime value (CLV)
- Win/loss ratio

## Best Practices

- Qualify early — disqualify fast
- Listen more than you talk (70/30 rule)
- Follow up consistently (5+ touches)
- Track everything in CRM
- Ask for referrals after every closed deal

"""

    elif category == 'trading':
        return f"""## Overview

{t.replace('-', ' ').title()} provides {cf} capabilities with risk management.

## Workflow

1. **Research** — Analyze market conditions and opportunities
2. **Plan** — Define entry, exit, and position sizing
3. **Execute** — Place trades with proper order types
4. **Monitor** — Track positions and market changes
5. **Manage risk** — Apply stop-losses and hedging
6. **Review** — Post-trade analysis and journaling

## Risk Management

- Never risk more than 1-2% of portfolio per trade
- Set stop-loss before entering any position
- Diversify across uncorrelated assets
- Size positions based on volatility (ATR)
- Have a maximum daily loss limit

## Key Metrics

- Win rate and profit factor
- Sharpe ratio and max drawdown
- Average risk-reward ratio
- Expectancy per trade
- Correlation to benchmark

## Discipline Rules

- Follow your trading plan — no impulsive trades
- Cut losses short, let winners run
- Review every trade in your journal
- Never revenge trade after a loss
- Take breaks after consecutive losses

"""

    # Fallback generic content
    return f"""## Overview

{t.replace('-', ' ').title()} provides {cf} capabilities.

## Workflow

1. **Define objectives** — Clarify goals and success criteria
2. **Prepare** — Gather required resources and access
3. **Execute** — Perform core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions

## Configuration

- Set up required tools and access
- Define input/output formats
- Configure logging and monitoring
- Set resource limits and timeouts

"""


def fix_skill(path: Path, category: str) -> bool:
    text = path.read_text(encoding='utf-8')
    if not has_placeholder(text):
        return False

    fm_match = re.match(r'^(---\n.*?\n---\n?)(.*)', text, re.DOTALL)
    if not fm_match:
        return False

    frontmatter = fm_match.group(1)
    body = fm_match.group(2)

    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        return False
    skill_name = name_match.group(1).strip()
    info = parse_skill_info(skill_name, category)
    title = skill_name.replace('-', ' ').title()

    # Extract existing When to Use
    when_match = re.search(r'(## When to Use\s*\n(?:.*?\n)*?)(?=\n## |\Z)', body, re.DOTALL)
    when_section = when_match.group(1).strip() if when_match else ''

    new_body = f"# {title}\n\n"
    if when_section:
        new_body += f"{when_section}\n\n"
    else:
        new_body += f"""## When to Use

- When the task matches this skill's domain expertise
- For {info['category_focus']} workflows
- When specialized {info['category_topic']} knowledge is needed

"""

    new_body += generate_content(info, category)

    path.write_text(frontmatter + new_body, encoding='utf-8')
    return True


def main():
    total_fixed = 0
    total_skipped = 0
    total_errors = 0

    for category in CATS:
        cat_dir = ROOT / category
        if not cat_dir.exists():
            continue
        fixed = 0
        for md in sorted(cat_dir.rglob('SKILL.md')):
            try:
                if fix_skill(md, category):
                    fixed += 1
                    total_fixed += 1
                else:
                    total_skipped += 1
            except Exception as e:
                total_errors += 1
                print(f"  ERROR {md.parent.relative_to(ROOT)}: {e}", file=sys.stderr)
        if fixed > 0:
            print(f"  {category}: {fixed} fixed")

    print(f"\nRemaining categories: {total_fixed} fixed, {total_skipped} skipped, {total_errors} errors")
    return 0 if total_errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
