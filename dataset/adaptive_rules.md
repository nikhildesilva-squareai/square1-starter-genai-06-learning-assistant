# Adaptive rules — pedagogy notes (the logic to implement)

These are the rules the **Personalised Learning Assistant** runs on. They are
deterministic on purpose: the offline contract tests check exactly this maths,
with **no LLM call** involved. The model is only used for the *explanation* text.

## Mastery state
Per learner, mastery is a number in `[0, 1]` for each topic. `0` = no idea,
`1` = mastered. A learner profile seeds the starting mastery (high on
`known_topics`, low on `weak_topics`).

## update_mastery(state, topic, correct) — exponential moving average
After the learner answers a question on `topic`:

```
target  = 1.0 if correct else 0.0
ALPHA   = 0.30          # learning rate
new     = (1 - ALPHA) * old + ALPHA * target
```

- A **correct** answer moves the score **up** (toward 1).
- An **incorrect** answer moves it **down** (toward 0).
- Clamp the result to `[0, 1]`. The move is strictly monotone: correct ⇒ new > old
  (unless already 1.0); incorrect ⇒ new < old (unless already 0.0).

## next_item(state, bank) — weakest-topic, easiest-unmastered
Pick the next question so the learner practises where they are weakest:

1. Find the topic with the **lowest** mastery in `state` (the weakest topic).
2. From `bank`, keep questions whose `topic` is that weakest topic.
3. Among those, prefer the lowest difficulty first (`easy` < `medium` < `hard`),
   then a stable order by question `id`.
4. Return that single question. (If the weakest topic has no questions in the
   bank, fall back to the next-weakest topic.)

The key, testable property: **the returned item's `topic` is the weakest topic
in the state.**

## build_explanation_prompt(item, state) — what the LLM sees
Assemble a prompt string for the tutor explanation. It MUST include:

- the question text (`item["question"]`),
- the learner's **level** (`state["level"]`), so the explanation is pitched right.

It SHOULD also mention the topic and ask for a short, level-appropriate
explanation. The LLM call itself is mocked in tests — only the prompt content
is asserted.
