import streamlit as st
import random
import math
import io
import base64
import re
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- 1. DỮ LIỆU CHƯƠNG TRÌNH HỌC (Giữ nguyên) ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chủ đề 1: Các số từ 0 đến 10": ["Đếm số lượng", "So sánh số", "Tách gộp số (Mấy và mấy)"],
        "Chủ đề 2: Phép cộng, trừ phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"],
        "Chủ đề 3: Hình học đơn giản": ["Nhận biết hình vuông, tròn, tam giác"]
    },
    # ... (Các lớp khác giữ nguyên như cũ để tiết kiệm chỗ) ...
    # Bạn nhớ giữ nguyên dữ liệu các lớp từ 2-9 như file cũ nhé
}
# (Nếu bạn cần tôi gửi lại full dữ liệu các lớp thì bảo tôi nhé, ở đây tôi tập trung vào logic mới)

# --- 2. CÁC HÀM XỬ LÝ (LOGIC MỚI - PHÂN HÓA MỨC ĐỘ) ---

def tao_cau_hoi_theo_muc_do(lop, bai_hoc, muc_do):
    """
    Hàm sinh câu hỏi cụ thể theo mức độ:
    - muc_do 1: Nhận biết (Trắc nghiệm/Điền khuyết đơn giản)
    - muc_do 2: Thông hiểu (Tính toán cơ bản)
    - muc_do 3: Vận dụng (Bài toán ngược, lời văn, tư duy)
    """
    de_latex = ""; dap_an = ""; loai_toan = ""
    
    bai_lower = bai_hoc.lower()
    
    # --- LOGIC LỚP 1 (Ví dụ chi tiết) ---
    if "Lớp 1" in lop:
        if "cộng" in bai_lower or "trừ" in bai_lower:
            a = random.randint(1, 5); b = random.randint(1, 4)
            
            if muc_do == 1: # Nhận biết
                de_latex = f"Kết quả của phép tính $ {a} + {b} $ là mấy?"
                dap_an = f"{a+b}"
                
            elif muc_do == 2: # Thông hiểu
                de_latex = f"Tính: $ {a} + {b} = ? $"
                dap_an = f"{a+b}"
                
            elif muc_do == 3: # Vận dụng (Tìm x hoặc điền số)
                res = a + b
                de_latex = f"Điền số thích hợp vào chỗ chấm: $ {a} + ... = {res} $"
                dap_an = f"{b}"

        elif "so sánh" in bai_lower:
            v1 = random.randint(0, 10); v2 = random.randint(0, 10)
            while v1 == v2: v2 = random.randint(0, 10)
            
            if muc_do == 1:
                de_latex = f"Số nào lớn hơn: ${v1}$ hay ${v2}$?"
                dap_an = f"{max(v1, v2)}"
            elif muc_do == 2:
                de_latex = f"Điền dấu ($>, <, =$) thích hợp: $ {v1} ... {v2} $"
                dap_an = ">" if v1 > v2 else "<"
            else: # Vận dụng (Sắp xếp)
                v3 = random.randint(0, 10)
                lst = [v1, v2, v3]
                de_latex = f"Sắp xếp các số sau theo thứ tự tăng dần: ${v1}, {v2}, {v3}$"
                dap_an = ", ".join(map(str, sorted(lst)))
                
        else: # Mặc định (Hình học, đếm...)
            if muc_do == 1:
                de_latex = "Hình tam giác có mấy cạnh?"
                dap_an = "3"
            else:
                n = random.randint(2, 5)
                de_latex = f"Có {n} con gà, mua thêm 1 con. Hỏi có tất cả mấy con?"
                dap_an = f"{n+1}"

    # --- LOGIC CHUNG CHO CÁC LỚP KHÁC (Fallback) ---
    else:
        a = random.randint(1, 20); b = random.randint(1, 20)
        if muc_do == 1:
            de_latex = f"Khẳng định sau đúng hay sai: $ {a} + {b} = {a+b} $"
            dap_an = "Đúng"
        elif muc_do == 2:
            de_latex = f"Tính giá trị biểu thức: $ A = {a} + {b} $"
            dap_an = f"{a+b}"
        else: # Vận dụng
            de_latex = f"Tìm x biết: $ x - {a} = {b} $"
            dap_an = f"{a+b}"

    return de_latex, dap_an

def tao_de_toan(lop, bai_hoc):
    # Hàm cũ giữ lại để tương thích với trang Gia sư (nếu cần)
    # Nhưng ở trang Sinh đề chúng ta sẽ dùng hàm tao_cau_hoi_theo_muc_do bên trên
    return tao_cau_hoi_theo_muc_do(lop, bai_hoc, 2) + ([], "", "", "")

# ... (Giữ nguyên các hàm khác như text_to_speech_html, dich_sang_mong... của file cũ) ...
# Bổ sung các hàm cũ vào đây để không bị lỗi thiếu hàm
def text_to_speech_html(text, lang='vi'):
    return "" # Giả lập
def dich_sang_mong_giu_cong_thuc(text):
    return text
def phan_tich_loi_sai(u, t, q):
    return ""
def ai_giai_thich_chi_tiet(l, d, a):
    return ""
def update_rank():
    pass
