# Personalised Learning Assistant — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Generative AI · Project 6.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) and is the **same standardized dataset every learner uses** — so results are comparable. It is 100% synthetic and Square 1-owned (no third-party or personal data). You can also download it as a single file from the project page on Square 1.

To run the commands below, copy the files into `data/` (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`.

MIT licensed — fork it, build on it, put it in your portfolio.

---

# Personalised Learning Assistant — starter

Starter for Square 1 AI **Generative AI · Project 6**. Build an adaptive AI tutor:
track mastery, pick the next best item, and explain it at the learner's level.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...                 # never commit this
```

## Get the data
Download the sample material (`learner_profiles.json`, `question_bank.json`,
`adaptive_rules.md`) from your project page (Resources → Dataset) into `dataset/`.

## Your task
Three tests define the contract — they fail until you implement the stubs in
`tutor/core.py`:
```bash
pytest -q
python -m tutor.cli            # runs a short adaptive session (needs the data + key)
```
- `update_mastery(state, topic, correct)` → moves the topic's score up/down (EMA, clamped to `[0,1]`).
- `next_item(state, bank)` → returns one question from the learner's **weakest** topic.
- `build_explanation_prompt(item, state)` → a prompt string containing the question + learner level.

Then call the **Anthropic SDK** to generate the explanation. Use current model ids
only — `claude-sonnet-4-6` (default), `claude-haiku-4-5-20251001` (cheap). **Never
`claude-3-*`.** The LLM is mocked in the tests, so the core logic must be correct
on its own. Full brief, rubric, and references are on your Square 1 project page.
MIT licensed.
