import streamlit as st
import pandas as pd
from utils import inject_custom_css

inject_custom_css()

st.markdown('<div class="section-title">Tài nguyên và thông tin dự án</div>', unsafe_allow_html=True)

tab_resources, tab_partners, tab_cit_contact = st.tabs([
    "TÀI LIỆU VÀ DỮ LIỆU",
    "NHÓM THỰC HIỆN VÀ ĐỐI TÁC",
    "TRÍCH DẪN VÀ LIÊN HỆ"
])

with tab_resources:
    st.markdown('<div class="sub-section-title">Danh mục các tài liệu và sản phẩm dữ liệu mở của dự án</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Các sản phẩm nghiên cứu phát triển dưới đây được cung cấp nhằm thúc đẩy khoa học dữ liệu mở và tăng cường khả năng tiếp cận tái sử dụng thông tin nghiên cứu rủi ro ngập lụt.</div>', unsafe_allow_html=True)
    
    docs_table = pd.DataFrame([
        {"Sản phẩm nghiên cứu": "Báo cáo tổng hợp dự án", "Mô tả": "Tài liệu khoa học đầy đủ về phương pháp, thuật toán PCA và kết quả tính FVI cho 31 cơ sở.", "Trạng thái": "Dự kiến nghiệm thu 2026", "Tải xuống": "Chờ công bố"},
        {"Sản phẩm nghiên cứu": "Báo cáo tóm tắt (Executive Summary)", "Mô tả": "Tài liệu tóm lược ngắn gọn kết quả và mô hình phục vụ tra cứu nhanh.", "Trạng thái": "Dự kiến nghiệm thu 2026", "Tải xuống": "Chờ công bố"},
        {"Sản phẩm nghiên cứu": "Khuyến nghị chính sách (Policy Brief)", "Mô tả": "Tóm tắt các hướng giải pháp can thiệp cho tỉnh Thừa Thiên Huế.", "Trạng thái": "Đã hoàn thành bản thảo", "Tải xuống": "Liên hệ nhóm nghiên cứu"},
        {"Sản phẩm nghiên cứu": "Cơ sở dữ liệu FVI chuẩn hóa (.csv)", "Mô tả": "Bộ dữ liệu thuộc tính khảo sát thực địa đã chuẩn hóa mã hóa.", "Trạng thái": "Mở một phần phục vụ học thuật", "Tải xuống": "Liên hệ tác giả"}
    ])
    st.table(docs_table)

with tab_partners:
    st.markdown('<div class="sub-section-title">Đơn vị chủ trì thực hiện nghiên cứu</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="academic-paragraph">
            <b>Viện Quy hoạch Thủy lợi (Institute of Water Resources Planning – IWRP)</b><br>
            Là đơn vị khoa học công nghệ trực thuộc Bộ Nông nghiệp và Phát triển nông thôn Việt Nam. Viện chịu trách nhiệm xây dựng toàn bộ khung phương pháp luận FVI, triển khai điều tra đo đạc thực địa bão lụt tại tỉnh Thừa Thiên Huế, chạy mô hình thống kê đa biến PCA và lập trình xây dựng cổng thông tin số hóa tương tác.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Chương trình tài trợ và bảo trợ khoa học</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="academic-paragraph">
            <b>Coalition for Disaster Resilient Infrastructure (CDRI)</b><br>
            Nghiên cứu khoa học này vinh dự nhận nguồn tài trợ từ Chương trình CDRI Fellowship Programme 2025–2026 nhằm mục tiêu đề xuất các giải pháp nâng cao khả năng tự chống chịu của hệ thống cơ sở hạ tầng đô thị toàn cầu trước tác động của biến đổi khí hậu.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Nhóm chuyên gia thực hiện dự án</div>', unsafe_allow_html=True)
    col_per1, col_per2, col_per3 = st.columns(3)
    
    with col_per1:
        st.markdown("""
            <div class="card-team">
                <div class="card-team-title">Đỗ Thị Thúy Hà</div>
                <div class="card-team-sub">Chủ nhiệm dự án nghiên cứu</div>
                <div class="academic-paragraph" style="font-size:12px; margin-bottom:0px;">Viện Quy hoạch Thủy lợi (IWRP)<br>Chịu trách nhiệm chung điều phối dự án, xây dựng khung phương pháp chỉ số tổn thương FVI học thuật.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_per2:
        st.markdown("""
            <div class="card-team">
                <div class="card-team-title">Cộng sự Kỹ thuật IWRP</div>
                <div class="card-team-sub">Thành viên Ban kỹ thuật</div>
                <div class="academic-paragraph" style="font-size:12px; margin-bottom:0px;">Viện Quy hoạch Thủy lợi (IWRP)<br>Phụ trách lập trình bản đồ không gian địa lý, xử lý ảnh vệ tinh Sentinel-1 SAR và chạy thuật toán học máy.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_per3:
        st.markdown("""
            <div class="card-team">
                <div class="card-team-title">Cộng tác viên Thừa Thiên Huế</div>
                <div class="card-team-sub">Điều phối viên Khảo sát địa phương</div>
                <div class="academic-paragraph" style="font-size:12px; margin-bottom:0px;">Sở Giáo dục & Sở Y tế Thừa Thiên Huế<br>Hỗ trợ nhóm nghiên cứu tiếp cận trực tiếp 31 cơ sở y tế - trường học địa phương trong điều kiện thời tiết lụt bão.</div>
            </div>
        """, unsafe_allow_html=True)

with tab_cit_contact:
    st.markdown('<div class="sub-section-title">Quy chuẩn định dạng trích dẫn nghiên cứu khoa học</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="highlight-box">
            Khi sử dụng bất kỳ dữ liệu số, bản đồ ngập lụt đô thị hoặc điểm kết quả chỉ số FVI hiển thị trên trang thông tin điện tử này, vui lòng trích dẫn đầy đủ theo quy chuẩn học thuật sau:<br><br>
            <i>Đỗ Thị Thúy Hà và cộng sự (2026). Bản đồ rủi ro ngập lụt theo ngành nhằm tăng cường ứng phó và thích ứng với biến đổi khí hậu tại Thành phố Huế. Viện Quy hoạch Thủy lợi, Chương trình CDRI Fellowship 2025–2026.</i>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Thông tin liên hệ chính thức</div>', unsafe_allow_html=True)
    st.markdown("""
        * **Đơn vị thực hiện chủ trì:** Viện Quy hoạch Thủy lợi (IWRP)
        * **Đại diện nhóm nghiên cứu:** Đỗ Thị Thúy Hà
        * **Địa điểm trụ sở công tác:** Thành phố Hà Nội, Việt Nam
        * **Thời điểm cập nhật dữ liệu tự động:** <b>Ngày 12 tháng 07 năm 2026</b>
    """)
