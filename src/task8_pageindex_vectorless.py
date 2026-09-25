"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
import hashlib
import time
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
PAGEINDEX_PDF_DIR = Path(__file__).parent.parent / "pageindex_pdfs"
DOCUMENT_IDS: dict[str, str] = {}
DOCUMENT_METADATA: dict[str, dict] = {}
RETRIEVAL_TIMEOUT_SECONDS = 10.0


def _get_client():
    api_key = os.getenv("PAGEINDEX_API_KEY", PAGEINDEX_API_KEY)
    if not api_key:
        return None

    from pageindex import PageIndexClient

    return PageIndexClient(api_key=api_key)


def _provider_path(source_path: Path) -> Path:
    if source_path.suffix.lower() == ".pdf":
        return source_path

    from fpdf import FPDF

    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if not font_path.is_file():
        raise RuntimeError("PageIndex Markdown conversion requires DejaVuSans.ttf")

    source_key = source_path.relative_to(STANDARDIZED_DIR).as_posix()
    filename = f"{source_path.stem}-{hashlib.sha256(source_key.encode()).hexdigest()[:12]}.pdf"
    pdf_path = PAGEINDEX_PDF_DIR / filename
    if pdf_path.exists() and pdf_path.stat().st_mtime >= source_path.stat().st_mtime:
        return pdf_path

    PAGEINDEX_PDF_DIR.mkdir(parents=True, exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", str(font_path))
    pdf.set_font("DejaVu", size=10)
    pdf.multi_cell(0, 5, source_path.read_text(encoding="utf-8"))
    pdf.output(str(pdf_path))
    return pdf_path


def _source_metadata(source_path: Path) -> dict:
    relative_path = source_path.relative_to(STANDARDIZED_DIR)
    return {
        "source": relative_path.as_posix(),
        "title": source_path.stem,
        "doc_type": "legal" if "legal" in relative_path.parts else "news",
        "url": None,
    }


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    client = _get_client()
    if client is None or not STANDARDIZED_DIR.exists():
        return

    source_paths = sorted(
        path
        for path in STANDARDIZED_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".pdf"}
    )
    for source_path in source_paths:
        source_key = source_path.relative_to(STANDARDIZED_DIR).as_posix()
        if source_key in DOCUMENT_IDS:
            continue
        response = client.submit_document(str(_provider_path(source_path)))
        document_id = response.get("doc_id")
        if not isinstance(document_id, str) or not document_id:
            raise RuntimeError("PageIndex submit_document returned no doc_id")
        DOCUMENT_IDS[source_key] = document_id
        DOCUMENT_METADATA[document_id] = _source_metadata(source_path)


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if top_k <= 0:
        return []

    client = _get_client()
    if client is None:
        return []

    upload_documents()
    retrieved_nodes: list[tuple[str, dict]] = []
    for document_id in DOCUMENT_METADATA:
        if not client.is_retrieval_ready(document_id):
            continue
        response = client.submit_query(document_id, query)
        retrieval_id = response.get("retrieval_id")
        if not isinstance(retrieval_id, str) or not retrieval_id:
            raise RuntimeError("PageIndex submit_query returned no retrieval_id")

        deadline = time.monotonic() + RETRIEVAL_TIMEOUT_SECONDS
        while True:
            response = client.get_retrieval(retrieval_id)
            status = response.get("status")
            if status == "completed":
                nodes = response.get("retrieved_nodes", [])
                if isinstance(nodes, list):
                    retrieved_nodes.extend((document_id, node) for node in nodes if isinstance(node, dict))
                break
            if status == "failed":
                break
            if time.monotonic() >= deadline:
                break
            time.sleep(0.25)

    results = []
    seen_ids = set()
    for rank, (document_id, node) in enumerate(retrieved_nodes, start=1):
        node_id = node.get("node_id")
        content = node.get("text")
        if not isinstance(node_id, str) or not node_id or not isinstance(content, str) or not content.strip():
            continue
        result_id = f"{document_id}::node-{node_id}"
        if result_id in seen_ids:
            continue
        seen_ids.add(result_id)
        metadata = dict(DOCUMENT_METADATA[document_id])
        title = node.get("title")
        if isinstance(title, str) and title.strip():
            metadata["title"] = title
        metadata["chunk_index"] = rank - 1
        results.append(
            {
                "id": result_id,
                "content": content,
                "score": 1.0 / rank,
                "metadata": metadata,
                "retrieval_method": "pageindex",
            }
        )
        if len(results) == top_k:
            break
    return results


if __name__ == "__main__":
    upload_documents()
