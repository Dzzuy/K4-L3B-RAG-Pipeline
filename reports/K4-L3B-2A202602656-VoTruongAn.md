# Individual contribution report — Võ Trường An

- Student ID: 2A202602656
- Team: Nova

## Work completed

| Module | Contribution | Evidence |
| --- | --- | --- |
| Task 10 | Context formatting, answer generation, source citations, and safe refusal. | `src/task10_generation.py` |
| User interface | Streamlit chat interface, retrieval visualisation, and source display. | `app.py` |

## Technical decisions

The generator receives labelled context containing the title and source, so an answer can show a source the user can inspect. When retrieval returns no verifiable context, it returns a fixed safe refusal instead of an unsupported answer.

## Check and limitation

The generation contract checks source-aware context formatting and a safe refusal. Live model responses require a local API key in `.env`; without one, the app uses its local extractive fallback.
