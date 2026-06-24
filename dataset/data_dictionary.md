# Data dictionary — sample material

Three files for the **Personalised Learning Assistant**. **Synthetic — generated
by Square 1 AI, free for learners.** No personal data, no licence risk.

> ⚠️ This is *sample material*, not a tidy training table. A learner profile has
> a real, recoverable signal — mastery is high on `known_topics` and low on
> `weak_topics` — so a correct tutor picks practice from the weak topics and
> can move a weak score up over time. The adaptive logic is the project.

## `learner_profiles.json` — 60 learners

| Field | Type | Description |
|---|---|---|
| `learner_id` | string | Learner identifier, e.g. `L207`. |
| `level` | string | `beginner` \| `intermediate` \| `advanced`. Pitch explanations to this. |
| `known_topics` | string[] | Topics this learner is strong on (high seed mastery). |
| `weak_topics` | string[] | Topics this learner is weak on (low seed mastery). |
| `mastery` | object | `topic -> score` in `[0,1]`. The state your tutor updates. |

## `question_bank.json` — 120 questions (8 topics × 3 difficulties × 5)

| Field | Type | Description |
|---|---|---|
| `id` | string | Question identifier, e.g. `Q1042`. |
| `topic` | string | One of the 8 topics (see below). |
| `difficulty` | string | `easy` \| `medium` \| `hard`. |
| `question` | string | The prompt shown to the learner (difficulty-tagged). |
| `answer` | string | The correct answer (used for grading + the explanation). |

**Topics:** `prompt_basics`, `few_shot_prompting`, `chain_of_thought`,
`tool_use`, `rag_fundamentals`, `embeddings`, `evaluation`,
`safety_and_guardrails`.

## `adaptive_rules.md`
The pedagogy notes — the exact mastery-update and item-selection rules to
implement. The offline contract tests check this maths directly (LLM mocked).

**What to build:** track per-topic **mastery**; on each answer, `update_mastery`
nudges the topic's score up (correct) or down (incorrect); `next_item` selects
practice from the learner's **weakest** topic; `build_explanation_prompt`
assembles the prompt for the LLM tutor (question + learner level).

_Licence: Synthetic, Square 1 AI-owned. No attribution required. Regenerate with
`generate_dataset.py` (seed 42)._
