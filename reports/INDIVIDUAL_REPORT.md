# Individual contribution report

## Thông tin

- Họ và tên: Phạm Đình Duy
- Mã học viên: 2A202602913
- Nhóm: Nova
- Repository/branch: `K4-L3B-RAG-Pipeline` / `feat/duy-hybrid-retrieval`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| BM25 lexical retrieval | Tạo BM25 index trên chunk corpus, trả SearchResult có metadata, ID unique và sort giảm dần. | `src/task6_lexical_search.py` | Done |
| RRF hybrid retrieval | Fuse dense và BM25 bằng `1 / (k + rank)`, không cộng trực tiếp hai loại score và không sửa input. | `src/task7_reranking.py` | Done |
| PageIndex fallback | Thêm upload/cache ID trong memory, chuyển Markdown thành PDF tạm, timeout polling và map node về SearchResult. | `src/task8_pageindex_vectorless.py` | Partial |
| Retrieval orchestration | Chạy dense + BM25, RRF đúng một lần, dùng dense cosine score gốc để quyết định fallback và không crash khi provider lỗi. | `src/task9_retrieval_pipeline.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Dùng RRF thay vì cộng cosine score với BM25 score.

   **Lý do/evidence:** Hai score có thang đo khác nhau. Contract của nhóm yêu cầu `sum(1 / (k + rank))`, với rank bắt đầu từ 1. Test RRF pass và chunk có mặt ở cả hai list sẽ nhận điểm từ cả hai rank.

   **Trade-off:** RRF không giữ độ lớn cosine score, nên không dùng score này để quyết định fallback.

2. **Quyết định:** Quyết định fallback bằng dense score gốc, không dùng BM25/RRF/PageIndex score.

   **Lý do/evidence:** `retrieve()` lấy `dense[0]["score"]` trước khi fuse. Contract test kiểm tra low dense score vẫn gọi fallback, còn dense score cao thì không gọi PageIndex.

   **Trade-off:** Ngưỡng `0.3` chỉ là default của starter. Chưa thể coi là ngưỡng cuối cho Shopee khi corpus và dense retrieval chưa xong.

## Kiểm thử và kết quả

- Test đã dùng: `python -m pytest tests/test_contracts.py -q -k 'lexical or rrf or retrieve'`
- Kết quả: `5 passed, 10 deselected`.
- Import check cho Task 6–9 pass, không gọi PageIndex/network khi import.
- Test không có `PAGEINDEX_API_KEY` trả `[]`, nên retrieval pipeline giữ hybrid result.
- Full contract suite hiện là `12 passed, 3 failed`. Ba lỗi ở Task 4 chunking, Task 5 semantic search và Task 10 generation vẫn là starter `NotImplementedError`, không thuộc phần tôi phụ trách.
- Lỗi BM25 với corpus rất nhỏ đã được phát hiện: score có thể bằng 0 dù keyword match. Tôi lọc theo token match thay vì bỏ toàn bộ score `<= 0`.

## Điều còn hạn chế

- PageIndex chưa test thật vì chưa có standardized Shopee corpus, `PAGEINDEX_API_KEY`, và Task 4/5 của thành viên khác chưa tích hợp.
- Nếu có thêm thời gian, thay đổi đầu tiên là chạy end-to-end trên corpus Shopee thật, kiểm tra chunk ID giữa dense/BM25 và calibrate `SCORE_THRESHOLD` bằng một query in-domain và một query out-of-domain.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-25
- Tên thành viên: Phạm Đình Duy
