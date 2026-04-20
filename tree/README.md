# Daily Reflection Tree

**DT Fellowship Assignment — Part A Submission**

---

## Repository Structure

```
/tree/
  reflection-tree.json     ← The complete tree as structured data (Part A)
  tree-diagram.md          ← Mermaid flowchart — paste into mermaid.live to render

write-up.md                ← Design rationale (questions, branching, psychology, improvements)
README.md                  ← This file
```

---

## How to Read the Tree

The tree is a flat array of nodes in `reflection-tree.json`. Each node has a `type` that determines how it behaves. Here's a quick reference:

| Type | Visible to employee? | What it does |
|---|---|---|
| `start` | Yes | Opens the session. Auto-advances. |
| `question` | Yes | Displays question text + fixed options. Employee picks one. Each option has a `signal` that tallies toward an axis pole. |
| `decision` | No | Internal routing. Reads accumulated signal tallies and routes to the correct next node. |
| `reflection` | Yes | Shows a reframe based on the path taken. Employee clicks Continue. |
| `bridge` | Yes | Short transition sentence between axes. Auto-advances. |
| `summary` | Yes | End-of-session synthesis using `{placeholder}` interpolation from state. |
| `end` | Yes | Closes session. |

---

## How State Works

As the employee answers questions, each selected option emits a `signal` — a tag that increments a counter in state:

```
"signal": "axis1:victor"   →   state.axis1.victor += 1
"signal": "axis2:entitlement" →  state.axis2.entitlement += 1
```

At the end of each axis, a `decision` node compares the two counters and routes to the dominant-pole reflection:

```json
{
  "if": "state.axis1.victor >= state.axis1.victim",
  "set": "axis1.dominant = 'victor'",
  "next": "R1_VICTOR"
}
```

The summary nodes use `{axis1.dominant}`, `{axis2.dominant}`, `{axis3.dominant}` as placeholders — these are replaced at runtime with the dominant pole values set by the decision nodes.

---

## How to Trace a Path (Example)

Employee answers: Q1_A=B, Q1_B=C, Q1_C=C → all victim signals → D1_REFLECT routes to R1_VICTIM.

Employee answers: Q2_A=A, Q2_B=C, Q2_C=A → all contribution signals → D2_REFLECT routes to R2_CONTRIBUTION.

Employee answers: Q3_A=D, Q3_B=D, Q3_C=D → all altro signals → D3_REFLECT routes to R3_ALTROCENTRIC.

D_SUMMARY: axis1.dominant=victim → condition "all three = growth poles" is FALSE → routes to SUMMARY_DEFAULT.

Full path: START → Q1_A → Q1_B → Q1_C → D1_REFLECT → R1_VICTIM → BRIDGE_1_2 → Q2_A → Q2_B → Q2_C → D2_REFLECT → R2_CONTRIBUTION → BRIDGE_2_3 → Q3_A → Q3_B → Q3_C → D3_REFLECT → R3_ALTROCENTRIC → BRIDGE_3_SUMMARY → D_SUMMARY → SUMMARY_DEFAULT → END

---

## Viewing the Diagram

1. Open [mermaid.live](https://mermaid.live)
2. Paste the contents of `tree-diagram.md` (without the triple-backtick fences)
3. The full branching structure renders as a flowchart

---

## Node Count Summary

| Type | Count |
|---|---|
| start | 1 |
| question | 9 |
| decision | 4 |
| reflection | 6 |
| bridge | 3 |
| summary | 2 |
| end | 1 |
| **Total** | **26** |

All minimum requirements exceeded:
- ✅ 25+ total nodes (26)
- ✅ 8+ question nodes (9)
- ✅ 4+ decision nodes (4)
- ✅ 4+ reflection nodes (6)
- ✅ 2+ bridge nodes (3)
- ✅ All 3 axes covered in sequence
- ✅ 4 options per question
- ✅ 1+ summary node (2)
