# Individual contribution report — Phạm Quốc Đạt

- Student ID: 2A202602384
- Team: Nova

## Work completed

| Module | Contribution | Evidence |
| --- | --- | --- |
| Corpus | Organized legal policy files, support-article data, and standardized Markdown. | `data/landing/`, `data/standardized/` |
| Golden set | Prepared grounded evaluation questions, expected answers, and expected context. | `group_project/evaluation/golden_dataset.json` |
| Evaluation | Implemented A/B evaluation artifacts and result analysis. | `group_project/evaluation/eval_pipeline.py`, `RESULT.md`, `eval_run_results.json` |

## Technical decisions

The golden cases use corpus-grounded expected context so retrieval is measured against a traceable source. Config A and B share the same set and generator settings so the comparison isolates the retrieval strategy.

## Check and limitation

The acceptance test confirms at least 15 complete golden cases and the completed evaluation report. The recorded evaluation values are retained as run artifacts; rerun the script after any corpus or retrieval configuration change.
