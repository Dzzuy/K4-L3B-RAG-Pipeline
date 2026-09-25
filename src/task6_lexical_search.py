"""
Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""


CORPUS: list[dict] = []


def build_bm25_index(corpus: list[dict]):
    """Tạo BM25 index từ cùng corpus chunks của Task 4."""
    from rank_bm25 import BM25Okapi

    tokenized_corpus = [item["content"].lower().split() for item in corpus]
    return BM25Okapi(tokenized_corpus)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    if top_k <= 0:
        return []

    corpus = CORPUS
    if not corpus:
        from .task4_chunking_indexing import chunk_documents, load_documents

        corpus = chunk_documents(load_documents())
    if not corpus:
        return []

    query_tokens = query.lower().split()
    scores = build_bm25_index(corpus).get_scores(query_tokens)
    ranked_indices = sorted(range(len(corpus)), key=lambda index: (-scores[index], index))

    results = []
    seen_ids = set()
    for index in ranked_indices:
        score = float(scores[index])
        item = corpus[index]
        if not set(query_tokens).intersection(item["content"].lower().split()):
            continue
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])
        results.append(
            {
                "id": item["id"],
                "content": item["content"],
                "score": score,
                "metadata": dict(item["metadata"]),
                "retrieval_method": "bm25",
            }
        )
        if len(results) == top_k:
            break
    return results


if __name__ == "__main__":
    for result in lexical_search("test query", top_k=3):
        print(result)
