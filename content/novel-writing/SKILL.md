---
name: novel-writing
description: Use when complete novel and fiction writing skill covering story structure,
  character creation, world-building, dialogue, pacing, and chapter craft. Adopts
  Chinese novelist patterns (show-don't-tell, conflict, cliffhanger) plus Western
  frameworks. Includes kids books (picture book, middle grade) and Buku Bahasa Indonesia
  for Indonesian fiction. Use when writing novels, short stories, or children's fiction.
domain: content
tags:
- content
- writing
- fiction
- novel
- character
- plot
- worldbuilding
- story
- creative-writing
- kids
- childrens-books
- middle-grade
- picture-book
- indonesian
- buku-anak
- bahasa-indonesia
author: oyi77
license: MIT
subdomain: writing
version: 1.0.0
category: content
---


# Novel & Fiction Writing — Complete Craft System

## Overview

This is a complete fiction writing system that **adopts the proven patterns** from the popular chinese-novelist skill (penglonghuang, 4.9K installs) and **extends them** with Western novel craft frameworks, character creation systems, world-building methodology, genre conventions, and code-backed workflows.

### Three Golden Rules (adopted from chinese-novelist)

| # | Rule | Meaning |
|---|------|---------|
| 1 | **Show, Don't Tell** | Dramatize emotions through action, dialogue, and sensory detail — never state feelings flatly |
| 2 | **Conflict Drives Plot** | Every scene must contain tension between opposing forces (character vs. character, self, nature, society) |
| 3 | **Cliffhanger Chapters** | End each chapter at a decision point or revelation — make readers turn the page |

### Key Features (adopted & expanded)

| Feature | From Reference | Expansion |
|---------|---------------|-----------|
| **Interrupted Continuation** | Resume from any text prompt | Also: scene-stub, outline, or character note |
| **Auto-Validation** | Chapter quality & self-refine | Also: continuity checker, character voice checker, pacing analyzer |
| **Parallel Writing** | Multiple chapters, one prompt | Also: multiple POVs, parallel timelines |
| **Multi-Language** | Adapts to user language | Bilingual: English + Chinese web novel patterns |

## Quick Start — Minimal Viable Process

For small-context models or when you need the minimum to start writing:

1. **Pick a story structure** — Three-Act, Hero's Journey, or Save the Cat (see Story Structure below)
2. **Define each major character's GMC** — Goal, Motivation, Conflict (see Character Creation)
3. **Write chapters as Entry → Escalation → Exit Hook** (see Chapter Craft)
4. **Run auto-validation after each chapter** (see Auto-Validation)
5. **Three-pass revision**: structure → scene craft → line edit (see Revision Workflow)

Genre-specific templates (Fantasy, Mystery, Chinese Web Novel, Kids Books, Buku Indonesia) are in Genre Templates below. Skip them unless they apply to your project.

---

## Story Structure

### 1. Three-Act Structure

```
ACT I (Setup) — 25%          ACT II (Confrontation) — 50%    ACT III (Resolution) — 25%
┌──────────────┐              ┌──────────────────────┐        ┌──────────────────┐
│ • Inciting    │              │ • Rising action       │        │ • Climax          │
│   Incident    │───→         │ • Midpoint twist      │───→    │ • Falling action  │
│ • First       │              │ • "All is lost"       │        │ • Denouement      │
│   Plot Point  │              │ • Darkest moment      │        │ • Final state     │
│ • Key Q:      │              │ • Q: Can they win?    │        │ • Q: What changed?│
│   "Who is     │              │                        │        │                  │
│    the hero?" │              │                        │        │                  │
└──────────────┘              └──────────────────────┘        └──────────────────┘
```

### 2. Hero's Journey (Campbell / Vogler)

```python
beat = {
    "ordinary_world": "Hero in their normal life",
    "call_to_adventure": "Something disrupts the normal",
    "refusal_of_call": "Hero hesitates or refuses",
    "meeting_mentor": "Guide provides wisdom/tool",
    "crossing_threshold": "Hero commits to the journey",
    "tests_allies_enemies": "Learning the new world's rules",
    "approach_inmost_cave": "Preparing for greatest challenge",
    "ordeal": "Hero faces their biggest fear — often a death/rebirth",
    "reward": "Hero gains what they sought",
    "road_back": "Return journey, not yet safe",
    "resurrection": "Final test — transformed, they face one last trial",
    "return_elixir": "Hero returns with wisdom to share",
}

# Check: does your story map to at least 8 of 12 beats?
assert sum(1 for b, v in beat.items() if v != "") >= 8
```

### 3. Save the Cat! (Blake Snyder)

| Beat | Page % | What Happens |
|------|--------|-------------|
| Opening Image | 1% | A snapshot of the hero's flawed world |
| Theme Stated | 5% | What the hero needs to learn (stated by someone else) |
| Set-Up | 1–10% | Hero's flaw, supporting cast, stakes |
| Catalyst | 10% | Inciting event — everything changes |
| Debate | 10–20% | Should I go? Doubt and weighing options |
| Break into Two | 20% | Hero chooses the new world |
| B Story | 22% | A relationship that teaches the theme |
| Fun and Games | 20–55% | The promise of the premise — the fun part |
| Midpoint | 55% | False victory OR false defeat — stakes escalate |
| Bad Guys Close In | 55–75% | Pressure mounts; hero loses allies, confidence, or ground |
| All Is Lost | 75% | A death, betrayal, or failure — no way out |
| Dark Night of the Soul | 75–85% | Grief, reflection, and finding the real answer |
| Break into Three | 85% | Hero discovers the actual solution |
| Finale | 85–99% | Hero applies the lesson — climax |
| Final Image | 99–100% | Mirror of opening image — shows transformation |

### 4. Kishōtenketsu (Classical Four-Act Structure — No Conflict Required)

| Stage | Japanese | Function |
|-------|----------|----------|
| Introduction | 起 (ki) | Present a scene, setting, or normal state |
| Development | 承 (shō) | Deepen or expand — add new element |
| Twist | 転 (ten) | Unexpected turn: something doesn't fit |
| Resolution | 結 (ketsu) | Connect, reveal harmony, show deeper meaning |

Best for: literary fiction, slice-of-life, and stories where discovery displaces conflict.

### 5. Chinese Web Novel (网文) — Three Golden Chapters (黄金三章)

The first three chapters must:

1. **Chapter 1 — The Hook (开篇)** : Introduce protagonist with a clear flaw or misfortune → hint at cheat/counterattack coming
2. **Chapter 2 — The System (金手指)** : Reveal the unique advantage (cheat skill, system, transmigration knowledge, hidden inheritance)
3. **Chapter 3 — The Payoff (打脸)** : First satisfying face-slap moment — protagonist uses their advantage to overcome an early opposer

**Pacing formula:** Small victory every 3–5 chapters (小爽点), medium victory every 10–15 chapters (中爽点), arc climax every 30–50 chapters (大高潮).

---

## Character Creation

### GMC (Goal / Motivation / Conflict)

Every character needs a clear GMC per story arc:

```python
@dataclass
class CharacterGMC:
    goal: str            # What they want
    motivation: str      # Why they want it (emotional need)
    conflict: str        # What stops them (internal + external)

@dataclass
class CharacterArc:
    beginning_gmc: CharacterGMC
    midpoint_shift: str   # How GMC changes at midpoint
    ending_gmc: CharacterGMC  # How GMC resolves
    inner_flaw: str       # The lie they believe
    truth_to_learn: str   # What accepting the truth looks like

def validate_character_arc(arc: CharacterArc) -> list[str]:
    """Check arc coherence — does the character actually change?"""
    issues = []
    if arc.beginning_gmc.goal == arc.ending_gmc.goal:
        issues.append("Goal didn't change — flat arc without intentional design")
    if arc.beginning_gmc.motivation == arc.ending_gmc.motivation:
        issues.append("No motivational shift — missing emotional growth")
    return issues
```

### Character Voice Profile

```python
@dataclass
class CharacterVoice:
    name: str
    archetype: str       # hero, mentor, trickster, shadow, herald, etc.
    speech_pattern: str  # e.g. "formal, uses full sentences" | "halting, with filler words"
    vocabulary_tier: int  # 1 (simple) to 5 (erudite)
    pet_phrases: list[str] = None
    tells_lie_when: str = ""  # Under what pressure they lie
    emotional_giveaway: str = ""  # Body language that betrays them

    def sample_dialogue(self, emotion: str, topic: str) -> str:
        """Generate in-character dialogue sample for consistency checking"""
        # Used to validate dialogue attribution scenes
        return f"[{self.name} speaking about '{topic}' with {emotion} — style: {self.speech_pattern}]"
```

### Archetype Galaxy

| Archetype | Core Drive | Best For | Example |
|-----------|-----------|----------|---------|
| **Hero** | Prove worth / protect | Protagonist | Katniss Everdeen |
| **Mentor** | Pass on wisdom | Guide figure | Haymitch, Obi-Wan |
| **Shadow** | Impose will / destroy | Villain | Voldemort, Sauron |
| **Trickster** | Disrupt norms / expose truth | Comic relief, chaos agent | Tyrion, Loki |
| **Herald** | Announce change | Catalyst character | Fiver in Watership Down |
| **Guardian** | Test worthiness | Gatekeeper | The Sphinx at Thebes |
| **Shape-Shifter** | Keep identity hidden | Unreliable ally | Snape |
| **Ally** | Support / sacrifice | Companion | Samwise Gamgee |

---

## World-Building

### Sanderson's Three Laws of Magic

1. **First Law:** An author's ability to resolve conflict with magic is directly proportional to how well the reader understands that magic
2. **Second Law:** Limitations > Powers — what magic CAN'T do is more interesting than what it can
3. **Third Law:** Expand before adding — deepen an existing system before adding a new one

### Checklist per Fictional Element

```python
def check_world_consistency(element: str, properties: dict) -> list[str]:
    """
    Validate a world-building element for internal consistency.
    """
    issues = []
    if "cost" not in properties:
        issues.append(f"'{element}' has no cost — free abilities lack narrative tension")
    if "limitation" not in properties:
        issues.append(f"'{element}' has no limitations — readers will ask 'why not use X for everything?'")
    if "impact" not in properties:
        issues.append(f"'{element}' has no shown impact on daily life — magic shouldn't be background wallpaper")
    return issues
```

### The Iceberg Principle (Tolkein)

Reveal 10% of your world; know the other 90%. Every reference to history, geography, or culture should feel like it sits on a foundation of real knowledge — even if only the author sees the whole iceberg.

---

## Dialogue Craft

### Mechanics Checklist

- [ ] **Subtext:** Do characters say what they mean, or what they NEED to say? (Good dialogue: they need to say something else.)
- [ ] **Beats:** Action beats replace dialogue tags and reveal character — "She traced the rim of her glass." vs. She said nervously.
- [ ] **Distinct voices:** Cover the character names and read — can you tell who's speaking?
- [ ] **Exposition delivery:** Information revealed through argument, not through "As you know, Bob..."
- [ ] **Rhythm:** Short exchanges for tension; longer sentences for reflection or intimacy
- [ ] **Silence:** What characters DON'T say is louder than what they do

### On-the-Nose vs. Subtext

```
ON THE NOSE:
"I'm angry at you for forgetting my birthday."
"Oh, I'm sorry, I was busy with work."

SUBTEXT:
"You remembered the Stark account's anniversary."
"...Was there something else I should have remembered?"
```

---

## Pacing & Tension

### Scene / Sequel (Dwight Swain)

| Scene (Proactive) | → | Sequel (Reactive) |
|-------------------|---|-------------------|
| Goal | | Reaction |
| Conflict | | Dilemma |
| Disaster | | Decision → new goal |

### Micro-Tension Checklist

- [ ] Every paragraph: is there a question the reader wants answered?
- [ ] Every page: is there a reason to turn it?
- [ ] After each revelation: what NEW question arises?
- [ ] Dialogue: do the characters want opposite things?

### Word Count by Genre (Novel)

| Genre | Typical Length | Chapter Avg | Scene Avg |
|-------|---------------|-------------|-----------|
| Literary | 60,000–100,000 | 3,000–5,000 | 1,000–2,500 |
| Fantasy / Sci-Fi | 90,000–150,000 | 4,000–6,000 | 1,500–3,000 |
| Mystery / Thriller | 70,000–95,000 | 2,500–4,000 | 1,000–2,000 |
| Romance | 50,000–90,000 | 2,000–4,000 | 1,000–2,000 |
| YA / Middle Grade | 40,000–80,000 | 2,000–3,500 | 800–1,500 |
| Chinese Web Novel (网文) | 500,000–3,000,000 | 2,000–3,000 | 1,500–2,500 |

---

## Chapter Craft

### Chapter Anatomy

Every chapter should contain:
1. **Entry Hook** — Why start reading this chapter NOW? (sensory detail, intriguing statement, action beat)
2. **Escalation** — The scene's tension rises or twists
3. **Exit Hook** — Why read the NEXT chapter? (cliffhanger, revelation, decision point, question)

### Chapter-Ending Techniques

| Technique | Effect | Example |
|-----------|--------|---------|
| Door slam | Scene ends with bad news | "The king is dead." |
| Revelation | New info changes everything | "She's your sister." |
| Question | Reader must find the answer | "What if the monster is real?" |
| Decision point | Protagonist must choose | The clock read 11:59. |
| Ironic reversal | Expectation inverted | The hero found the sword — and sold it. |
| Incoming threat | Danger approaching | "They know where we live." |

### Parallel Writing (adopted from chinese-novelist)

When writing multiple chapters in one turn:

```
PROMPT FORMAT:

Write Chapters 4, 5, and 6 of my novel.

For each chapter:
1. Identify the POV character
2. State the scene goal
3. Write complete chapter text
4. End with a hook pointing to the next chapter
5. Count words

VALIDATE each chapter after writing:
- ✓ Word count within target (±500 words)
- ✓ Scene goal achieved or subverted meaningfully
- ✓ At least one Show-Don't-Tell beat
- ✓ Chapter ends with hook
- ✓ POV consistent throughout
```

### Interrupted Continuation (adopted from chinese-novelist)

When resuming from any state — a saved draft, a scene stub, a character note — use:

```
PROMPT FORMAT:

[Current state: paste what exists — any text]
[Goal: what should happen next in the story]

Continue from the provided text. Do not repeat it.
Identify: what is the next scene's goal?
Write the scene.
Then auto-validate: does it connect logically to what came before?
```

---

## Auto-Validation (adopted & expanded from chinese-novelist)

After each writing cycle, run validation:

```python
@dataclass
class ValidationResult:
    passed: bool
    issues: list[str]

def validate_chapter(chapter_text: str, chapter_num: int, prev_hook: str = "") -> ValidationResult:
    issues = []

    # 1. Word count
    wc = len(chapter_text.split())
    if wc < 1500 or wc > 6000:
        issues.append(f"Word count {wc} outside 1500–6000 range")

    # 2. Show-Don't-Tell check — look for telling emotion words
    tell_words = {"felt", "felt that", "felt like", "knew that", "realized that", "was angry",
                  "was sad", "was happy", "was scared", "was excited"}
    for word in tell_words:
        if word in chapter_text.lower():
            issues.append(f"Possible telling: '{word}' — dramatize instead")
            break  # one warning per chapter

    # 3. Cliffhanger check — does last paragraph end with a hook?
    final_para = chapter_text.split("\n\n")[-1].strip()
    question_markers = ["?" in final_para, "..." in final_para,
                        any(w in final_para.lower() for w in ["sudden", "reveal", "found", "discover", "then"])]
    if not any(question_markers):
        issues.append("Chapter may lack a strong exit hook")

    # 4. Conflict check — does the chapter have tension?
    conflict_words = {"but", "however", "yet", "refused", "fight", "argue",
                      "struggle", "trap", "betray", "choice", "cost"}
    if not any(w in chapter_text.lower() for w in conflict_words):
        issues.append("No clear conflict signal detected — ensure tension exists")

    # 5. Continuity check (if previous hook provided)
    if prev_hook and prev_hook not in chapter_text:
        issues.append("Previous chapter's hook not addressed in this chapter's opening")

    return ValidationResult(passed=len(issues) == 0, issues=issues)
```

### Self-Refine Loop

```python
def write_with_refine(outline: dict, max_refinements: int = 3) -> str:
    """
    Write chapter then auto-validate and refine until clean.
    """
    chapter = generate_chapter(outline)
    for _ in range(max_refinements):
        result = validate_chapter(chapter, outline["chapter_num"], outline.get("prev_hook", ""))
        if result.passed:
            return chapter  # Good enough — ship it
        # Fix the most critical issue
        fix = identify_fix(result.issues, chapter)
        chapter = refine_chapter(chapter, fix)
    return chapter  # Best effort after max_refinements
```

---

## Genre Templates

### Fantasy

```python
fantasy_epic = {
    "world_scope": "multiple continents, distinct cultures",
    "magic_system": "defined rules with costs and limitations",
    "scale": "the fate of a kingdom or world",
    "typical_length": "100,000–150,000 words",
    "key_beats": [
        "Hero in ordinary/magical world",
        "Call to quest (world-threat)",
        "Gathering the party",
        "Learning the magic rules",
        "Confrontation with dark lord",
        "Sacrifice and return"
    ],
    "avoid": "info-dumping history in chapter 1; show the world through action"
}
```

### Mystery / Thriller

| Beat | Detective Novel | Thriller |
|------|----------------|----------|
| Hook | Body is found | Bomb is ticking |
| Investigation | Suspects interviewed | Chase begins |
| Twist | Clue points wrong way | Ally betrays |
| Darkest moment | Case seems unsolvable | All seems lost |
| Reveal | Identity of killer | Truth exposed |
| Resolution | Justice served | World restored (changed) |

### Chinese Web Novel (网文) — 爽文 (Power Fantasy)

```
爽文 Key Mechanics:

1. 打脸 (Face-Slapping) — The protagonist is underestimated, then decisively proves superiority.
   Pattern: Mock → Reveal power → Public humiliation of mocker → Face-slap

2. 扮猪吃虎 (Playing Pig to Eat Tiger) — Protagonist pretends to be weak, then crushes the strong.
   Pattern: Disguised weakness → Arrogant antagonist takes bait → Devastating counterattack

3. 装逼打脸 (Show-Off Face-Slap) — Protagonist deliberately provokes to invoke face-slapping chain.
   Pattern: Antagonist provokes → Protagonist pretends to be scared → Spring the trap

4. 升级 (Leveling Up) — Clear progression markers with visible power increases.
   Each level shows concrete improvement that matters to current conflict.

5. 后宫 (Harem) — Multiple romantic interests (optional, genre-dependent).
   Critical: each interest should have distinct personality and role.

Avoid: Protagonist achieving everything easily — tension requires REAL threat.
If protagonist can solve everything, there's no conflict.
```

---

### Kids Book Writing

Complete guide for children's fiction — from board books to middle grade novels.

| Category | Age | Word Count | Format | Key Feature |
|----------|-----|-----------|--------|-------------|
| **Board Books** | 0–3 | 0–100 words | Thick pages, durable | Sensory, rhythm, simple bold images |
| **Picture Books** | 3–7 | 300–800 words | 32 pages standard | Illustration-text dance, must be read-aloud |
| **Early Readers** | 5–8 | 500–2,500 words | Short chapters, large font | Simple vocab, sight words, short sentences |
| **Chapter Books** | 7–10 | 5,000–15,000 words | Short chapters, few illustrations | Simple plots, fast pacing, series-ready |
| **Middle Grade** | 8–12 | 25,000–50,000 words | Full novel format | Growing independence, school/friendship stakes |
| **YA (Young Adult)** | 13–18 | 50,000–90,000 words | Standard novel | Identity, first love, larger world questions |

#### Picture Book — The 32-Page Standard (Danny G's No-Fail Format)

Practically every picture book naturally follows this arc:

| Pages | Beat | Function |
|-------|------|----------|
| 1–20 | **Problem** | Establish character, want, obstacle; build through 4–6 spread sequences |
| 21–24 | **Climax** | The BIG moment — character faces the problem directly |
| 25–28 | **Resolution** | Problem solved through character's own action |
| 29–32 | **Closing** | Final page turn — satisfying visual/verbal finish |

```
PAGE TURN = REVEAL. The text on page N must make the reader NEED to turn to page N+1.
Good picture book text has a "curtain" word at each spread break — the word that creates the turn.
```

#### Kids Book Craft Essentials

- **Read-aloud test**: Read every draft ALOUD. Every word must earn its place when spoken.
- **Illustration partnership**: What the picture shows, the text doesn't tell — and vice versa. Let the illustrator's half of the story breathe.
- **Repetition with variation**: Pattern → pattern break → pattern return. Kids expect the pattern; the break creates the tension.
- **Age-appropriate vocabulary**: 1–2 challenge words per spread (guessable from context). For early readers, sight words + phonetic decoding.
- **Refrain / running gag**: A repeating line or joke that kids can chant along with (e.g., "I do not like green eggs and ham").
- **Adult off-stage**: If the kid character can solve the problem themselves, the story empowers. If an adult rescues them, it doesn't.

#### Middle Grade Novel Craft

MG novels look like adult novels but follow different rules:

| Criterion | Middle Grade | Adult |
|-----------|-------------|-------|
| Protagonist age | 9–12 | 20+ |
| Stakes | Personal/social — friendship, family, justice | Life/death, career, relationships |
| Voice | Authentic kid — not an adult remembering childhood | Mature perspective |
| Adult involvement | Adults present but NOT solving the problem | Adults fully engaged |
| Ending | Hopeful, earned — often bittersweet OK | Any resolution |

```python
def check_mg_compatibility(story: dict) -> list[str]:
    """Screen an outline for MG novel compatibility."""
    issues = []
    if story.get("protagonist_age", 0) > 14:
        issues.append("Protagonist should be 9–12 for true MG voice")
    if not story.get("kid_solves_problem", True):
        issues.append("Adult rescue invalidates MG empowerment contract")
    if story.get("romance_amount", "none") not in ("none", "crush-only"):
        issues.append("MG romance stays at crush/awkward-dance level — no consummation")
    themes = story.get("themes", [])
    kid_friendly = {"friendship", "family", "justice", "identity", "bravery",
                    "belonging", "curiosity", "difference", "loss"}
    if not any(t in kid_friendly for t in themes):
        issues.append("Themes should be accessible to 8–12 year old readers")
    return issues
```

#### Series Architecture for Kids

Kids are series readers. Design for series from the start:

1. **Standalone with series potential** — Book 1 tells a complete story but leaves world/characters wanting more
2. **Rising series arc** — Each book raises the stakes; a multi-book thread runs underneath
3. **Episodic series** — Same characters, same formula, different setting each book (Magic Tree House model)

```
Middle Grade & Chapter Book Series Models:

• Boxcar Children: Episodic — solve mystery in each book
• Harry Potter: Rising arc — each book bigger threat
• Diary of a Wimpy Kid: Episodic — school year vignettes
• Percy Jackson: Rising arc — quest per book + prophecy thread
• Magic Tree House: Episodic — historical adventure per book
```

---

### Buku Bahasa Indonesia (Indonesian-Language Fiction)

Panduan lengkap menulis fiksi dalam bahasa Indonesia — untuk pasar penerbitan nasional dan platform digital.

#### Pasar Buku Indonesia

Indonesia memiliki pasar penerbitan terbesar di Asia Tenggara. Karakteristik utama:

- **Platform digital** → **buku cetak**: Banyak novel populer berawal dari Wattpad atau Cabaca sebelum diterbitkan secara fisik
- **Pembaca setia genre**: Roman remaja, fiksi Islami, dan horor memiliki basis pembaca yang loyal
- **Pengaruh media**: Adaptasi film/series (Dilan, Ayat-Ayat Cinta, Rindu) mendorong penjualan buku secara signifikan
- **Harga jual**: IDR 50.000–150.000 per buku; margin tipis — volume penjualan adalah kunci

#### Genre Populer di Pasar Indonesia

| Genre | Deskripsi | Target Pembaca |
|-------|-----------|---------------|
| **Roman Remaja** | Kisah cinta dengan drama sekolah/keluarga; voice ringan, emosional | Remaja 13–18 |
| **Fiksi Islami** | Novel dengan nilai-nilai Islam, sering mengandung romance/keluarga; ending moral | Dewasa muda 18–35 |
| **Horor / Misteri** | Kisah mistis berdasarkan urban legend Indonesia; atmosfer lokal yang kuat | 16+ |
| **Sastra Serius** | Novel kontemporer dengan tema sosial, politik, budaya; gaya sastra | 20+ |
| **Cerita Anak** | Dongeng modern, petualangan, nilai moral; bahasa sederhana | 4–12 |
| **Fiksi Pengembangan Diri** | Novel yang menyampaikan pelajaran hidup melalui cerita (inspiratif) | 16+ |

#### Bahasa Indonesia untuk Penulisan Kreatif

- **Baku vs. sehari-hari**: Narasi menggunakan bahasa baku (formal) tetapi dialog menggunakan bahasa sehari-hari (natural). Jangan tulis dialog seperti buku tata bahasa.
- **Tingkat kesopanan**: Pilih sapaan sesuai hubungan karakter — *Anda* (formal), *Kak/Mas/Mbak* (semi-formal akrab), *lo/gue* (sangat santai, Jabodetabek).
- **Kata serapan regional**: Gunakan kata daerah dengan bijak — beri konteks agar pembaca di luar daerah tetap mengerti. Contoh: *siger* (Lampung) bisa dijelaskan melalui narasi.
- **Pantun dan pribahasa**: Alat puitis yang kuat untuk dialog karakter bijak atau narasi tematik. Jangan berlebihan.

```python
@dataclass
class NovelIndonesia:
    """Parameter template for an Indonesian novel."""
    judul: str
    genre: str  # roman, fiksi-islami, horor, sastra, cerita-anak
    target_kata: int  # 40000–80000
    setting_lokasi: str  # kota/daerah di Indonesia
    suasana: str  # segar, mistis, haru, tegang
    narasi_baku: bool = True
    dialog_sehari_hari: bool = True
    moral_ending: bool = False

    def cek_konsistensi(self) -> list[str]:
        masalah = []
        if self.genre == "fiksi-islami" and not self.moral_ending:
            masalah.append("Fiksi Islami umumnya memiliki pesan moral — pertimbangkan tambahkan")
        if self.target_kata < 40000:
            masalah.append("Novel Indonesia biasanya 40.000+ kata — terlalu pendek")
        if self.narasi_baku and self.dialog_sehari_hari:
            masalah.append("Kombinasi baku + sehari-hari benar — pastikan tidak tercampur dalam satu paragraf")
        return masalah
```

#### Perbedaan dengan Novel Barat

| Aspek | Novel Barat | Novel Indonesia |
|-------|-----------|----------------|
| **Gaya prosa** | Deskriptif, banyak narasi internal | Lebih ringkas, banyak dialog |
| **Emosi** | Subtext, implied | Langsung, eksplisit |
| **Moral/pesan** | Opsional, sering ambiguous | Diharapkan (kecuali sastra kontemporer) |
| **Ending** | Bisa bittersweet atau gelap | Happy ending atau hopeful sangat disukai |
| **Setting** | Imajinatif atau berdasarkan lokasi nyata | Sangat lokal — pembaca suka mengenali tempat |
| **Serial** | Trilogi atau stand-alone | Series panjang (5–10+ buku) jika sukses |

#### Platform Digital Indonesia

| Platform | Keunggulan | Model |
|----------|-----------|-------|
| **Wattpad** | Basis pembaca besar, banyak dieksplor penerbit | Gratis → kontrak penerbitan |
| **Cabaca** | Pembaca berbayar, penulis dapat royalti | Langganan / per-bab |
| **Storial** | Komunitas penulis aktif, ada kelas menulis | Gratis + premium |
| **Karyarsa** | Fokus pada cerita pendek dan puisi | Komunitas |

#### Word Count per Format (Pasar Indonesia)

| Format | Halaman | Kata |
|--------|--------|------|
| Cerita Anak Bergambar | 24–32 halaman | 200–600 kata |
| Novel Remaja (YA) | 200–300 halaman | 40,000–60,000 kata |
| Novel Dewasa | 250–400 halaman | 50,000–80,000 kata |
| Kumpulan Cerpen | 150–250 halaman | 25,000–40,000 kata |
| Novel Horor | 200–350 halaman | 45,000–70,000 kata |
| Web Serial (bab per bab) | 200–1000+ bab | 1,000–3,000 per bab |

#### Tips Menulis Bab Pembuka (for Indonesian Market)

1. **Language setting**: Tentukan level bahasa di bab 1 — pembaca langsung tahu apakah ini roman ringan atau sastra serius
2. **Halaman 1 = hook**: Pembaca Indonesia tidak sabar — beri konflik atau misteri di 3 paragraf pertama
3. **Karakter relatable**: Gunakan nama, setting, dan situasi yang dikenal pembaca (sekolah Indonesia, kos, kampus, warung kopi)
4. **Emosi langsung**: Jangan terlalu subtle — pembaca Indonesia ingin MERASAKAN emosi karakter
5. **Dialog alami**: Baca dialog dengan suara keras — jika kedengarannya seperti buku pelajaran, tulis ulang

## Revision Workflow

### Three-Pass Revision

```
PASS 1: STRUCTURE (10,000 ft view)
- Does the plot make logical sense?
- Does every scene advance the story?
- Are act breaks at the right place?
- Does the ending resolve the central question?
- Action: Move, cut, or merge scenes. DON'T fix prose yet.

PASS 2: SCENE CRAFT (1,000 ft view)
- Does each scene have: goal, conflict, disaster / decision?
- Is POV consistent?
- Does dialogue have subtext?
- Is pacing right? (Fast for action, slow for reflection)
- Action: Rewrite weak scenes. Enhance tension.

PASS 3: LINE EDIT (street level)
- Kill adverbs (-ly words) — use stronger verbs instead
- Remove filter words (saw, heard, noticed, felt, seemed)
- Vary sentence length for rhythm
- Read ALOUD for awkward phrasing
- Check for repeated words on the same page
- Action: Cut 10% of word count.
```

### Filter Words to Kill

| Weak | Strong |
|------|--------|
| He saw the dog run | The dog bolted |
| She heard footsteps | Footsteps thudded |
| He felt cold | Cold bit his fingers |
| She seemed angry | She slammed the door |
| He noticed the door was open | The door stood open |
| She thought he was lying | The lie hung between them |

---

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "AI can't write novels, so why try?" | AI is a co-pilot — outlines, character profiles, pacing analysis, and revision suggestions all amplify the human writer's craft |
| "Just start writing and see what happens" | A novel is a 60K–150K word system. Without structure, you'll hit the soggy middle and stall. Plan beats pants. |
| "Show-don't-tell is for beginners" | Every published novel that works uses the iceberg principle. Readers FEEL the emotion; they don't read a report of it. |
| "Cliffhangers are cheap/trite" | A hook isn't a gimmick — it's narrative momentum. A chapter without a reason to turn the page is a break point where the reader puts the book down forever. |
| "Character profiles are a waste of time" | A character who sounds like every other character is a flat character. Profiles ensure distinct voices, consistent arcs, and meaningful growth. |
| "World-building means 50 pages of history" | The iceberg: 10% shows, 90% is known by the author. If you're explaining instead of experiencing, you're telling, not showing. |
| "Web novels have no literary merit" | The best web novels (Lord of the Mysteries, Reverend Insanity) are masterclasses in pacing, chapter hooks, and reward systems. |
| "Kids books are easy — just short words and rhymes" | A successful picture book is a 32-page poem with a dramatic arc — every word earns its place, the page turn creates suspense, and the read-aloud test is merciless. It's hard. |
| "Indonesian novels are just translations of Western ones" | Pasar Indonesia memiliki ekspektasi sendiri: ending happy/hopeful, emosi langsung, dialog mendominasi narasi, dan moral/pesan sering diharapkan. Indonesian readers want a different reading experience. |
| "Picture books are for the parent, not the child" | The best picture books work on two levels — the child enjoys the story and repetition; the parent appreciates the wit, irony, or deeper theme. Both must be satisfied. |


## Verification

### Checklist

- [ ] Story structure chosen and mapped (Three-Act / Hero's Journey / Save the Cat / Kishōtenketsu / Web Novel)
- [ ] Each major character has GMC documented and an arc planned
- [ ] Each chapter ends with a hook (question, revelation, or incoming threat)
- [ ] Every scene contains conflict (even subtle internal tension)
- [ ] World is shown through character experience, not narrative info-dumps
- [ ] Dialogue passes the "cover the names" test — voices are distinct
- [ ] Auto-validation run on each chapter: word count, conflict, cliffhanger, show-don't-tell
- [ ] At least 3 face-slap / tension-release moments per arc (web novel) or comparable dramatic beats
- [ ] Revision plan: structural pass → scene pass → line pass
- [ ] Continuity: character traits, setting details, and timeline are consistent
- [ ] (Picture Book) Read-aloud test passed — every word earns its place when spoken aloud
- [ ] (Picture Book) Page turn creates a reveal — text on page N makes reader NEED page N+1
- [ ] (Middle Grade) Protagonist is 9–12 and solves the core problem themselves
- [ ] (Middle Grade) Themes accessible to 8–12 year olds (friendship, family, justice, identity)
- [ ] (Bahasa Indonesia) Narasi baku + dialog natural — tidak tercampur dalam satu paragraf
- [ ] (Bahasa Indonesia) Setting dan situasi relatable untuk pembaca Indonesia
- [ ] (Bahasa Indonesia) Moral ending atau hopeful ending sesuai genre
- [ ] (Bahasa Indonesia) Bab pertama: hook dalam 3 paragraf pertama — pembaca Indonesia tidak sabar

## When to Use

Use this skill when writing novels, short stories, or any fiction. Covers the full pipeline: outlining → character creation → world-building → drafting (with interrupt-resume and parallel writing) → auto-validation → revision. Best suited for novel-length fiction (40K–150K words), web serials, picture books (300–800 words), middle grade novels (25K–50K words), and Indonesian-language fiction for the pasar penerbitan Indonesia. For kids books, follow the Kids Book Writing section for age-appropriate craft. For Indonesian fiction, follow the Buku Bahasa Indonesia section for market-specific conventions.

## Process


See the parent skill for authoritative workflow documentation.
