import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Gia sư Toán AI Song ngữ", 
    page_icon="📘", 
    layout="wide"
)

# --- PHONG CÁCH GIAO DIỆN (CSS CUSTOM) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CÀI ĐẶT ---
with st.sidebar:
    st.title("⚙️ Cấu hình hệ thống")
    st.info("Ứng dụng sử dụng trí tuệ nhân tạo Gemini để hỗ trợ giải toán song ngữ.")
    
    api_key = st.text_input("🔑 Nhập Google API Key:", type="password", help="Lấy tại: https://aistudio.google.com/app/apikey")
    
    if api_key:
        st.success("✅ API Key đã sẵn sàng")
    else:
        st.warning("⚠️ Vui lòng nhập API Key để bắt đầu")
        
    st.markdown("---")
    st.markdown("### 📘 Hướng dẫn nhanh:")
    st.write("1. Chụp hoặc tải ảnh đề bài.")
    st.write("2. Chọn ngôn ngữ mong muốn.")
    st.write("3. Bấm 'Giải bài tập' và chờ kết quả.")

# --- HÀM XỬ LÝ LOGIC ---
def analyze_math_problem(api_key, image, target_lang):
    """Gửi ảnh đến Gemini API và xử lý kết quả."""
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buf = BytesIO()
    image.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    # Sử dụng mô hình gemini-2.5-flash
    MODEL = "gemini-2.5-flash"
    URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

    prompt = f"""
Bạn là một gia sư Toán học tận tâm. Hãy giải bài tập trong ảnh theo phong cách giảng dạy:
1. Ngôn ngữ: Song ngữ (Tiếng Việt và {target_lang}).
2. Cấu trúc: 
   - Chép lại đề bài (Song ngữ).
   - Giải chi tiết từng bước (Mỗi bước giải thích bằng Tiếng Việt, sau đó đến {target_lang}).
   - Kết luận đáp số rõ ràng.
3. Công thức: Sử dụng LaTeX chuẩn, đặt trong khối $$ ... $$. Ví dụ: $$\\frac{{a}}{{b}}$$.
4. Lưu ý: Nếu ảnh không phải là bài tập Toán, hãy lịch sự từ chối bằng cả hai thứ tiếng.
"""

    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }]
    }

    try:
        res = requests.post(URL, json=payload, timeout=30)
        
        # Xử lý các mã lỗi phổ biến
        if res.status_code == 503:
            return "⚠️ **Hệ thống AI đang quá tải.** Do bạn đang dùng bản miễn phí, vui lòng đợi khoảng 10-20 giây rồi bấm nút 'Giải bài tập' lại nhé!"
        elif res.status_code == 400:
            return "❌ **Lỗi:** API Key không hợp lệ hoặc hình ảnh không đúng định dạng."
        elif res.status_code != 200:
            return f"❌ **Lỗi hệ thống ({res.status_code}):** {res.text}"

        data = res.json()
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "❌ Không thể phân tích nội dung hình ảnh. Hãy thử chụp rõ nét hơn."

    except Exception as e:
        return f"❌ **Lỗi kết nối:** {str(e)}. Kiểm tra internet của bạn."

# --- GIAO DIỆN CHÍNH ---
st.title("📘 Gia sư Toán AI Song ngữ")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📸 Bước 1: Cung cấp đề bài")
    input_method = st.radio("Chọn cách nhập:", ["Chụp ảnh trực tiếp", "Tải ảnh từ máy tính"], horizontal=True)
    
    image = None
    if input_method == "Chụp ảnh trực tiếp":
        photo = st.camera_input("Quét đề bài:")
        if photo: image = Image.open(photo)
    else:
        upload = st.file_uploader("Chọn tệp hình ảnh (jpg, png):", type=["png", "jpg", "jpeg"])
        if upload: image = Image.open(upload)

    if image:
        st.image(image, caption="Ảnh đề bài đã chọn", use_column_width=True)

with col2:
    st.subheader("🔍 Bước 2: Tùy chọn & Giải bài")
    target_lang = st.selectbox(
        "Chọn ngôn ngữ bổ trợ:",
        ["Tiếng H'Mông", "Tiếng Anh"],
        help="Kết quả sẽ hiển thị song song Tiếng Việt và ngôn ngữ này."
    )
    
    st.write("") # Tạo khoảng trống
    
    if st.button("🚀 BẮT ĐẦU GIẢI BÀI", type="primary"):
        if not api_key:
            st.error("Bạn chưa nhập API Key ở menu bên trái!")
        elif image is None:
            st.error("Vui lòng chụp hoặc tải ảnh đề bài lên trước.")
        else:
            with st.spinner(f"⏳ Trợ lý AI đang giải toán (Việt - {target_lang})..."):
                result = analyze_math_problem(api_key, image, target_lang)
                
                st.markdown("### 📝 Kết quả giải chi tiết:")
                st.markdown(result)
                
                if not result.startswith("⚠️") and not result.startswith("❌"):
                    st.balloons()
                    st.download_button(
                        label="📥 Tải lời giải về máy (.txt)",
                        data=result,
                        file_name="loi_giai_toan.txt",
                        mime="text/plain"
                    )

# --- CHÂN TRANG ---
st.markdown("---")
st.caption("Dự án tham gia cuộc thi Sáng tạo Thanh thiếu niên - Hỗ trợ học tập cho học sinh vùng cao.")
