---
name: adhd-style-eval-run
description: Use when running or resuming the i-have-adhd paired blind response-style eval
  (baseline vs candidate) to test a rules/skill text change — gpt-oss:20b or claude-sonnet-5
  judges, SIGKILL-resume pattern, score gate
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- eval
- evaluation
- response-style
- rules
- baseline
- candidate
- blind-judge
- measurement
version: 1.0.0
category: development
---

persona:
  name: "Domain Expert"
  title: "Master of Response-Style Evaluation"
  expertise: ['Blind Evaluation Design', 'Measurement Methodology', 'Judge Selection', 'Agent Skill Testing']
  philosophy: "A rule change is not adopted until it beats baseline on evidence, not vibes."
  credentials: ['Built the 1ai-rules section 18 eval', 'Four skill iterations measured', 'Judge-bias post-mortem']
  principles: ['Evidence before claims', 'Measure, then decide', 'Judge quality is measurement quality', 'Same-family judge is a confound']



# adhd-style-eval-run — paired blind response-style evaluation

## Overview

Tests whether injecting a proposed rules/skill text (e.g. a RULES.md section) changes
response quality. Paired, blind: same 15 cases x 3 trials, two conditions (baseline = no
injection, candidate = skill injected), judged blind by label. Fork of `ayghri/i-have-adhd`
(MIT). Harness repo: `oyi77/i-have-adhd-eval` (private), local checkout `~/projects/i-have-adhd-eval`.

## When to Use

- You changed rules text (§18 Response Communication, other RULES.md sections) or a
  response-style skill and must prove it helps before shipping.
- You need a reproducible before/after measurement for an agent-behavior change.
- You are resuming a killed eval run (SIGKILL is expected; resume, never restart).

**Trigger phrases:** "does this rule change help?", "evaluate §18", "run the response-style eval",
"is the skill better than baseline".

## When NOT to Use

- Single-case or anecdotal style checks — run the full harness or nothing.
- Measuring task outcome quality (correctness of code) — this harness scores response
  *style* dimensions only.
- The skill text is not the variable — anything else you change invalidates the pairing.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The judge said FAIL, so the rule is bad." | Check which judge. gpt-oss:20b scored every skill iteration −0.13..−0.46 (FAIL) while claude-sonnet-5 scored the SAME responses +0.41 (PASS). Weak-judge verdicts are style bias. |
| "One run is enough." | Judge variance floor is ~±0.25 per case (mean \|v4−v2\| 0.25, stdev 0.38 on identical skill text). Single-run deltas < 0.3 are indistinguishable from noise. |
| "I can eyeball the responses." | You can't blind yourself retroactively. The judge must not see which condition is which. |
| "Faster judge = more iterations." | gpt-oss:20b is fast but rewards verbose markdown on correctness/autonomy and only concedes concision — a systematic bias, not signal. |

## Layout

```
~/projects/i-have-adhd-eval/          # harness repo (oyi77/i-have-adhd-eval)
  scripts/run_evals.py                # generation + score aggregation (upstream verbatim)
  scripts/judge.py                    # blind judge driver (imports run_evals)
  scripts/ollama_runner.py            # runner: Ollama Cloud gpt-oss:20b
  scripts/freeai_runner.py            # runner: freeai gateway anthropic/claude-sonnet-5
  evals/cases.jsonl                   # 15 cases
  evals/rubric.md                     # grader rubric (judge:begin/end slice)
  evals/runners.json                  # runner registry (absolute script paths)
  skills/rules-output-section-v2.md   # shipping candidate (v3/v4 text)
  RESULTS.md                          # full run history + verdict
```

Runner contract: prompt from trailing argv (generation) or stdin (judging); emits ONLY the
assistant text on stdout. Harness neutralizes cwd, so runner commands in `evals/runners.json`
MUST use absolute script paths.

## Commands

Generate (resumes: skips completed rows, appends):

```
python3 scripts/run_evals.py run --runner ollama-cloud --runner-config evals/runners.json \
  --condition baseline --output results/responses.jsonl --allow-unmetered
# candidate: add --condition-skill skills/rules-output-section-v2.md --output results/candidate.jsonl
```

Judge (resumes: skips judged groups, appends):

```
python3 scripts/judge.py --responses results/all_responses.jsonl --runner ollama-cloud \
  --runner-config evals/runners.json --output results/scores.jsonl
```

Merge conditions first:

```
python3 -c "import json; rows=[json.loads(l) for f in ['results/responses.jsonl','results/candidate.jsonl'] for l in open(f)]; open('results/all_responses.jsonl','w').writelines(json.dumps(r)+'\n' for r in rows)"
```

Score (weighted comparison + gate):

```
python3 scripts/run_evals.py score results/scores.jsonl
```

Use the claude-sonnet-5 judge instead of gpt-oss for trustworthy verdicts (swap `--runner
ollama-cloud` for `--runner freeai-claude-sonnet`). The freeai runner resolves the API key from
`~/.omp/agent/models.yml` and honors the gateway's 429 `retry_after_seconds` with backoff.

## Operational facts

- **SIGKILL (exit 137) is survivable and EXPECTED** on this host (~2-4 min per run). Both
  scripts resume from their output file: skip completed rows + append. Rerun the SAME command;
  never delete the output file. A full 90-response run takes ~4-6 restarts.
- Run conditions SEQUENTIALLY, never concurrently — parallel runs both get killed and the
  gateways rate-limit (Ollama Cloud and freeai both enforce RPM windows).
- Score row shape: per (case_id, trial, condition), dims correctness/autonomy/actionability/
  safety/concision, weights .35/.25/.2/.1/.1. `score` emits `conditions.<name>.weighted_score`
  and `release_gate.passed` (blocker findings, >0.1 correctness/safety regression, must beat
  baseline weighted).
- Long freeai runs (claude-sonnet-5, ~16s/row + pacing) exceed single job windows: launch the
  judge as a managed process (`hub op:start`), follow its log, restart on failure — it resumes.

## Known limitation (report it)

Same-model generation+judging inflates agreement; the definitive check is a strong judge on
responses generated by a different model. Verified result: §18 with the v3/v4 fixes PASSES the
gate on claude-sonnet-5 both as re-judge (+0.411) and in a clean claude-generated run (+0.263);
the gpt-oss:20b judge's FAIL was measurement bias.

## Verification

After running the harness, confirm:

- [ ] 90 score rows (45 baseline + 45 candidate), 45 groups judged, no `went unjudged` line
- [ ] Judge ran blind (conditions labeled A/B, judge prompt never names conditions)
- [ ] Gate verdict read from `score` output, not eyeballed
- [ ] Judge model stated alongside the verdict (gpt-oss vs claude-sonnet-5 changes the answer)

## Process

1. Merge condition response files into one `all_responses.jsonl`.
2. Judge with the claude-sonnet-5 runner (freeai); relaunch on SIGKILL, never delete output.
3. Score with `run_evals.py score`; record weighted delta and gate verdict.
4. Read per-case deltas; separate real regressions from judge variance by re-checking the
   responses against the case criteria.
5. Update `RESULTS.md` with the iteration table before claiming a verdict.