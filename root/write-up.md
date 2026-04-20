# Write-Up: Daily Reflection Tree — Design Rationale

**Candidate:** [Your Name]
**Assignment:** DT Fellowship — Daily Reflection Tree (Part A)

---

## 1. Why These Questions

The three axes each required a different interrogation strategy.

**Axis 1 (Locus)** needed questions that surface how the employee *narrated* their day to themselves — not what happened, but the grammar of their interpretation. The three questions follow an arc: orientation at the start of day (Q1_A), first instinct when things broke down (Q1_B), and whether they stepped into or away from a moment of agency (Q1_C). Together they build a picture of habitual posture, not a single incident. A person can have a bad day and still lean "victor" — what matters is the internal stance, not the outcome.

**Axis 2 (Orientation)** is the hardest axis to surface honestly because entitlement is largely invisible to the person holding it (Campbell et al., 2004). The questions were designed to make the contrast feel natural rather than loaded. Q2_A asks about a real interaction without naming the spectrum. Q2_B focuses on emotional tone after effort — pride vs irritation. Q2_C makes the belief explicit. A person with a contribution orientation won't find Q2_C leading; a person with entitlement orientation will feel seen by it. That discomfort — not shame — is the productive output.

**Axis 3 (Radius)** follows Maslow's later work on self-transcendence (1969), which positioned outward concern not as altruism but as the most mature form of self-actualization. The questions progressively widen the frame: Q3_A asks who was in mind during challenges (cognitive), Q3_B asks whether the employee paused to consider ripple effects (behavioral), and Q3_C asks for a retrospective judgment of their own radius. Options within each question are ordered narrow-to-wide (A = self, D = everyone), which allows a runner to see their own answer on a spectrum without being told where they land.

---

## 2. How the Branching Was Designed

The tree uses a **signal-tally model** rather than hard branching at every question. Each option on each question emits one of two signals per axis (e.g., `axis1:victor` or `axis1:victim`). Decision nodes collect those tallies and route to the dominant-pole reflection at the end of each axis.

This was a deliberate trade-off. An alternative design would branch after every question, creating a tree that doubles in width at each node — resulting in 2^9 = 512 possible paths for nine questions. That scale would be unmanageable to write well, and would produce many reflection nodes no one ever sees. The tally model instead compresses the branching into four decision points (one per axis plus one for the final summary), which keeps the number of reflection nodes small enough to write with genuine care.

The cost of this trade-off is that two employees with exactly opposite distributions — one who answered victim/victim/victor and another who answered victor/victor/victim — could theoretically receive the same axis-1 reflection. In practice, the signal totals at three questions make a true tie unlikely. And ties always resolve toward the growth pole (victor, contribution, altro) — not because the growth pole is "better," but because the reflection for the growth pole offers less friction and is therefore more likely to land cleanly when the employee is genuinely on the fence.

The final decision node (D_SUMMARY) checks whether all three axes resolved to the growth pole simultaneously. This was included because a three-for-three day feels qualitatively different and deserves a different close — not a reward, but an acknowledgment that feels accurate rather than generic.

---

## 3. Psychological Sources

| Framework | Application in Tree |
|---|---|
| Rotter's Locus of Control (1954) | Foundation of Axis 1. Options in Q1_A–Q1_C map to internal (victor) vs external (victim) locus. |
| Dweck's Growth Mindset (2006) | Reinforces Axis 1 framing — the "victim" pole is not a character flaw but a fixed-mindset interpretation of events that can be examined. |
| Campbell et al. Psychological Entitlement Scale (2004) | Axis 2. Entitlement is operationalized as expectation decoupled from contribution — captured through Q2_B (emotional reaction to effort) and Q2_C (explicit belief about desert). |
| Organ's Organizational Citizenship Behavior (1988) | Axis 2 "contribution" pole — discretionary effort that goes beyond role requirements, not contingent on recognition. |
| Maslow's Self-Transcendence (1969) | Foundation of Axis 3. The option ordering in Q3_A–Q3_C deliberately maps to Maslow's hierarchy from ego-bound to self-transcendent concern. |
| Batson's Perspective-Taking (2011) | Q3_B and Q3_C operationalize perspective-taking as a behavioral check (did you actually pause to consider others?) rather than as a stated value. |

---

## 4. What I Would Improve With More Time

**A. Branching after Q1_A.** The current design routes everyone to the same Q1_B regardless of how they described their morning. With more time, I would write separate Q1_B variants: one framed around protecting what went well (for Victor-leaning openers) and one framed around what got in the way (for Victim-leaning openers). This would make the conversation feel more responsive and less like a survey.

**B. Tie-breaking logic.** Currently, ties resolve to the growth pole by default. A more careful design would surface the tie explicitly — something like "You were almost exactly split on this one. That ambiguity is worth noticing." A special `reflection:tie` node type could handle this.

**C. Axis 2 tone calibration.** The entitlement reflection (R2_ENTITLEMENT) is the hardest to write well. The current version is warm but still somewhat pointed. A real deployment would want this tested against actual employees — the goal is that someone on the entitlement end doesn't feel shamed, just seen. That calibration benefits from iteration with real feedback.

**D. Longitudinal state.** In a real product, the tree would compare today's dominant axes against a rolling average across the past 7 or 30 days. A single session captures a snapshot; the more interesting question is trend. "You've been leaning victim for three days in a row — that's worth paying attention to" is a richer reflection than any single session can produce.
