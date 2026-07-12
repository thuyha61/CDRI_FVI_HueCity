import streamlit as st
import pandas as pd
from utils import inject_custom_css

# inject CSS để áp dụng định dạng Roboto
inject_custom_css()

# Banner tiêu đề chính của dự án CDRI Fellowship
st.markdown("""
    <style>
        .hero-banner {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            padding: 30px;
            border-radius: 12px;
            border-left: 8px solid #1d3557;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
        }
        .hero-title-vn {
            color: #1d3557;
            font-size: 26px;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        .hero-title-en {
            color: #457b9d;
            font-size: 20px;
            font-style: italic;
            font-weight: 500;
            line-height: 1.4;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 15px;
        }
        .hero-meta {
            color: #2b2d42;
            font-size: 15px;
            line-height: 1.6;
        }
        .hero-meta b {
            color: #1d3557;
        }
        
        /* Đảm bảo hiển thị tốt trên cả giao diện Tối (Dark Mode) của Streamlit */
        @media (prefers-color-scheme: dark) {
            .hero-banner {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border-left-color: #38bdf8;
            }
            .hero-title-vn {
                color: #f8fafc;
            }
            .hero-title-en {
                color: #38bdf8;
                border-bottom-color: #334155;
            }
            .hero-meta {
                color: #cbd5e1;
            }
            .hero-meta b {
                color: #38bdf8;
            }
        }
    </style>

    <div class="hero-banner">
        <div class="hero-title-vn">Bản đồ rủi ro ngập lụt theo ngành nhằm tăng cường ứng phó và thích ứng với biến đổi khí hậu tại Thành phố Huế</div>
        <div class="hero-title-en">Sectoral Flood Risk Mapping to Enhance Climate Change Response and Adaptation in Hue City, Vietnam</div>
        <div class="hero-meta">
            Nghiên cứu thuộc Chương trình <b>CDRI Fellowship 2025–2026</b><br>
            Đơn vị thực hiện: <b>Viện Quy hoạch Thủy lợi (Institute of Water Resources Planning – IWRP)</b><br>
            Đơn vị tài trợ: <b>Coalition for Disaster Resilient Infrastructure (CDRI)</b><br>
            Địa điểm nghiên cứu: <b>Thành phố Huế, Việt Nam</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# Các cột truy cập nhanh
col_quick1, col_quick2, col_quick3 = st.columns(3)
with col_quick1:
    st.info("🗺️ Khám phá bản đồ tương tác")
with col_quick2:
    st.warning("📄 Báo cáo nghiên cứu (Cập nhật sau khi nghiệm thu)")
with col_quick3:
    st.success("📂 Dữ liệu mở (Cập nhật sau khi công bố kết quả)")

# Tạo các tab nội dung
tab_over, tab_contrib, tab_overview_proj, tab_application = st.tabs([
    "TỔNG QUAN",
    "ĐÓNG GÓP CỦA NGHIÊN CỨU",
    "DỰ ÁN NGHIÊN CỨU",
    "KẾT QUẢ NỔI BẬT VÀ GIÁ TRỊ ỨNG DỤNG"
])

with tab_over:
    st.markdown('<div class="academic-paragraph">Lũ lụt là loại hình thiên tai biến động mạnh và gây thiệt hại nghiêm trọng nhất đối với hệ thống hạ tầng đô thị trên toàn cầu. Dưới tác động của biến đổi khí hậu, tần suất và cường độ của các hiện tượng mưa cực đoan có xu hướng gia tăng rõ rệt, đặc biệt tại các đô thị ven biển và vùng đồng bằng thấp.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Tại Việt Nam, khu vực miền Trung là trọng điểm chịu ảnh hưởng sâu sắc bởi các đợt ngập lụt kéo dài. Trong đó, Thành phố Huế có nguy cơ rủi ro rất cao do đặc điểm địa hình lòng chảo, mạng lưới sông ngắn có độ dốc lớn và lượng mưa hàng năm cao. Tính chất nghiêm trọng này được minh chứng qua đợt mưa lịch sử năm 2025 với lượng mưa trong 24 giờ đạt mốc kỷ lục 1.739 mm, gây ra chuỗi bốn trận lũ lớn liên tiếp phá vỡ các mốc lịch sử.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Trường học và cơ sở y tế là hai nhóm hạ tầng thiết yếu, giữ vai trò tuyến đầu bảo đảm an sinh và hỗ trợ sơ tán, cứu trợ khẩn cấp. Khi các công trình này bị ngập lụt hoặc cô lập, hệ lụy không chỉ dừng lại ở thiệt hại vật chất mà còn trực tiếp làm gián đoạn quyền tiếp cận y tế, giáo dục, làm suy giảm khả năng phục hồi của toàn cộng đồng. Do đó, nâng cao năng lực chống chịu cho các hạ tầng thiết yếu này là yêu cầu cấp bách trong quản lý đô thị hiện đại.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Dự án nghiên cứu "Bản đồ rủi ro ngập lụt theo ngành nhằm tăng cường ứng phó và thích ứng với biến đổi khí hậu tại Thành phố Huế" ứng dụng công nghệ viễn thám, hệ thống GIS và khảo sát thực địa để lượng hóa năng lực chống chịu của 31 cơ sở giáo dục và y tế tại 5 phường trung tâm thành phố Huế. Nghiên cứu tích hợp các nguồn dữ liệu này để xây dựng Bản đồ phơi nhiễm ngập lụt kết hợp Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) cấp cơ sở.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="highlight-box">
            <b>Không phải mọi cơ sở nằm trong cùng một vùng ngập đều có mức độ tổn thương giống nhau.</b>
            Khả năng chống chịu và tốc độ phục hồi của từng công trình không chỉ phụ thuộc vào độ sâu ngập vật lý, mà được quyết định bởi các cấu phần nội tại. Do đó, chỉ số FVI được thiết lập nhằm kết hợp chặt chẽ giữa các yếu tố rủi ro vật lý không gian (độ sâu ngập, khoảng cách tới sông) và các đặc trưng kinh tế - xã hội nội tại (kết cấu công trình, quy mô nhân lực, trang thiết bị và năng lực ứng phó tại chỗ) nhằm định lượng và làm rõ sự khác biệt vi mô này. Sản phẩm đầu ra hỗ trợ các cơ quan quản lý lồng ghép thông tin rủi ro vào quy hoạch, xác định chính xác danh mục công trình cần ưu tiên đầu tư ngân sách và chủ động xây dựng kế hoạch thích ứng.
        </div>
    """, unsafe_allow_html=True)
    
    # Chỉ số nổi bật
    st.markdown('<div class="sub-section-title">Các chỉ số nổi bật của dự án</div>', unsafe_allow_html=True)
    col_idx1, col_idx2, col_idx3, col_idx4 = st.columns(4)
    col_idx1.metric("Cơ sở được đánh giá", "31", "22 Trường học | 9 Y tế")
    col_idx2.metric("Phường nghiên cứu", "5", "Trung tâm Thành phố")
    col_idx3.metric("Độ phân giải bản đồ", "10 m", "Từ dữ liệu Sentinel-1")
    col_idx4.metric("Độ chính xác mô hình", "95–97%", "Phát hiện vùng ngập")
    
    st.markdown('<div class="sub-section-title">Các sản phẩm chính bàn giao của dự án</div>', unsafe_allow_html=True)
    products_df = pd.DataFrame([
        {"Sản phẩm": "Bản đồ phơi nhiễm ngập lụt", "Nội dung": "Phạm vi và tần suất ngập theo các chu kỳ lặp khác nhau"},
        {"Sản phẩm": "Bản đồ Chỉ số tổn thương lũ (FVI)", "Nội dung": "Đánh giá mức độ tổn thương của từng trường học và cơ sở y tế"},
        {"Sản phẩm": "Cơ sở dữ liệu FVI", "Nội dung": "Bộ dữ liệu chuẩn hóa phục vụ phân tích và quản lý"},
        {"Sản phẩm": "Website tương tác", "Nội dung": "Tra cứu bản đồ, dữ liệu và kết quả nghiên cứu"},
        {"Sản phẩm": "Báo cáo nghiên cứu", "Nội dung": "Phương pháp, kết quả và khuyến nghị"},
        {"Sản phẩm": "Khuyến nghị chính sách", "Nội dung": "Hỗ trợ quản lý rủi ro và thích ứng với biến đổi khí hậu"}
    ])
    st.table(products_df)

