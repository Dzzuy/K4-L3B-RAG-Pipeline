# Individual contribution report — Phạm Đình Duy

- Student ID: 2A202602913
- Team: Nova

## Work completed

| Module | Contribution | Evidence |
| --- | --- | --- |
| Tasks 6–7 | BM25 lexical retrieval and Reciprocal Rank Fusion (RRF). | `src/task6_lexical_search.py`, `src/task7_reranking.py` |
| Tasks 8–9 | PageIndex fallback and dense/BM25 retrieval orchestration. | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` |
| Integration | Final repository review, cache cleanup, contract and acceptance testing. | `TEAMMATES.md`, tests, `.gitignore` |

## Technical decisions

RRF combines ranks instead of adding dense and BM25 scores because the two scores have different scales. The fallback gate uses the original dense cosine score because an RRF score is only a rank signal. This keeps the fallback decision meaningful and matches the module contract.

## Check and limitation

The final suite covers BM25, RRF, dense-score fallback, and provider-error safety. PageIndex remains optional at runtime: an unavailable provider returns hybrid results instead of crashing the application.
