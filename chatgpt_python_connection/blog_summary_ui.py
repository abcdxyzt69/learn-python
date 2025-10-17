# app.py
# ──────────────────────────────────────────────────────────────
# ỨNG DỤNG TÓM TẮT BLOG BẰNG STREAMLIT
# Input: URL bài viết
# Output: Tóm tắt gọn bằng bullet points từ mô hình ngôn ngữ (LLM)
# ──────────────────────────────────────────────────────────────

import streamlit as st
import re
import textwrap

# Import các module xử lý có sẵn từ project gốc
from helpers import get_article_from_url
from llm import llm_generate_text
from prompts.blog_prompts import blog_bullet_summary_prompt


# ========================
# 1️⃣ CẤU HÌNH TRANG
# ========================
# Giúp giao diện hiển thị đẹp, tối ưu không gian
st.set_page_config(page_title="Tóm tắt Blog bằng AI", page_icon="🧠", layout="wide")


# ========================
# 2️⃣ CÁC HẰNG SỐ MẶC ĐỊNH
# ========================
DEFAULT_URL = "https://learnwithhasan.com/chatgpt-earthquake/"
DEFAULT_MIN_POINTS = 5
DEFAULT_MAX_POINTS = 10

# Danh sách các model có thể chọn
MODEL_REGISTRY = {"OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]}


# ========================
# 3️⃣ HÀM TIỆN ÍCH
# ========================


def is_valid_url(url: str) -> bool:
    """Kiểm tra xem URL có hợp lệ không"""
    return bool(re.match(r"^https?://", url.strip()))


@st.cache_data(show_spinner=False)
def fetch_article(url: str) -> str:
    """
    Lấy nội dung bài viết từ URL.
    Sử dụng cache để tránh tải lại nhiều lần (tăng tốc độ).
    """
    article = get_article_from_url(url)
    return textwrap.dedent(article).strip()


def build_prompt(article: str, min_points: int, max_points: int) -> str:
    """Ghép nội dung bài viết vào template prompt để gửi cho LLM"""
    return blog_bullet_summary_prompt.format(
        MinPoints=min_points, MaxPoints=max_points, InputText=article
    )


def summarize_with_llm(prompt: str, service: str, model: str) -> str:
    """Gọi hàm LLM sinh tóm tắt"""
    return llm_generate_text(prompt, service, model)


def fix_point_order(min_points: int, max_points: int):
    """Đảm bảo min ≤ max để tránh lỗi nhập sai"""
    if min_points > max_points:
        return max_points, min_points
    return min_points, max_points


# ========================
# 4️⃣ THANH BÊN (SIDEBAR)
# ========================
# Mục đích: chứa cài đặt chung, không ảnh hưởng đến luồng chính
with st.sidebar:
    st.header("⚙️ Cài đặt")

    # Chọn dịch vụ LLM
    service = st.selectbox("Chọn dịch vụ AI", list(MODEL_REGISTRY.keys()), index=0)

    # Chọn model tương ứng
    model = st.selectbox("Chọn model", MODEL_REGISTRY[service], index=2)

    st.caption("💡 Gợi ý: Model nhỏ chạy nhanh hơn, model lớn chất lượng tốt hơn.")


# ========================
# 5️⃣ GIAO DIỆN CHÍNH
# ========================
st.title("🧠 Trình tóm tắt Blog bằng AI")
st.write(
    "Nhập URL của bài viết, chọn số lượng bullet points, và nhận bản tóm tắt nhanh chóng."
)

# Dùng form để gom các input, tránh việc app reload mỗi lần nhập ký tự
with st.form("summary_form"):
    url = st.text_input(
        "🔗 URL bài viết",
        value=DEFAULT_URL,
        placeholder="https://example.com/blog",
        help="Dán đường link đầy đủ (bao gồm https://)",
    )

    col1, col2 = st.columns(2)
    with col1:
        min_points = st.number_input("Số bullet nhỏ nhất", 1, 50, DEFAULT_MIN_POINTS)
    with col2:
        max_points = st.number_input("Số bullet lớn nhất", 1, 50, DEFAULT_MAX_POINTS)

    submit = st.form_submit_button("🚀 Tóm tắt ngay", use_container_width=True)


# ========================
# 6️⃣ LUỒNG CHẠY CHÍNH
# ========================
if submit:
    # Kiểm tra lỗi nhập URL
    if not is_valid_url(url):
        st.error("❌ URL không hợp lệ. Hãy nhập link bắt đầu bằng http hoặc https.")
        st.stop()

    # Đảm bảo min ≤ max
    min_points, max_points = fix_point_order(int(min_points), int(max_points))

    # 1️⃣ Lấy nội dung bài viết
    with st.spinner("Đang tải bài viết..."):
        try:
            article = fetch_article(url)
        except Exception as e:
            st.error(f"Lỗi khi lấy bài viết: {e}")
            st.stop()

    if not article:
        st.warning("Không trích xuất được nội dung. Thử URL khác nhé.")
        st.stop()

    with st.expander("👀 Xem trước nội dung bài viết"):
        st.write(article[:1500] + ("..." if len(article) > 1500 else ""))

    # 2️⃣ Tạo prompt và gọi LLM
    prompt = build_prompt(article, min_points, max_points)

    with st.expander("🧩 Xem prompt đã tạo (dành cho người học)", expanded=False):
        st.code(prompt, language="markdown")

    with st.spinner(f"Đang tóm tắt bằng {service} ({model})..."):
        try:
            summary = summarize_with_llm(prompt, service, model)
        except Exception as e:
            st.error(f"Lỗi khi gọi AI: {e}")
            st.stop()

    # 3️⃣ Hiển thị kết quả
    st.success("✅ Đã tạo tóm tắt thành công!")
    st.subheader("📄 Bản tóm tắt:")
    st.write(summary)

    # 4️⃣ Cho phép tải hoặc chỉnh sửa kết quả
    st.download_button(
        "⬇️ Tải tóm tắt (.txt)", summary, file_name="summary.txt", mime="text/plain"
    )

    with st.expander("✏️ Chỉnh sửa trước khi tải"):
        edited = st.text_area("Chỉnh sửa tại đây:", value=summary, height=200)
        st.download_button(
            "⬇️ Tải bản đã chỉnh sửa",
            edited,
            file_name="summary_edited.txt",
            mime="text/plain",
        )


# ========================
# 7️⃣ FOOTER / HƯỚNG DẪN
# ========================
st.markdown("---")
st.markdown("""
### 🧭 Cách hoạt động:
1. Ứng dụng **tải nội dung bài viết** từ URL bạn nhập.
2. Sau đó **tạo prompt** yêu cầu AI tóm tắt theo số bullet bạn chọn.
3. Cuối cùng, AI **trả về bản tóm tắt** ngắn gọn, dễ đọc.

💡 **Lưu ý:** Nếu bài viết dài hoặc URL lỗi, có thể cần thử lại 1–2 lần.
""")

with st.sidebar:
    st.markdown("---")
    st.markdown("#### 📘 Giới thiệu")
    st.write(
        "Công cụ này giúp bạn tóm tắt nhanh blog hoặc bài báo để tiết kiệm thời gian đọc."
    )