with tab_contrib:
    st.markdown('<div class="sub-section-title">Khoảng trống trong các nghiên cứu hiện nay</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="academic-paragraph"><b>Thiếu bộ chỉ số đánh giá theo từng lĩnh vực:</b> Phần lớn các nghiên cứu hiện nay sử dụng một bộ chỉ số chung để đánh giá nhiều loại hình hạ tầng. Cách tiếp cận này chưa phản ánh đầy đủ sự khác biệt về chức năng, yêu cầu vận hành và tiêu chí chống chịu của từng lĩnh vực. Đối với trường học, các yếu tố về quy mô học sinh hay điểm sơ tán cần ưu tiên; còn đối với y tế, nguồn điện và nước dự phòng, năng lực cấp cứu mới là yếu tố quyết định.</li>
            <li class="academic-paragraph"><b>Thiếu đánh giá ở cấp từng cơ sở:</b> Nhiều nghiên cứu đánh giá rủi ro theo đơn vị hành chính xã/huyện hoặc ô lưới không gian. Cách tiếp cận này thô và không thể lượng hóa được mức độ rủi ro khác nhau do sự khác biệt về cao độ công trình, thiết bị ứng cứu và năng lực chuẩn bị tại chỗ giữa hai tòa nhà nằm sát nhau.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Đóng góp của nghiên cứu đề xuất</div>', unsafe_allow_html=True)
    st.markdown("""
        <ol>
            <li class="academic-paragraph"><b>Phát triển bộ chỉ số theo từng lĩnh vực:</b> Xây dựng riêng hai bộ chỉ số độc lập cho giáo dục và y tế để phản ánh đúng đặc tính hoạt động thực tế.</li>
            <li class="academic-paragraph"><b>Đánh giá chi tiết ở cấp từng cơ sở:</b> Tính toán điểm tổn thương cho từng trường học và trạm y tế một cách độc lập.</li>
            <li class="academic-paragraph"><b>Tích hợp đa nguồn dữ liệu tiên tiến:</b> Kết hợp dữ liệu vệ tinh radar Sentinel-1, GIS địa hình cao độ số và điều tra bảng hỏi thực địa 31 cơ sở.</li>
        </ol>
    """, unsafe_allow_html=True)

with tab_overview_proj:
    st.markdown('<div class="sub-section-title">Mục tiêu và phạm vi nghiên cứu</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Dự án hướng tới xây dựng một hệ thống thông tin hỗ trợ quản lý rủi ro ngập lụt đối với trường học và cơ sở y tế tại thành phố Huế thông qua bốn mục tiêu chính: xây dựng bản đồ phơi nhiễm ngập lụt độ phân giải cao; phát triển Chỉ số tổn thương lũ (FVI) cấp công trình; phân tích yếu tố chi phối rủi ro và tích hợp cơ sở dữ liệu lên cổng thông tin tương tác.</div>', unsafe_allow_html=True)
    
    col_proj1, col_proj2 = st.columns(2)
    with col_proj1:
        st.markdown("""
            | Nội dung phạm vi | Mô tả chi tiết |
            |---|---|
            | **Khu vực nghiên cứu** | 5 phường trung tâm thành phố Huế |
            | **Đối tượng** | 22 trường học và 9 cơ sở y tế |
            | **Quy mô khảo sát** | 31 cơ sở hạ tầng thiết yếu |
            | **Nguồn dữ liệu** | Sentinel-1, GIS, số liệu thống kê, khảo sát thực địa |
            | **Thời gian thực hiện** | 2025–2026 |
        """)
    with col_proj2:
        st.markdown("""
            <div class="highlight-box" style="margin-top:0px;">
                <b>Lộ trình kỹ thuật tổng thể:</b><br><br>
                Ảnh viễn thám Sentinel-1 ➔ Hệ thống thông tin địa lý (GIS) ➔ Khảo sát thực địa trực tiếp ➔ Chuẩn hóa dữ liệu & Phân tích PCA ➔ Chỉ số tổn thương lũ (FVI).
            </div>
        """, unsafe_allow_html=True)

with tab_application:
    st.markdown('<div class="sub-section-title">Kết quả nổi bật đạt được</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Nghiên cứu đã xây dựng thành công bản đồ phơi nhiễm ngập lụt độ phân giải 10 m và Chỉ số tổn thương lũ cho 31 trường học và cơ sở y tế tại thành phố Huế. Mô hình phát hiện vùng ngập đạt độ chính xác 95–97%, tạo nền tảng cho việc đánh giá rủi ro ở cấp từng cơ sở. Kết quả phân tích xác định 5 cơ sở có mức độ tổn thương cao và 1 cơ sở có mức độ tổn thương tương đối cao, đồng thời làm rõ các yếu tố chính ảnh hưởng đến mức độ tổn thương của từng cơ sở.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Giá trị ứng dụng thực tiễn của dự án</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="academic-paragraph"><b>Đối với cơ quan quản lý:</b> Hỗ trợ xác định các cơ sở cần ưu tiên đầu tư, nâng cấp hạ tầng tránh dàn trải, đồng thời lồng ghép thông tin rủi ro trực tiếp vào quy hoạch thành phố thích ứng biến đổi khí hậu.</li>
            <li class="academic-paragraph"><b>Đối với ngành giáo dục và y tế:</b> Cung cấp dữ liệu định lượng cụ thể để từng đơn vị rà soát các hạn chế về cơ sở vật chất, trang bị (như thiếu máy bơm, thiếu máy nổ dự phòng) để lên phương án thích ứng mùa mưa lũ.</li>
            <li class="academic-paragraph"><b>Đối với nghiên cứu và phát triển:</b> Đề xuất một khung đánh giá có thể chuẩn hóa và nhân rộng cho các địa phương miền Trung có điều kiện tương tự.</li>
        </ul>
    """, unsafe_allow_html=True)
