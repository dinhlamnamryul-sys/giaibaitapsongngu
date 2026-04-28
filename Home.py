import streamlit as st
import os

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS GIAO DIỆN ---
st.markdown("""
<style>
    /* Ẩn thanh công cụ Streamlit (Deploy, Menu,...) */
    [data-testid="stHeader"] {
        visibility: hidden;
    }
    
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { background-color: #f8f9fa; margin-bottom: 50px; } /* Thêm margin để không bị footer che */
    
    .main-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 60%, #ff6f00 100%);
        color: white; padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 10px 30px rgba(183, 28, 28, 0.4); border-bottom: 6px solid #fdd835;
        margin-bottom: 20px;
    }
    .main-header h1 { font-size: 2.5rem; font-weight: 900; margin: 0; }
    
    .feature-card {
        background: white; padding: 20px; border-radius: 20px; text-align: center;
        border: 1px solid #eee; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 350px; display: flex; flex-direction: column; justify-content: space-between;
        transition: transform 0.3s;
    }
    .feature-card:hover { transform: translateY(-5px); border-color: #ff9800; }
    .icon-box { font-size: 3.5rem; margin-bottom: 10px; }
    .card-title { color: #d84315; font-weight: 800; font-size: 1.3rem; margin-bottom: 5px; }
    .stButton>button {
        width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff6f00, #ffca28);
        border: none; color: white; font-weight: bold; padding: 10px 0;
    }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- KHAI BÁO FILE TRANG ---
PAGE_1 = "pages/1_Gia_Sư_Toán_AI.py"
PAGE_2 = "pages/2_Sinh_Đề_Tự_Động.py"
PAGE_3 = "pages/3_Giải_bài_tập_từ_ảnh.py"
PAGE_4 = "pages/4_Học_liệu_đa_phương_tiện.py"
PAGE_5 = "pages/5_Văn_hóa_cội_nguồn.py"

# --- 3. MENU BÊN TRÁI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997235.png", width=120)
    st.markdown("<h3 style='text-align: center; color: #b71c1c;'>TRƯỜNG PTDTBT<br>TH&THCS NA Ư</h3>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🚀 Menu Chức Năng")

    if st.button("🏠 Trang Chủ"): 
        st.rerun()

    if os.path.exists(PAGE_1): 
        st.page_link(PAGE_1, label="Gia Sư Toán AI", icon="🏔️")

    if os.path.exists(PAGE_2): 
        st.page_link(PAGE_2, label="Sinh Đề Tự Động", icon="⚡")

    if os.path.exists(PAGE_3): 
        st.page_link(PAGE_3, label="Giải bài tập từ ảnh", icon="🧿")

    if os.path.exists(PAGE_4): 
        st.page_link(PAGE_4, label="Học liệu đa phương tiện", icon="📽️")

    if os.path.exists(PAGE_5): 
        st.page_link(PAGE_5, label="Văn hóa cội nguồn", icon="🌽")

    st.markdown("---")
    if 'visit_count' not in st.session_state:
        st.session_state.visit_count = 5383
    st.success(f"👥 Lượt truy cập: **{st.session_state.visit_count}**")

# --- 4. NỘI DUNG TRANG CHÍNH ---
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 CỔNG GIÁO DỤC SỐ NA Ư</h1>
    <h3>"Tri thức vùng cao - Vươn xa thế giới"</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="feature-card"><div class="icon-box">🏔️</div><div class="card-title">Gia Sư Toán AI</div><p>Học toán song ngữ.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_1):
        st.page_link(PAGE_1, label="Học ngay ➜", icon="📝", use_container_width=True)

with col2:
    st.markdown('<div class="feature-card"><div class="icon-box">⚡</div><div class="card-title">Sinh Đề Tốc Độ</div><p>Tạo đề trắc nghiệm trong vài giây.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_2):
        st.page_link(PAGE_2, label="Tạo đề ➜", icon="🚀", use_container_width=True)

with col3:
    st.markdown('<div class="feature-card"><div class="icon-box">🧿</div><div class="card-title">Giải bài tập từ ảnh</div><p>Giải bài mọi môn học bằng AI.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_3):
        st.page_link(PAGE_3, label="Giải ngay ➜", icon="📸", use_container_width=True)

with col4:
    st.markdown('<div class="feature-card"><div class="icon-box">📽️</div><div class="card-title">Đa Phương Tiện</div><p>Học liệu văn hóa H\'Mông.</p></div>', unsafe_allow_html=True)
    if os.path.exists(PAGE_4):
        st.page_link(PAGE_4, label="Khám phá ➜", icon="🎧", use_container_width=True)

# --- 5. CHÂN TRANG (FOOTER) ---
st.markdown("""
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #fff;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 2px solid #b71c1c;
        z-index: 100;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    .footer p {
        margin: 0;
        font-family: sans-serif;
    }
</style>
<div class="footer">
    <p>👨‍🏫 <b>Nhóm tác giả:</b> Trường PTDTBT TH&THCS Na Ư</p>
    <p style="font-size: 12px; color: #888;">© 2025 Cổng Giáo Dục Số Na Ư</p>
</div>
""", unsafe_allow_html=True)
