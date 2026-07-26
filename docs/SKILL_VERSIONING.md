# 1ai-Skill Versioning v1.0.0

Rules for versioning individual skills, the schema contract, and the overall
repository.

---

## 1. Skill Version (frontmatter `version` field)

Each skill has an independent semver (Semantic Versioning 2.0.0) in its
frontmatter. The field follows MAJOR.MINOR.PATCH format.

### 1.1 Patch (X.Y.Z → X.Y.Z+1)

Increment when:
- Fixing typos, broken links, formatting
- Adding or improving code examples without changing behavior
- Updating documentation for clarity
- Fixing a test that was wrong

No semantic change to the skill's behavior.

### 1.2 Minor (X.Y.Z → X.Y+1.0)

Increment when:
- Adding new sections, examples, or content
- Improving depth without breaking existing patterns
- Adding new code examples that demonstrate additional use cases
- Adding cross-references to new skills
- Improving verification steps
- Adding new frontmatter fields (optional only)

Backward-compatible. Existing users of the skill should see no breakage.

### 1.3 Major (X.Y.Z → X+1.0.0)

Increment when:
- Removing or renaming a required section
- Changing a code example that would fail if copied verbatim
- Changing the skill's category (moves to new directory)
- Updating API calls, tool names, or commands that would cause
  scripts to error
- Changing required frontmatter fields
- Revoking or downgrading a permission declaration
- Any change that makes the skill no longer self-consistent

Breaking change. Existing users MUST review and adapt.

### 1.4 Special Values

| Version | Meaning |
|---------|---------|
| `0.1.0` | Unversioned / initial — default for existing skills. Implies no versioning history. |
| `0.y.z` | Pre-release. May break at any time. Not suitable for production use. |
| Missing | Treated as `0.1.0` by the validator. |

### 1.5 Examples

```
name: onchain-transaction-forensics
version: "3.2.0"
# Major 3 → breaking changes in v3
# Minor 2 → added cross-chain support
# Patch 0 → no hotfixes yet
```

```
name: free-saas-toolkit
version: "0.1.0"
# Pre-release. No stability guarantees.
```

---

## 2. Schema Version (`schema_version` field)

The schema version applies to the **frontmatter metadata format**, not the
skill content. It tracks changes to `schemas/skill.schema.json`.

### 2.1 Bumping Schema Version

| Change | Bump |
|--------|------|
| Adding new optional fields | Patch |
| Adding new required fields | Major |
| Removing a field | Major |
| Changing a field's type or constraints | Major |
| Changing enum values | Minor |
| Relaxing constraints (widening pattern, removing required) | Patch |

### 2.2 Schema Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Current | Initial schema with 23+ properties, conditional validation. |

### 2.3 Backward Compatibility

- Validators MUST accept all versions matching the same MAJOR.
- Schema version 1.x.y validators MUST accept legacy skills with no
  `schema_version` field (treated as 1.0.0).
- A MAJOR schema bump indicates skills MUST be updated before validation
  passes.

---

## 3. Repository Version (`package.json`)

The repository version is independent of individual skill versions.

### 3.1 Bumping

| Trigger | Bump |
|---------|------|
| New skills added | Patch or Minor |
| Schema change | Minor (compatible) or Major (breaking) |
| Skills deepened | Patch |
| Skills deprecated/removed | Minor |
| CI/CD pipeline changes | Patch |
| Breaking schema changes | Major |

### 3.2 Relationship to Skill Versions

The repository version does NOT constrain individual skill versions.
A repository v3.14.0 may contain skills at v0.1.0, v2.4.0, v3.1.0, etc.
Each skill evolves independently.

---

## 4. Version Lifecycle

Skills progress through lifecycle statuses. Version numbers are NOT reset
on status change.

```
draft → active → deprecated → removed
  │                      │
  └──────────────────────┘ (direct draft→deprecated allowed)
```

### 4.1 Status Transitions

| From | To | Requirements |
|------|----|--------------|
| *(none) | draft | Initial creation. No review needed. |
| draft | active | Passes lint, test, and schema validation. Quality score ≥ 70. |
| active | deprecated | Superseded by newer skill. Keep file on disk for backward refs. Set `status: deprecated` and note replacement in description. |
| deprecated | removed | Removal from SKILLS.json after ≥ 1 release cycle. File may remain on disk. |
| draft | deprecated | Abandoned. Same as active→deprecated. |
| active | draft | *(disallowed)* Once active, maintain. Fix problems in place. |

### 4.2 Removed Skills

A removed skill:
- Retains a SKILLS.json entry with `status: removed`
- MAY or MAY NOT have a SKILL.md file on disk
- MUST NOT appear in lint or test results
- Exists only for backward-compatible references (skill:// links)

---

## 5. Changelog Entries

Every release MUST update `CHANGELOG.md` with:

```markdown
## [v3.14.0] — 2026-07-26

### Added
- New skills: skill-a, skill-b
- New schema validation

### Changed
- Skill X: deepened with code examples
- Skill Y: fixed broken link

### Removed
- Skill Z: deprecated (use new-skill-z instead)
```

---

## 6. Fast Track

For urgent fixes (broken links, typos, test fixes):
- Repository version patch bump only
- No changelog required (informal commit message suffices)
- Skill version bump optional
- Full validation still required before push
