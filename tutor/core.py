"""
The deterministic adaptive core. NO LLM calls live here — the tutor's decisions
(track mastery, pick the next item, assemble the explanation prompt) must be
correct and testable on their own. The model only writes the explanation text,
using the prompt that build_explanation_prompt returns. Tests define the contract.

`state` is a learner dict like the ones in dataset/learner_profiles.json:
    {
      "learner_id": "L207",
      "level": "intermediate",
      "known_topics": [...],
      "weak_topics": [...],
      "mastery": {"prompt_basics": 0.8, "tool_use": 0.2, ...},  # topic -> [0,1]
    }
`bank` is the list of questions from dataset/question_bank.json.
"""
from __future__ import annotations

ALPHA = 0.30  # learning rate for the mastery EMA


def update_mastery(state: dict, topic: str, correct: bool) -> dict:
    """Update the learner's mastery for `topic` after an answer.

    TODO: with target = 1.0 if correct else 0.0, set
        new = (1 - ALPHA) * old + ALPHA * target
    Clamp to [0, 1]. A correct answer must move the score UP, an incorrect
    answer DOWN. Return the (mutated or new) state.
    """
    raise NotImplementedError("Implement update_mastery")


def next_item(state: dict, bank: list[dict]) -> dict:
    """Pick the next question — from the learner's WEAKEST topic.

    TODO:
      1. find the topic with the lowest value in state["mastery"],
      2. from `bank`, return one question whose "topic" is that weakest topic
         (prefer difficulty easy < medium < hard, then a stable order by id).
    The returned item's "topic" MUST equal the weakest topic.
    """
    raise NotImplementedError("Implement next_item")


def build_explanation_prompt(item: dict, state: dict) -> str:
    """Build the prompt string for the LLM tutor explanation.

    TODO: return a prompt that INCLUDES both
      - the question text: item["question"], and
      - the learner's level: state["level"]
    so the explanation is pitched to the learner. (The LLM call is mocked in
    tests — only the prompt content is asserted.)
    """
    raise NotImplementedError("Implement build_explanation_prompt")
