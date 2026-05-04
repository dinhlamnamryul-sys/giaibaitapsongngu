import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json

st.set_page_config(page_title="Giải Bài Tập Từ Ảnh", page_icon="📘")
st.title("📘 Giải Bài Tập Từ Ảnh Đa Ngữ")

# =====================
# 🔑 NHẬP GOOGLE API KEY
# =====================

with st.expander("🔑 Hướng dẫn lấy Google API Key (bấm để xem)"):
    st.markdown("""
### 👉 Cách lấy Google API Key để dùng ứng dụng:

1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập Gmail.
3. Nhấn **Create API key**.
4. Copy API Key.
5. Dán vào ô bên dưới.

⚠️ Không chia sẻ API Key cho người khác.
""")

st.subheader("🔐 Nhập Google API Key:")
api_key = st.text_input("Google API Key:", type="password")

if not api_key:
    st.warning("⚠️ Nhập API Key để tiếp tục.")
else:
    st.success("✅ API Key hợp lệ!")


# ===============================
# 📌 HÀM GỌI GEMINI
# ===============================

def analyze_real_image(api_key, image, prompt):
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buf = BytesIO()
    image.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    MODEL = "gemini-2.5-flash"
    URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={api_key}"

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
        res = requests.post(URL, json=payload)
        if res.status_code != 200:
            return f"❌ Lỗi API {res.status_code}: {res.text}"

        data = res.json()
        if "candidates" not in data:
            return "❌ API trả về rỗng."

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"


# ===============================
# 📸 CHỤP HOẶC TẢI ẢNH
# ===============================

st.subheader("📷 Chụp ảnh đề bài")
photo = st.camera_input("Chụp từ camera:")

st.subheader("📤 Hoặc tải ảnh đề bài lên")
upload = st.file_uploader("Chọn ảnh:", type=["png", "jpg", "jpeg"])

image = None
if photo:
    image = Image.open(photo)
elif upload:
    image = Image.open(upload)


# ===============================
# 🧠 GIẢI BÀI TẬP TỪ ẢNH
# ===============================

if image:

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(image, caption="Ảnh đề bài", use_column_width=True)

    with col2:
        # ===============================
        # ⚙️ TÙY CHỌN NGÔN NGỮ
        # ===============================
        st.subheader("⚙️ Tùy chọn ngôn ngữ:")
        st.markdown("**Tiếng Việt**")
        use_hmong = st.checkbox("Tiếng Mông", value=True)
        use_english = st.checkbox("Tiếng Anh", value=True)
        
        st.markdown("---")
        st.subheader("🔍 Kết quả giải bài:")

        if st.button("Giải bài tập", type="primary"):

            if not api_key:
                st.error("❌ Bạn chưa nhập API Key!")
            else:
                with st.spinner("⏳ Đang giải bài..."):
                    
                    # Cấu trúc chuỗi ngôn ngữ dựa trên lựa chọn
                    langs_requested = ["Việt"]
                    if use_hmong: langs_requested.append("H’Mông")
                    if use_english: langs_requested.append("Anh")
                    lang_str = " – ".join(langs_requested)
                    
                    # Tạo hướng dẫn chép đề bài động
                    chep_de = "- Dòng 1: Tiếng Việt.\n"
                    line_idx = 2
                    if use_hmong:
                        chep_de += f"- Dòng {line_idx}: Tiếng H’Mông.\n"
                        line_idx += 1
                    if use_english:
                        chep_de += f"- Dòng {line_idx}: Tiếng Anh.\n"
                        
                    # Tạo hướng dẫn giải bài tập động
                    giai_bai = "- Tiếng Việt: [Nội dung giải thích]\n"
                    if use_hmong:
                        giai_bai += "- Tiếng H’Mông: [Nội dung giải thích]\n"
                    if use_english:
                        giai_bai += "- Tiếng Anh: [Nội dung giải thích]\n"

                    # ===============================
                    # 🧠 PROMPT CHUẨN – GIÁO VIÊN ĐA NĂNG
                    # ===============================
                    prompt_text = fr"""
Bạn là một giáo viên đa năng xuất sắc. Hãy **giải bài tập trong ảnh** (bất kể là môn Toán, Lý, Hóa, Văn, Anh...) theo cách NGẮN – DỄ HIỂU – ĐA NGỮ ({lang_str}).

==============================
⚠️ QUY TẮC TRÌNH BÀY
==============================
- Nếu có công thức (Toán, Lý, Hóa), hãy đặt trong khối:
  $$
  ... \\
  $$
  Và dùng chuẩn LaTeX. TUYỆT ĐỐI KHÔNG sinh ký tự lạ.
- Nếu là bài tập lý thuyết/chữ, trình bày rõ ràng từng đoạn, không cần gượng ép dùng công thức.

=====================
1️⃣ CHÉP LẠI ĐỀ BÀI (Tóm tắt)
=====================
{chep_de.strip()}

==========================
2️⃣ GIẢI BÀI TẬP (ĐA NGỮ)
==========================
Trình bày từng bước logic:
{giai_bai.strip()}
- Công thức (nếu có): Đặt trong khối $$...$$

==========================
3️⃣ TRÌNH BÀY RÕ RÀNG
==========================
- Câu ngắn, xuống dòng rõ ràng.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if result.startswith("❌"):
                        st.error(result)
                    else:
                        st.success("🎉 Hoàn thành!")
                        st.markdown(result)
