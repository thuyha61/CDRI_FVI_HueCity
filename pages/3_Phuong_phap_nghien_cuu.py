import streamlit as st
import pandas as pd
from utils import inject_custom_css

inject_custom_css()

st.markdown('<div class="section-title">Phương pháp nghiên cứu tích hợp</div>', unsafe_allow_html=True)
st.markdown('<div class="academic-paragraph">Phương pháp nghiên cứu được xây dựng nhằm đánh giá mức độ tổn thương do ngập lụt đối với các cơ sở hạ tầng thiết yếu tại thành phố Huế thông qua việc tích hợp dữ liệu viễn thám, hệ thống thông tin địa lý (GIS), khảo sát thực địa và phân tích thống kê. Thay vì chỉ đánh giá mức độ ngập, nghiên cứu phát triển Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) ở cấp từng cơ sở, cho phép xem xét đồng thời mức độ phơi nhiễm, đặc điểm dễ bị tổn thương và năng lực thích ứng của từng trường học và cơ sở y tế.</div>', unsafe_allow_html=True)

# Khởi tạo các Tab phương pháp luận chính
tab_theory, tab_workflow, tab_viendam, tab_weights_pca = st.tabs([
    "KHUNG LÝ THUYẾT & CHỈ SỐ FVI",
    "QUY TRÌNH XÂY DỰNG FVI",
    "BẢN ĐỒ NGẬP BẰNG VIỄN THÁM",
    "XÁC ĐỊNH TRỌNG SỐ PCA"
])

with tab_theory:
    st.markdown('<div class="sub-section-title">1. Cơ sở lý thuyết của IPCC</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Nghiên cứu dựa trên khung đánh giá rủi ro thiên tai của Ủy ban Liên chính phủ về Biến đổi khí hậu (IPCC), trong đó rủi ro thiên tai được hình thành từ sự tương tác giữa hiểm họa, mức độ phơi nhiễm và tính dễ bị tổn thương của đối tượng chịu tác động.</div>', unsafe_allow_html=True)
    st.latex(r"Risk = Hazard \times Exposure \times Vulnerability")
    
    st.markdown("""
        <ul>
            <li class="academic-paragraph"><b>Hazard (Hiểm họa):</b> Thể hiện qua đặc trưng ngập lụt đô thị gồm phạm vi, độ sâu và tần suất lặp của lũ lụt.</li>
            <li class="academic-paragraph"><b>Exposure (Độ phơi nhiễm):</b> Phản ánh diện tích và kết cấu hạ tầng nằm trong vùng nguy cơ chịu ảnh hưởng trực tiếp của bão lũ.</li>
            <li class="academic-paragraph"><b>Vulnerability (Tính dễ bị tổn thương):</b> Được lượng hóa bằng sự tương tác nội tại giữa Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity) của công trình hạ tầng.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">2. Khung xây dựng Chỉ số tổn thương lũ FVI</div>', unsafe_allow_html=True)
    st.latex(r"Flood\ Vulnerability = f(Exposure,\ Sensitivity,\ Adaptive\ Capacity)")
    st.markdown('<div class="academic-paragraph">Mức độ tổn thương tăng khi Exposure và Sensitivity tăng, đồng thời giảm khi Adaptive Capacity được cải thiện và nâng cấp phần cứng.</div>', unsafe_allow_html=True)

with tab_workflow:
    st.markdown('<div class="sub-section-title">Quy trình 6 bước xây dựng Chỉ số FVI cấp cơ sở</div>', unsafe_allow_html=True)
    st.markdown("""
        | Bước thực hiện | Tên bước kỹ thuật | Nội dung & Phương thức triển khai thực tế |
        |---|---|---|
        | **Bước 1** | Xác định phạm vi | Lựa chọn các cơ sở hạ tầng trường học và trạm y tế thuộc 5 phường trung tâm làm đơn vị nghiên cứu độc lập. |
        | **Bước 2** | Lựa chọn bộ chỉ số | Thiết lập hai bộ chỉ số chuyên biệt cho Giáo dục và Y tế để phù hợp với yêu cầu vận hành của từng ngành. |
        | **Bước 3** | Tổng hợp tích hợp dữ liệu | Thu thập dữ liệu đa nguồn gồm dữ liệu không gian, ảnh vệ tinh Sentinel-1 và phiếu điều tra thực địa. |
        | **Bước 4** | Tiền xử lý dữ liệu | Làm sạch dữ liệu, mã hóa biến định tính, rà soát chiều tác động thuận/nghịch của các biến thành phần. |
        | **Bước 5** | Chuẩn hóa dữ liệu | Đưa tất cả dữ liệu thô có đơn vị đo khác nhau về cùng thang đo chuẩn không đơn vị bằng phương pháp Z-score. |
        | **Bước 6** | Xác định trọng số & Tính FVI | Áp dụng phân tích thành phần chính PCA để loại bỏ tính chủ quan, sau đó phân nhóm bằng thuật toán Jenks. |
    """)
    st.latex(r"Z_i = \frac{x_i - \bar{x}}{\sigma}")
    st.latex(r"FVI = \sum_{i=1}^{n} w_i Z_i")

with tab_viendam:
    st.markdown('<div class="sub-section-title">Hợp phần viễn thám radar xây dựng bản đồ ngập lụt</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Hợp phần này cung cấp dữ liệu đầu vào cốt lõi để lượng hóa thành phần Độ phơi nhiễm (Exposure) trong Chỉ số tổn thương lũ (FVI). Nhằm đáp ứng yêu cầu phân tích chính xác tại vị trí của từng trường học và cơ sở y tế, nghiên cứu tiến hành xây dựng hệ thống bản đồ ngập độ phân giải cao 10 m từ ảnh radar vệ tinh Sentinel-1 kết hợp các thuật toán học máy Random Forest.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Bảng so sánh các phương pháp xác định vùng ngập viễn thám</div>', unsafe_allow_html=True)
    compare_df = pd.DataFrame([
        {"Tiêu chí": "Độ phân giải", "Bản đồ diện rộng (Ví dụ: SPADE)": "Thô (90 m)", "Phương pháp Phân ngưỡng": "Trung bình (10 m - 20 m)", "Tích hợp Học máy (Dự án đề xuất)": "Cao (10 m)"},
        {"Tiêu chí": "Nguồn ảnh đầu vào", "Bản đồ diện rộng (Ví dụ: SPADE)": "Quang học / Thủy văn", "Phương pháp Phân ngưỡng": "Ảnh radar đơn lẻ", "Tích hợp Học máy (Dự án đề xuất)": "Tích hợp đa nguồn (Radar + DEM + Khí tượng)"},
        {"Tiêu chí": "Hiệu quả tại khu đô thị", "Bản đồ diện rộng (Ví dụ: SPADE)": "Rất thấp (Bỏ sót các túi ngập)", "Phương pháp Phân ngưỡng": "Thấp (Bị nhiễu bởi phản xạ bê tông)", "Tích hợp Học máy (Dự án đề xuất)": "Cao (Thuật toán lọc nhiễu cấu trúc công trình)"},
        {"Tiêu chí": "Chi phí dữ liệu", "Bản đồ diện rộng (Ví dụ: SPADE)": "Thấp (Dữ liệu có sẵn)", "Phương pháp Phân ngưỡng": "Thấp (Ảnh Sentinel mở)", "Tích hợp Học máy (Dự án đề xuất)": "Tối ưu (Ảnh mở, khai thác hiệu năng thuật toán)"}
    ])
    st.table(compare_df)
    
    st.markdown('<div class="sub-section-title">Mô hình Random Forest và kết quả kiểm định</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="academic-paragraph"><b>Mẫu huấn luyện:</b> Gồm 630 điểm mẫu thực địa được thu thập đồng bộ tại 13 thời điểm thiên tai mưa lũ kỷ lục năm 2025.</li>
            <li class="academic-paragraph"><b>Kết quả kiểm định:</b> Tại khu vực đô thị lõi của TP. Huế, mô hình đạt độ chính xác toàn cục 97%, chỉ số Recall đạt 100% (không bỏ sót bất kỳ khu vực ngập thực tế nào) và chỉ số cân bằng F1-score đạt 0.89.</li>
        </ul>
    """, unsafe_allow_html=True)

