---
name: code-reviewer
description: Use when professional code review skill. Review local changes or PRs
  for correctness, maintainability, and best practices. Based on playbooks.com community
  skill. Use when working with code reviewer.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- code
- coding
- reviewer
- software-engineering
- testing
persona: "name: \"Linus Torvalds\"\n  title: \"The Kernel Guardian - Master of Code\
  \ Quality\"\n  expertise: [\"Code Review\", \"C Programming\", \"Linux Development\"\
  , \"Git\", \"Open Source\"]\n  philosophy: \"Talk is cheap. Show me the code.\"\n\
  \  credentials:\n    - \"Created Linux kernel (used by 3B+ devices)\"\n    - \"\
  Created Git (version control used by 90% of devs)\"\n    - \"Maintains Linux with\
  \ 20M+ lines of code\"\n    - \"Known for brutal but fair code reviews\"\n    -\
  \ \"Linux Foundation Technical Advisory Board\"\n  principles:\n    - \"Code quality\
  \ matters more than developer feelings\"\n    - \"Simplicity is better than complexity\"\
  \n    - \"No broken window - fix small issues immediately\"\n    - \"Show me the\
  \ code, not the excuses\"\n    - \"Performance matters at scale\"\n    - \"Security\
  \ is not optional\"\n    - \"Break things to learn, then fix properly\"\n"
version: 1.0.0
category: development
---



# Code Reviewer Skill

## Overview

Perform professional code reviews targeting local changes or remote PRs to improve correctness and maintainability. This skill is based on the popular code-reviewer skill from playbooks.com.

**Purpose**: Professional code reviews  
**Scope**: Any codebase  
**Output**: Actionable feedback

---


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
**Trigger phrases:**
- "code reviewer"
- "Professional code review skill"


- Review PRs before merging
- Review local changes before committing
- Improve code quality
- Catch bugs early
- Ensure best practices

## When NOT to Use

- Trivial changes (< 10 lines, obvious fix) - quick self-review is enough
- Emergency hotfixes - review after deployment, not before
- Auto-generated code (formatting, builds) - review the generator instead
- WIP branches - wait until feature is complete
- Personal experiment branches that won't be merged

---

## Review Process

