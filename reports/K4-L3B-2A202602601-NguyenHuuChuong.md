# Individual contribution report — Nguyễn Hữu Chương

- Student ID: 2A202602601
- Team: Nova

## Work completed

| Module | Contribution | Evidence |
| --- | --- | --- |
| Task 4 | Document loading, recursive chunking, multilingual embeddings, and ChromaDB indexing. | `src/task4_chunking_indexing.py` |
| Task 5 | Dense semantic search using the shared embedding and collection contract. | `src/task5_semantic_search.py` |
| Integration support | Preserved the document/chunk data contract used by downstream retrieval. | `src/contracts.py` |

## Technical decisions

The pipeline uses `paraphrase-multilingual-MiniLM-L12-v2` because the corpus and questions are Vietnamese while the model still produces compact 384-dimensional vectors. Recursive chunks of 750 characters with 100-character overlap keep a policy condition together while retaining a small bridge across boundaries.

## Check and limitation

The shared embedding path is exercised by the semantic-search contract test. Re-index after changing the corpus, chunking settings, or embedding model because vector collections are generated artifacts.
