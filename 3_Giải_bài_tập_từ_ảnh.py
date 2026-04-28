import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Gia sư Toán AI", page_icon="📘")
st.title("📘 Gia sư Toán AI (Hỗ trợ Đa ngôn ngữ)")

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
        st.subheader("🔍 Tùy chọn giải bài:")
        
        # Thêm tính năng chọn ngôn ngữ phụ
        ngon_ngu = st.radio(
            "Chọn ngôn ngữ song song với Tiếng Việt:",
            options=["Tiếng H'Mông", "Tiếng Anh"],
            horizontal=True
        )

        if st.button("Giải bài tập", type="primary"):

            if not api_key:
                st.error("❌ Bạn chưa nhập API Key!")
            else:
                with st.spinner(f"⏳ Đang giải bài bằng Việt - {ngon_ngu}..."):
                    
                    # ===============================
                    # 🧠 PROMPT CHUẨN – GIẢI BÀI TẬP (ĐÃ ĐỘNG HÓA NGÔN NGỮ)
                    # ===============================
                    prompt_text = f"""
Bạn là giáo viên Toán giỏi. Hãy **giải bài tập trong ảnh** theo cách NGẮN – DỄ HIỂU – SONG NGỮ (Việt – {ngon_ngu}).

==============================
⚠️ QUY TẮC CÔNG THỨC TOÁN HỌC
==============================
- Tất cả công thức phải đặt trong khối:
  $$
  ... \\\\
  $$
- Mỗi phép toán BẮT BUỘC xuống dòng bằng \\\\
- Dùng đúng LaTeX chuẩn:
  \\frac{{}}, \\sqrt{{}}, ^{{}}, _{{}}, \\triangle, \\angle, \\parallel, \\perp
- TUYỆT ĐỐI KHÔNG sinh ký tự lạ.
- Không ghép nhiều công thức trên 1 dòng.
- Đơn vị viết dạng: 150\\,m ; 30\\,cm

=====================
1️⃣ CHÉP LẠI ĐỀ BÀI
=====================
- Dòng 1: Đề bài tiếng Việt (ngắn gọn).
- Dòng 2: Dịch sang {ngon_ngu}.
- Dòng 3: Công thức LaTeX rõ ràng, mỗi dòng có \\\\.

==========================
2️⃣ GIẢI BÀI TẬP (SONG NGỮ)
==========================
Mỗi bước trình bày 3 dòng:
- Dòng 1: Giải thích tiếng Việt.
- Dòng 2: Giải thích {ngon_ngu}.
- Dòng 3: Công thức LaTeX sạch:
  $$
  \\frac{{AP}}{{AB}} = \\frac{{150}}{{300}} = \\frac{{1}}{{2}} \\\\
  AP = 150\\,m
  $$

==========================
3️⃣ TRÌNH BÀY RÕ RÀNG
==========================
- Câu ngắn.
- Mỗi ý xuống dòng.
- Song ngữ Việt – {ngon_ngu}.
- LaTeX sạch – không ký tự lạ.
"""

                    result = analyze_real_image(api_key, image, prompt_text)

                    if result.startswith("❌"):
                        st.error(result)
                    else:
                        st.success("🎉 Hoàn thành!")
                        st.markdown(result)
