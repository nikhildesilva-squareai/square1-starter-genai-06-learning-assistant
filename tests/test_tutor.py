"""Contract tests — fail against the starter stubs; make them pass.

Tiny in-test data only (never the big JSON). The LLM is never called here —
build_explanation_prompt just returns a string, so there is nothing to mock.
"""
from tutor import update_mastery, next_item, build_explanation_prompt


def _state() -> dict:
    # tool_use is the weakest topic; prompt_basics is strong.
    return {
        "learner_id": "L999",
        "level": "beginner",
        "known_topics": ["prompt_basics"],
        "weak_topics": ["tool_use"],
        "mastery": {"prompt_basics": 0.80, "tool_use": 0.20, "embeddings": 0.50},
    }


def _bank() -> list[dict]:
    return [
        {"id": "Q1", "topic": "prompt_basics", "difficulty": "easy",
         "question": "[easy] What is a system prompt?", "answer": "Role and behaviour"},
        {"id": "Q2", "topic": "tool_use", "difficulty": "hard",
         "question": "[hard] Who runs a tool call?", "answer": "Your application"},
        {"id": "Q3", "topic": "tool_use", "difficulty": "easy",
         "question": "[easy] What is a tool?", "answer": "A function it can call"},
    ]


def test_update_mastery_moves_score_up_and_down():
    # Correct answer raises the weak topic; incorrect lowers a strong one.
    up = update_mastery(_state(), "tool_use", correct=True)
    assert up["mastery"]["tool_use"] > 0.20
    assert up["mastery"]["tool_use"] <= 1.0

    down = update_mastery(_state(), "prompt_basics", correct=False)
    assert down["mastery"]["prompt_basics"] < 0.80
    assert down["mastery"]["prompt_basics"] >= 0.0


def test_next_item_picks_from_weakest_topic():
    item = next_item(_state(), _bank())
    assert item["topic"] == "tool_use"  # the weakest topic in the state


def test_build_explanation_prompt_includes_item_and_level():
    item = _bank()[2]  # the easy tool_use question
    prompt = build_explanation_prompt(item, _state())
    assert item["question"] in prompt   # the item
    assert "beginner" in prompt          # the learner's level
