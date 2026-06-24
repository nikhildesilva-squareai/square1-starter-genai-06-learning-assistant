"""
CLI:  python -m tutor.cli

Runs a short adaptive session for one learner: pick the weakest-topic item,
ask the Anthropic model to explain it at the learner's level, then simulate an
answer and update mastery — showing the weak topic improve.

Reads ANTHROPIC_API_KEY from the environment. Uses current model ids only.
"""
import json
import os

from .core import update_mastery, next_item, build_explanation_prompt

DATA = "dataset"
DEFAULT_MODEL = "claude-sonnet-4-6"          # default
CHEAP_MODEL = "claude-haiku-4-5-20251001"    # cheap/fast — never claude-3-*


def explain(prompt: str, model: str = CHEAP_MODEL) -> str:
    """Call the Anthropic SDK to generate the explanation for `prompt`."""
    from anthropic import Anthropic  # imported here so tests don't need the key

    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    msg = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


def main() -> None:
    with open(os.path.join(DATA, "learner_profiles.json"), encoding="utf-8") as f:
        learner = json.load(f)[0]
    with open(os.path.join(DATA, "question_bank.json"), encoding="utf-8") as f:
        bank = json.load(f)

    item = next_item(learner, bank)
    topic = item["topic"]
    print(f"Learner {learner['learner_id']} ({learner['level']}) — "
          f"weakest topic: {topic} @ {learner['mastery'][topic]:.2f}")

    prompt = build_explanation_prompt(item, learner)
    print("\nExplanation:\n" + explain(prompt))

    # Simulate a correct answer and show mastery climb.
    before = learner["mastery"][topic]
    update_mastery(learner, topic, correct=True)
    after = learner["mastery"][topic]
    print(f"\nAnswered correctly — {topic} mastery {before:.2f} -> {after:.2f}")


if __name__ == "__main__":
    main()