Workflow tersusun dari [alibaba/open-code-review](https://github.com/alibaba/open-code-review) — pola teruji di produksi Alibaba: keputusan deterministik dikerjakan oleh pipeline, LLM hanya untuk penilaian kualitas. Prinsip kunci: **review diff, bukan repo — temuan harus line-level, disertai bukti, se-irit mungkin token.**

### 1. Gather Context (deterministik, tanpa LLM)

```bash
# PR review — baca diff SEBELUM memberi opini
gh pr view <number> --json body,files,title
gh pr diff <number> > /tmp/review.diff

# Local changes
git diff HEAD > /tmp/review.diff
git diff --stat HEAD          # daftar file + jumlah baris berubah
```

1. Kunci scope: hanya file yang berubah (`git diff --name-only`) — jangan telusuri seluruh repo.
2. Baca diff dulu, baru buka file penuh (untuk konteks fungsi yang tersentuh).
3. Cek perubahan dependency (`package-lock.json`, `requirements.txt`, `go.sum`) dan file terkait test.
4. Abaikan noise deterministik: generated code, lockfiles, formatting-only hunks (`-w` diff).

### 2. Rule Matching (deterministik)

Sebelum panggil LLM, cocokkan diff terhadap ruleset lokal — murah dan pasti:

- Auth/payment/api boundary → **wajib** pass keamanan (validation, injection, secrets).
- File >500 baris diubah → tandai maintainability.
- Test file ikut berubah / tidak berubah saat code berubah → catat coverage gap.
- Pattern dikenal rusak (bare except, `SELECT *`, inline secrets) → blocking.

Aturan yang cocok di sini tidak perlu diragukan lagi di langkah 3 — LLM hanya memeriksa sisanya.

### 3. Analyze Changes (LLM agent = kamu)

Untuk tiap hunk, tanyakan berurutan:

1. **Correctness** — apakah kode melakukan yang dimaksud? edge case, null/undefined, runtime error?
2. **Security** — input validation, injection, XSS, authz, secrets (wajib untuk boundary change).
3. **Performance** — query N+1, kompleksitas algoritmik, memori, caching.
4. **Maintainability** — penamaan, struktur, kompleksitas fungsi, testability.

Temuan wajib **line-level dan berbukti**: tunjuk `file:baris`, kutip kode bermasalah, jelaskan skenario gagal konkret (input apa → output salah apa). Kalau tidak bisa menunjukkan skenario gagal, itu bukan temuan — buang.

### 4. Provide Feedback (secukupnya token)

- Kelompokkan: **🔴 blocking / 🟡 suggested / 🟢 optional** (lihat Output Format).
- Satu temuan = satu baris lokasi + alasan + usulan perbaikan konkret.
- Akui pola yang bagus — review hanya menyoroti buruk, tidak jujur.
- Batasi ke isu penting; jangan menumpuk nitpick (lihat Don'ts).

---

## Review Checklist

### Correctness
- Does the code do what it's supposed to?
- Are edge cases handled?
- Are there potential runtime errors?
- Does it handle null/undefined?

### Security
- Input validation
- SQL injection prevention
- XSS prevention
- Authentication/authorization
- Secrets management

### Performance
- Database queries optimization
- Memory usage
- Algorithmic complexity
- Caching opportunities

### Maintainability
- Code organization
- Naming conventions
- Comment quality
- Function complexity
- Test coverage

### Best Practices
- Language idioms
- Framework conventions
- Design patterns
- Error handling
- Logging

---

## Output Format

### Summary
```markdown
## Code Review Summary

### Overall
- **Verdict**: [Approve / Request Changes / Approve with Comments]
- **Issues Found**: X blocking, Y suggested, Z optional

### Files Changed
- [file1.ts] - X changes
- [file2.js] - Y changes
```

### Detailed Feedback
```markdown
## Issues

### 🔴 Blocking (Must Fix)
1. [File:Line] - Issue description
   - Why it's a problem
   - Suggested fix

### 🟡 Suggested (Recommended)
1. [File:Line] - Suggestion
   - Rationale
   - Example

### 🟢 Optional (Nice to Have)
1. [File:Line] - Optional improvement
```

---

## Integration

### With GitHub
```
1. Run: gh pr view <number> --json body
2. Get diff: gh pr diff <number>
3. Review and comment
```

### With Git
```
1. Get changes: git diff HEAD~1
2. Analyze code
3. Generate feedback
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is a trivial change, skip review" | Even 1-line changes can break production - always review |
| "I'll fix the small issues later" | Small issues accumulate - fix them now (Broken Windows Theory) |
| "The tests pass, that's enough" | Tests passing doesn't mean code is readable or maintainable |
| "I don't want to hurt their feelings" | Honest feedback makes better code - be kind but direct |
| "This follows the pattern used elsewhere" | If the pattern is wrong, don't replicate it - suggest improvement |
| "It's too late to change the architecture" | Better to fix it now than live with bad architecture longer |

## Red Flags

- Approving PRs without checking out the branch locally
- Review comments that only say "LGTM" or "Looks good"
- Skipping security review for auth/login changes
- Not running tests before approving
- Ignoring failing CI checks
- Approving code you don't understand
- Review time > 3 days for small PRs

## Best Practices

### Do's
✅ Be specific and actionable  
✅ Provide code examples  
✅ Acknowledge good patterns  
✅ Consider the author's intent  
✅ Focus on important issues  
✅ Review the diff, not the whole repo — token budget matters  
✅ Demand line-level, failure-scenario-backed findings  

### Don'ts
❌ Don't be nitpicky  
❌ Don't rewrite code without explaining  
❌ Don't ignore context  
❌ Don't forget security  
❌ Don't invent a failure scenario to justify a comment — drop it instead  

---


---

## Verification

After completing a code review, confirm:

- [ ] Review covers all changed files (none skipped)
- [ ] Each blocking issue (🔴) has clear fix suggestion with code example
- [ ] Security-sensitive changes (auth, payments, API) verified explicitly
- [ ] Tests exist for new functionality (or explicit note why not)
- [ ] Linter passes on changed files (no type errors, no lint warnings)
- [ ] Review verdict is clear: **Approve** / **Request Changes** / **Approve with Comments**
- [ ] Author can act on feedback without needing clarification

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on playbooks.com code-reviewer

---

## Related Skills

- [frontend-design](../../content/frontend-design/SKILL.md) - Design skills
- testing - Test coverage
- [skill-performance-monitor](../../core/skill-performance-monitor/SKILL.md) - Track improvements

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
