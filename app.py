import streamlit as st
from utils import inject_custom_css
import os

# st.set_page_config CHỈ ĐƯỢC PHÉP KHỞI CHẠY DUY NHẤT một lần ở file app.py chính này
st.set_page_config(
    page_title="Hệ thống Bản đồ rủi ro ngập lụt Thừa Thiên Huế",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# Hiển thị Logo IWRP & CDRI bên thanh điều hướng Sidebar nếu có trong thư mục assets/
st.sidebar.markdown("<div style='margin-top:-20px;'></div>", unsafe_allow_html=True)
col_logo1, col_logo2 = st.sidebar.columns(2)
with col_logo1:
    if os.path.exists("assets/iwrp_logo.png"):
        st.image("assets/iwrp_logo.png", use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; font-weight:700; color:#475569; font-size:16px;'>IWRP</div>", unsafe_allow_html=True)
with col_logo2:
    if os.path.exists("assets/cdri_logo.png"):
        st.image("assets/cdri.jpg", use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; font-weight:700; color:#475569; font-size:16px;'>CDRI</div>", unsafe_allow_html=True)

# Thêm cấu trúc Markdown tóm tắt rìa tay trái (Sidebar)
st.sidebar.markdown("""
---
### **Tóm tắt dự án**
Đề tài xây dựng bản đồ phơi nhiễm ngập lụt và lượng hóa **Chỉ số tổn thương lũ (Flood Vulnerability Index - FVI)** cấp công trình cho **31 cơ sở thiết yếu** (22 trường học, 9 y tế) tại 5 phường trung tâm TP. Huế.

**Hợp phần công nghệ:**
1. Bản đồ ngập độ phân giải **10 m** từ ảnh vệ tinh radar **Sentinel-1 VV/VH**.
2. Chỉ số **FVI** xây dựng từ phân tích đa biến **PCA** kết hợp dữ liệu khảo sát thực địa.
3. Hỗ trợ quy hoạch, tối ưu hóa danh mục đầu tư công thích ứng biến đổi khí hậu.
""")

# Định nghĩa hệ thống định tuyến đa trang dựa trên file nằm trong pages/
pages = [
    st.Page("pages/1_Tom_tat_du_an.py", title="1. Tổng quan dự án", icon="📋", default=True),
    st.Page("pages/2_Hanh_trinh_thuc_hien.py", title="2. Lộ trình dự án", icon="📅"),
    st.Page("pages/3_Phuong_phap_nghien_cuu.py", title="3. Phương pháp nghiên cứu", icon="🔬"),
    st.Page("pages/4_Ban_do_va_Ket_qua_FVI.py", title="4. BẢN ĐỒ & KẾT QUẢ FVI", icon="🗺️"),
    st.Page("pages/5_Khuyen_nghi_va_Giai_phap.py", title="5. Khuyến nghị & Giải pháp", icon="💡"),
    st.Page("pages/6_Tai_nguyen_va_Lien_he.py", title="6. Tài nguyên & Liên hệ", icon="📞")
]

pg = st.navigation(pages)
pg.run()