with tab_weights_pca:
    st.markdown('<div class="sub-section-title">Bảng tổng hợp kết quả phân tích PCA cho hệ thống Trường học</div>', unsafe_allow_html=True)
    pca_school_df = pd.DataFrame([
        {"Nhóm chỉ số": "Exposure (Phơi nhiễm)", "Thành phần chính": "PC1", "Phương sai (%)": 53.48, "Yếu tố chi phối": "Mức độ ngập tại trường học", "Ý nghĩa": "Phản ánh tác động trực tiếp của ngập lụt đến công trình"},
        {"Nhóm chỉ số": "Exposure (Phơi nhiễm)", "Thành phần chính": "PC2", "Phương sai (%)": 26.28, "Yếu tố chi phối": "Mức độ ngập lân cận", "Ý nghĩa": "Phản ánh ảnh hưởng gián đoạn giao thông tiếp cận"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC1", "Phương sai (%)": 46.69, "Yếu tố chi phối": "Vai trò điểm sơ tán", "Ý nghĩa": "Phản ánh áp lực tiếp nhận cứu trợ của trường học"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC2", "Phương sai (%)": 22.35, "Yếu tố chi phối": "Quy mô học sinh", "Ý nghĩa": "Phản ánh áp lực bảo vệ tính mạng học sinh"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC3", "Phương sai (%)": 14.89, "Yếu tố chi phối": "Tuổi thọ công trình", "Ý nghĩa": "Phản ánh tính dễ tổn thương của kết cấu xây dựng"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC1", "Phương sai (%)": 53.91, "Yếu tố chi phối": "Phương tiện ứng cứu tại chỗ", "Ý nghĩa": "Phản ánh khả năng ứng cứu sơ tán khẩn cấp"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC2", "Phương sai (%)": 16.76, "Yếu tố chi phối": "Kế hoạch ứng phó & Diễn tập", "Ý nghĩa": "Phản ánh sự chuẩn bị tổ chức phi cấu trình"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC3", "Phương sai (%)": 12.73, "Yếu tố chi phối": "Hạ tầng kỹ thuật độc lập", "Ý nghĩa": "Duy trì năng lượng và nước sạch dự phòng"}
    ])
    st.table(pca_school_df)
