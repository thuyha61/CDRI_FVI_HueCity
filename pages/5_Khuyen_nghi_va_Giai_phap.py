import streamlit as st
from utils import inject_custom_css

inject_custom_css()

st.markdown('<div class="section-title">Khuyến nghị và ứng dụng kết quả</div>', unsafe_allow_html=True)
st.markdown('<div class="academic-paragraph">Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) không chỉ giúp xác định mức độ tổn thương của từng cơ sở mà còn cung cấp cơ sở khoa học để ưu tiên đầu tư và lựa chọn các giải pháp nâng cao khả năng chống chịu. Các khuyến nghị dưới đây được xây dựng trên cơ sở kết quả phân tích ba thành phần của FVI, bao gồm Độ phơi nhiễm (Exposure), Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity).</div>', unsafe_allow_html=True)

# Khởi tạo các Tab giải pháp chính sách
tab_priority, tab_indicator_solutions, tab_group_recommendations, tab_future_dev = st.tabs([
    "ƯU TIÊN CAN THIỆP",
    "GIẢI PHÁP THEO THÀNH PHẦN FVI",
    "KHUYẾN NGHỊ CHO CÁC NHÓM ĐỐI TƯỢNG",
    "HƯỚNG PHÁT TRIỂN"
])

with tab_priority:
    st.markdown('<div class="sub-section-title">Ma trận hành động ưu tiên can thiệp trong đầu tư công</div>', unsafe_allow_html=True)
    st.markdown("""
        | Mức độ tổn thương | Mức ưu tiên hành động | Hành động can thiệp đề xuất cụ thể |
        |---|---|---|
        | **Mức độ Cao** | Rất cao (Ưu tiên số 1) | Đầu tư nâng cấp công trình trong ngắn hạn; xây dựng kịch bản ứng phó khẩn cấp; trang bị máy bơm công suất lớn. |
        | **Mức độ Tương đối cao** | Cao (Ưu tiên số 2) | Rà soát cơ sở vật chất kỹ thuật; tăng cường kịch bản huấn luyện tự thích ứng tại chỗ cho cán bộ. |
        | **Mức độ Trung bình** | Trung bình | Duy trì theo dõi trạng thái định kỳ; khắc phục các khiếm khuyết kỹ thuật hạ tầng nhỏ hiện tại. |
        | **Mức độ Thấp** | Thấp / Duy trì | Tiếp tục phát huy năng lực chống chịu bền vũg vốn có; làm bài học điển hình nâng cấp. |
    """)
    st.markdown("""
        <div class="highlight-box">
            <b>Ý nghĩa chính sách:</b> Chỉ số định lượng FVI giúp các nhà quản lý chuyển dịch hoàn toàn tư duy quy hoạch từ đầu tư phân bổ dàn trải sang đầu tư trọng điểm, tập trung tối ưu hóa nguồn lực tài chính công vào các khu vực công trình hạ tầng dễ bị tổn thương nhất.
        </div>
    """, unsafe_allow_html=True)

with tab_indicator_solutions:
    st.markdown('<div class="sub-section-title">Các giải pháp kỹ thuật đề xuất theo cấu phần FVI</div>', unsafe_allow_html=True)
    
    # Sử dụng định dạng danh sách Markdown chuẩn để tránh lỗi vỡ dòng trong bảng
    st.markdown("""
        | Cấu phần rủi ro | Mục tiêu giảm thiểu | Đề xuất giải pháp kỹ thuật ưu tiên |
        |---|---|---|
        | **Độ phơi nhiễm (Exposure)** | Giảm mức độ tiếp xúc vật lý của hạ tầng với vùng ngập | • Nâng cao độ nền công trình chính so với mặt đường lân cận.<br>• Nâng cấp hệ thống mương gom thoát nước nội khu ra sông chính.<br>• Thiết lập hệ thống đê quai bảo vệ cục bộ khu vực trọng yếu. |
        | **Độ nhạy cảm (Sensitivity)** | Giảm mức độ thiệt hại tài sản khi nước tràn vào công trình | • Bố trí thiết bị kỹ thuật, kho lưu trữ và trạm biến áp lên tầng 2.<br>• Thay đổi sang sử dụng các loại vật liệu xây dựng chịu nước bền vững.<br>• Định rõ lối thoát hiểm kết cấu hỗ trợ nhóm người yếu thế. |
        | **Năng lực thích ứng (Adaptive)** | Tăng tốc khả năng khôi phục hoạt động tự lực khi ngập xảy ra | • Trang bị máy nổ phát điện độc lập đặt ở cao độ an toàn.<br>• Dự trữ lương thực, thiết bị vật tư y tế sơ cấp cứu, máy bơm và áo phao.<br>• Tổ chức huấn luyện và diễn tập kịch bản ứng phó hàng năm. |
    """, unsafe_allow_html=True)

with tab_group_recommendations:
    st.markdown('<div class="sub-section-title">Hành động cụ thể định hướng cho từng nhóm chủ thể</div>', unsafe_allow_html=True)
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
            ### 1. Chính quyền Thành phố Huế
            * Tích hợp bản đồ Chỉ số rủi ro FVI 10 m trực tiếp vào các kế hoạch phòng chống thiên tai cấp thành phố.
            * Phân bổ ngân sách trung hạn cải thiện hạ tầng giao thông tiếp cận quanh các điểm rủi ro.
            
            ### 2. Ngành Giáo dục (Sở GD&ĐT)
            * Rà soát quy trình an toàn bão lũ trường học trước kỳ mưa lũ miền Trung hàng năm.
            * Chủ động xác định các điểm trường học cao ráo an toàn làm điểm sơ tán lâm thời cho cộng đồng.
        """)
        
    with col_rec2:
        st.markdown("""
            ### 3. Ngành Y tế (Sở Y tế)
            * Đảm bảo tính hoạt động liên tục 24/7 của các trạm y tế cơ sở ngay cả khi mạng lưới giao thông bị ngập cô lập sâu.
            * Trang bị máy phát điện độc lập chống ngập để bảo quản các loại vắc xin, thuốc men khẩn cấp.
            
            ### 4. Nhóm các nhà nghiên cứu
            * Tiếp tục thu thập và làm giàu cơ sở dữ liệu thực địa sau mỗi mùa bão lũ mới.
            * Nghiên cứu nhân rộng mô hình tính toán FVI cho các khu vực vùng ven sông Hương có điều kiện tương tự.
        """)

with tab_future_dev:
    st.markdown('<div class="sub-section-title">Hướng phát triển và mở rộng nghiên cứu trong tương lai</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="academic-paragraph"><b>Mở rộng phạm vi đối tượng hạ tầng:</b> Đề xuất nghiên cứu áp dụng khung phân tích rủi ro FVI cho các đối tượng hạ tầng đô thị quan trọng khác như hệ thống giao thông huyết mạch, trạm phân phối điện sạch và mạng lưới cung cấp nước sinh hoạt thành phố.</li>
            <li class="academic-paragraph"><b>Hệ thống cập nhật thời gian thực:</b> Xây dựng module tự động tiếp nhận dữ liệu khí tượng thủy văn dự báo ngập lụt sớm 24h - 48h để đưa ra cảnh báo khẩn cấp trực tiếp cho từng đơn vị.</li>
            <li class="academic-paragraph"><b>Ứng dụng di động (Mobile WebGIS):</b> Phát triển công cụ bản đồ thông tin rủi ro tương tác trên thiết bị di động hỗ trợ người dân và đội ngũ cứu hộ tìm hướng di chuyển an toàn khi thiên tai xảy ra.</li>
        </ul>
    """, unsafe_allow_html=True)
