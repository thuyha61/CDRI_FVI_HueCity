import streamlit as st
import pandas as pd
from utils import inject_custom_css

# Khởi tạo CSS tùy biến hệ thống
inject_custom_css()

# Tùy biến CSS nội bộ cho Trang 3 nhằm khắc phục lỗi màu chữ Markdown bị tối
st.markdown("""
    <style>
      
        /* Ép tiêu đề của tất cả các Tab cho phép xuống dòng và căn giữa */
        div[data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            white-space: normal !important;
            text-align: center !important;
            line-height: 1.3 !important;
            word-break: break-word !important;
        }
        
        /* Cố định chiều cao tối thiểu cho tab để không bị lệch nếu có tab 1 dòng, tab 2 dòng */
        div[data-baseweb="tab-list"] button {
            min-height: 60px !important;
            height: auto !important;
            padding-top: 8px !important;
            padding-bottom: 8px !important;
        }

        /* Tiêu đề chính và tiêu đề phụ */
        .section-title {
            color: #1d3557;
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 15px;
            border-bottom: 3px solid #1d3557;
            padding-bottom: 10px;
        }
        .sub-section-title {
            color: #457b9d;
            font-size: 22px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 12px;
        }
        
        /* Đoạn văn học thuật tổng quan */
        .academic-paragraph {
            color: #2b2d42;
            font-size: 15.5px;
            line-height: 1.7;
            text-align: justify;
            margin-bottom: 15px;
        }
        
        /* Cấu trúc danh sách chỉ số */
        .academic-list {
            margin-top: 10px;
            margin-bottom: 20px;
            padding-left: 20px;
        }
        .academic-list li {
            color: #2b2d42;
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        
        /* Khung ghi chú / Trích dẫn học thuật */
        .academic-quote {
            background-color: #f8fafc;
            border-left: 5px solid #1d3557;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .academic-quote p {
            margin: 0;
            color: #1e293b;
            font-style: italic;
        }

        /* Đồng bộ giao diện Dark Mode tự động */
        @media (prefers-color-scheme: dark) {
            .section-title {
                color: #f8fafc;
                border-bottom-color: #38bdf8;
            }
            .sub-section-title {
                color: #38bdf8;
            }
            .academic-paragraph {
                color: #cbd5e1;
            }
            .academic-list li {
                color: #cbd5e1;
            }
            .academic-quote {
                background-color: #1e293b;
                border-left-color: #38bdf8;
            }
            .academic-quote p {
                color: #f1f5f9;
            }
            
        }
    </style>
""", unsafe_allow_html=True)

# --- GIỚI THIỆU TRANG ---
st.markdown('<div class="section-title">TRANG 3 – PHƯƠNG PHÁP NGHIÊN CỨU</div>', unsafe_allow_html=True)
st.markdown('<div class="academic-paragraph">Phương pháp nghiên cứu được xây dựng nhằm đánh giá mức độ tổn thương do ngập lụt đối với các cơ sở hạ tầng thiết yếu tại thành phố Huế thông qua việc tích hợp dữ liệu viễn thám, hệ thống thông tin địa lý (GIS), khảo sát thực địa và phân tích thống kê. Thay vì chỉ đánh giá mức độ ngập, nghiên cứu phát triển Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) ở cấp từng cơ sở, cho phép xem xét đồng thời mức độ phơi nhiễm, đặc điểm dễ bị tổn thương và năng lực thích ứng của từng trường học và cơ sở y tế.</div>', unsafe_allow_html=True)
st.markdown('<div class="academic-paragraph">Toàn bộ quy trình nghiên cứu được thiết kế theo hướng minh bạch, có khả năng lặp lại và có thể mở rộng cho các khu vực hoặc loại hình hạ tầng khác.</div>', unsafe_allow_html=True)

# Khởi tạo các Tab phương pháp luận chính
tab_theory, tab_workflow, tab_viendam, tab_weights_pca = st.tabs([
    "🔹 KHUNG LÝ THUYẾT & HỆ THỐNG CHỈ SỐ FVI",
    "🔹 CÁC BƯỚC XÂY DỰNG CHỈ SỐ TỔN THƯƠNG LŨ (FVI)",
    "🔹 BẢN ĐỒ NGẬP BẰNG VIỄN THÁM VÀ HỌC MÁY",
    "🔹 XÁC ĐỊNH TRỌNG SỐ VÀ XÂY DỰNG CHỈ SỐ FVI"
])

# ==========================================
# TAB 1: KHUNG LÝ THUYẾT & HỆ THỐNG CHỈ SỐ FVI
# ==========================================
with tab_theory:
    st.markdown('<div class="sub-section-title">1. Cơ sở lý thuyết</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Nghiên cứu dựa trên khung đánh giá rủi ro thiên tai của Ủy ban Liên chính phủ về Biến đổi khí hậu (IPCC), trong đó rủi ro thiên tai được hình thành từ sự tương tác giữa hiểm họa, mức độ phơi nhiễm và tính dễ bị tổn thương của đối tượng chịu tác động.</div>', unsafe_allow_html=True)
    
    st.latex(r"Risk = Hazard \times Exposure \times Vulnerability")
    
    st.markdown('<div class="academic-paragraph">Trong nghiên cứu này:</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><b>Hazard (Hiểm họa):</b> được biểu diễn thông qua đặc điểm ngập lụt, bao gồm phạm vi, độ sâu và tần suất ngập được xây dựng từ dữ liệu viễn thám.</li>
            <li><b>Exposure (Độ phơi nhiễm):</b> phản ánh mức độ mà từng cơ sở chịu tác động trực tiếp của ngập lụt.</li>
            <li><b>Vulnerability (Tính dễ bị tổn thương):</b> được xem là sự kết hợp giữa độ nhạy cảm và năng lực thích ứng của từng cơ sở.</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Do mục tiêu của nghiên cứu là đánh giá sự khác biệt về mức độ tổn thương giữa các cơ sở hạ tầng, phần phân tích tập trung vào việc xây dựng Flood Vulnerability Index (FVI).</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">2. Khung xây dựng Chỉ số tổn thương lũ</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">FVI được xây dựng trên ba nhóm thành phần chính:</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><b>Exposure</b> – phản ánh mức độ tiếp xúc của cơ sở với ngập lụt.</li>
            <li><b>Sensitivity</b> – phản ánh những đặc điểm làm gia tăng mức độ ảnh hưởng khi xảy ra ngập.</li>
            <li><b>Adaptive Capacity</b> – phản ánh khả năng chuẩn bị, ứng phó và phục hồi của cơ sở.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="academic-paragraph">Về mặt khái niệm:</div>', unsafe_allow_html=True)
    st.latex(r"Flood\ Vulnerability = f(Exposure,\ Sensitivity,\ Adaptive\ Capacity)")
    st.markdown('<div class="academic-paragraph">Trong đó, mức độ tổn thương tăng khi Exposure và Sensitivity tăng, đồng thời giảm khi Adaptive Capacity được cải thiện.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="academic-quote">
        <p><b>Gợi ý sơ đồ trực quan:</b> Mẫu sơ đồ ba thành phần cấu phần (Exposure, Sensitivity, Adaptive Capacity) hội tụ đồng hướng về chỉ số trung tâm FVI.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 2: XÂY DỰNG CHỈ SỐ FVI
# ==========================================
with tab_workflow:
    st.markdown('<div class="sub-section-title">Giới thiệu tổng quan</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) được xây dựng nhằm lượng hóa mức độ tổn thương của từng trường học và cơ sở y tế trước nguy cơ ngập lụt. Khác với các chỉ số được tính toán ở cấp xã, phường hoặc trên các ô lưới không gian, FVI trong nghiên cứu này được xây dựng ở cấp từng cơ sở, cho phép phản ánh sự khác biệt về điều kiện hạ tầng, quy mô hoạt động và năng lực ứng phó của từng đơn vị.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Quy trình xây dựng FVI được thiết kế theo sáu bước nhằm đảm bảo tính minh bạch, khả năng lặp lại và có thể mở rộng cho các nghiên cứu tương tự.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Quy trình 6 bước xây dựng Chỉ số FVI cấp cơ sở</div>', unsafe_allow_html=True)
    
    # Sử dụng component Sequence để trực quan hóa sơ đồ workflow tuyến tính
    st.markdown('<div class="academic-paragraph">Mô hình diễn tiến quy trình kỹ thuật:</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <Sequence>
      <Step title="Bước 1. Xác định phạm vi đánh giá" subtitle="Đơn vị phân tích độc lập">
        Nghiên cứu tập trung vào các cơ sở hạ tầng thiết yếu gồm trường học và cơ sở y tế thuộc 5 phường trung tâm thành phố Huế. Mỗi đơn vị được xem như một đối tượng phân tích độc lập với đặc điểm riêng về vị trí, cơ sở vật chất, quy mô và năng lực ứng phó nhằm hỗ trợ trực tiếp việc xác định thứ tự ưu tiên đầu tư.
      </Step>
      <Step title="Bước 2. Lựa chọn bộ chỉ số" subtitle="Chuyên biệt hóa theo ngành">
        Hệ thống chỉ số dựa trên khung IPCC, tổng quan nghiên cứu quốc tế và đặc điểm y tế/giáo dục Việt Nam. Xây dựng hai bộ chỉ số riêng biệt cho Giáo dục và Y tế để phản ánh đúng yêu cầu vận hành. Áp dụng phân tích tương quan Pearson để loại bỏ biến trùng lặp thông tin.
      </Step>
      <Step title="Bước 3. Tổng hợp và tích hợp dữ liệu" subtitle="Cơ sở dữ liệu đa nguồn">
        Thu thập dữ liệu đa nguồn gồm dữ liệu không gian, ảnh vệ tinh Sentinel-1, số liệu thống kê và phiếu điều tra thực địa. Toàn bộ thông tin được đồng bộ về cùng hệ quy chiếu không gian và liên kết thông qua mã định danh duy nhất của từng cơ sở.
      </Step>
      <Step title="Bước 4. Tiền xử lý dữ liệu" subtitle="Kiểm soát hướng tác động">
        Kiểm tra dữ liệu thiếu và giá trị ngoại lệ, mã hóa biến định tính. Các biến làm tăng tổn thương (độ sâu lũ, quy mô học sinh) giữ chiều thuận. Các biến tăng khả năng chống chịu (máy phát điện, kế hoạch ứng phó) quy đổi theo chiều nghịch để đảm bảo tính nhất quán.
      </Step>
      <Step title="Bước 5. Chuẩn hóa dữ liệu" subtitle="Phương pháp Z-score">
        Loại bỏ ảnh hưởng của sự khác biệt đơn vị đo (mét, số người, năm, biến nhị phân) đưa về cùng thang đo chuẩn thông qua việc chuyển đổi dựa trên giá trị trung bình và độ lệch chuẩn của mẫu.
      </Step>
      <Step title="Bước 6. Xác định trọng số và tính toán FVI" subtitle="Thuật toán PCA & Jenks Natural Breaks">
        Áp dụng phân tích thành phần chính PCA để xác định trọng số từ cấu trúc thống kê nhằm loại bỏ tính chủ quan. Sau khi tính điểm tổng hợp tuyến tính FVI, áp dụng thuật toán Jenks Natural Breaks để phân loại các cơ sở thành 4 cấp độ tổn thương: Thấp, Trung bình, Tương đối cao và Cao.
      </Step>
    </Sequence>
    """, unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown('<div class="sub-section-title">Bố cục ma trận bộ chỉ số và nguồn dữ liệu đầu vào</div>', unsafe_allow_html=True)
    
    # Bảng số lượng chỉ số phân bổ
    indicator_df = pd.DataFrame([
        {"Thành phần cấu phần": "Exposure (Độ phơi nhiễm)", "Ngành Giáo dục (Trường học)": "Tính toán từ mô hình viễn thám", "Ngành Y tế (Cơ sở y tế)": "Tính toán từ mô hình viễn thám", "Nguồn dữ liệu tích hợp": "Bản đồ ngập từ Sentinel-1 và hệ thống GIS"},
        {"Thành phần cấu phần": "Sensitivity (Độ nhạy cảm)", "Ngành Giáo dục (Trường học)": "Quy mô học sinh, tuổi công trình, điểm sơ tán", "Ngành Y tế (Cơ sở y tế)": "Quy mô giường bệnh, nhân lực, thiết bị đặc thù", "Nguồn dữ liệu tích hợp": "Số liệu thống kê và Khảo sát thực địa"},
        {"Thành phần cấu phần": "Adaptive Capacity (Năng lực thích ứng)", "Ngành Giáo dục (Trường học)": "Phương tiện tại chỗ, kế hoạch diễn tập, hạ tầng", "Ngành Y tế (Cơ sở y tế)": "Nguồn điện dự phòng, thuốc men, năng lực ứng cứu", "Nguồn dữ liệu tích hợp": "Phiếu điều tra khảo sát thực địa trực tiếp"}
    ])
    st.table(indicator_df)
    
    st.markdown('<div class="sub-section-title">Công thức toán học áp dụng trong mô hình toán</div>', unsafe_allow_html=True)
    st.latex(r"Z_i = \frac{x_i - \bar{x}}{\sigma}")
    st.latex(r"FVI = \sum_{i=1}^{n} w_i Z_i")
    
    st.markdown('<div class="sub-section-title">Kết quả và ý nghĩa của quy trình xây dựng FVI</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Sau khi hoàn thành sáu bước xử lý, nghiên cứu xây dựng được Chỉ số tổn thương lũ cho toàn bộ 31 cơ sở giáo dục và y tế trong khu vực nghiên cứu. Bộ chỉ số này không chỉ phản ánh mức độ tổn thương tổng hợp mà còn cho phép phân tích riêng từng thành phần Độ phơi nhiễm (Exposure), Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity), giúp nhận diện nguyên nhân dẫn đến mức độ tổn thương của từng cơ sở.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Kết quả FVI là đầu vào cho các phân tích ở các trang tiếp theo, bao gồm bản đồ tổn thương, so sánh giữa các cơ sở và đề xuất các giải pháp ưu tiên nhằm nâng cao khả năng chống chịu của hệ thống giáo dục và y tế trước nguy cơ ngập lụt.</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: BẢN ĐỒ NGẬP BẰNG VIỄN THÁM
# ==========================================
with tab_viendam:
    st.markdown('<div class="sub-section-title">1. Giới thiệu tổng quan</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Hợp phần này đóng vai trò kỹ thuật nền tảng thuộc Bước 3 của quy trình tổng thể, cung cấp dữ liệu đầu vào cốt lõi để lượng hóa thành phần Độ phơi nhiễm (Exposure) trong Chỉ số tổn thương lũ (FVI). Nhằm đáp ứng yêu cầu phân tích chính xác tại vị trí của từng trường học và cơ sở y tế, nghiên cứu tiến hành xây dựng hệ thống bản đồ ngập độ phân giải cao 10 m từ ảnh radar vệ tinh Sentinel-1 kết hợp các thuật toán học máy (Machine Learning).</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">2. Lý do xây dựng lại bản đồ ngập từ ảnh viễn thám radar</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><b>Nâng cấp độ phân giải không gian từ 90 m sang 10 m:</b> Các bản đồ diện rộng trước đây (như lớp dữ liệu SPADE) sử dụng độ phân giải 90 m (pixel rộng 8.100 m²), quá thô để phân biệt rủi ro khu vực khuôn viên và cấu trúc công trình chính. Lớp bản đồ mới nâng cấp lên độ phân giải 10 m (ô ảnh 100 m²), giúp tăng chi tiết không gian và nhận diện chính xác rủi ro ngập của từng cơ sở.</li>
            <li><b>Lợi thế xuyên mây của cảm biến radar Sentinel-1 SAR:</b> Khác với ảnh quang học bị che phủ hoàn toàn bởi mây trong mùa mưa bão miền Trung, cảm biến radar khẩu độ tổng hợp (SAR) hoạt động bằng cách thu nhận bước sóng tán xạ ngược (VV, VH). Cơ chế này cho phép vệ tinh quan sát xuyên mây dày, vận hành liên tục cả ngày lẫn đêm ngay trong thời điểm xảy ra mưa lớn kỷ lục.</li>
            <li><b>Tối ưu hóa chi phí đầu tư dữ liệu:</b> Dữ liệu ảnh radar Sentinel-1 thuộc kho tài nguyên mở quốc tế. Việc khai thác nguồn ảnh này giúp giảm thiểu tối đa chi phí mua bản quyền ảnh thương mại đắt đỏ, tạo điều kiện thuận lợi cho việc cập nhật định kỳ mà không phụ thuộc vào ngân sách lớn.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Bảng so sánh các phương pháp xác định vùng ngập viễn thám</div>', unsafe_allow_html=True)
    compare_df = pd.DataFrame([
        {"Tiêu chí": "Độ phân giải không gian", "Bản đồ diện rộng (Ví dụ: SPADE)": "Thô (90 m)", "Phương pháp Phân ngưỡng (Thresholding)": "Trung bình (10 m - 20 m)", "Phương pháp Tích hợp Học máy (Dự án đề xuất)": "Cao (10 m)"},
        {"Tiêu chí": "Nguồn ảnh đầu vào", "Bản đồ diện rộng (Ví dụ: SPADE)": "Quang học / Mô hình thủy văn", "Phương pháp Phân ngưỡng (Thresholding)": "Radar đơn lẻ", "Phương pháp Tích hợp Học máy (Dự án đề xuất)": "Tích hợp đa nguồn (Radar + DEM + Khí tượng)"},
        {"Tiêu chí": "Hiệu quả tại khu vực đô thị", "Bản đồ diện rộng (Ví dụ: SPADE)": "Rất thấp (Không bắt được túi ngập nhỏ)", "Phương pháp Phân ngưỡng (Thresholding)": "Thấp (Bị nhiễu bởi phản xạ bề mặt bê tông)", "Phương pháp Tích hợp Học máy (Dự án đề xuất)": "Cao (Thuật toán lọc nhiễu cấu trúc công trình)"},
        {"Tiêu chí": "Chi phí dữ liệu đầu vào", "Bản đồ diện rộng (Ví dụ: SPADE)": "Thấp (Dữ liệu sẵn có)", "Phương pháp Phân ngưỡng (Thresholding)": "Thấp (Ảnh mở)", "Phương pháp Tích hợp Học máy (Dự án đề xuất)": "Tối ưu (Ảnh mở, khai thác hiệu năng thuật toán)"},
        {"Tiêu chí": "Độ phức tạp tính toán", "Bản đồ diện rộng (Ví dụ: SPADE)": "Thấp (Tra cứu có sẵn)", "Phương pháp Phân ngưỡng (Thresholding)": "Đơn giản (Dễ sai lệch vùng giáp ranh)", "Phương pháp Tích hợp Học máy (Dự án đề xuất)": "Trung bình - Cao (Đảm bảo độ chính xác học thuật)"}
    ])
    st.table(compare_df)
    
    st.markdown('---')
    st.markdown('<div class="sub-section-title">3. Quy trình triển khai hệ thống (Workflow)</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Quy trình công nghệ từ khai thác dữ liệu thô đến trích xuất chỉ số phơi nhiễm được vận hành theo sơ đồ tuyến tính 7 bước:</div>', unsafe_allow_html=True)
    
    # Sử dụng Timeline / text block hiển thị luồng sơ đồ
    st.code("""
Ảnh vệ tinh Sentinel-1 thô
      │
      ▼
 Tiền xử lý dữ liệu vật lý (Hiệu chỉnh quỹ đạo, địa hình, giảm nhiễu)
      │
      ▼
 Xây dựng bộ mẫu huấn luyện tích hợp (Khảo sát thực địa + Crowdsourcing)
      │
      ▼
 Huấn luyện và đánh giá chéo đa thuật toán học máy
      │
      ▼
 Lựa chọn mô hình tối ưu dựa trên chỉ số kiểm định độc lập
      │
      ▼
 Xây dựng bản đồ ngập theo từng sự kiện mưa lũ năm 2025
      │
      ▼
 Tổng hợp lớp ngập không gian theo chu kỳ kịch bản thiên tai
      │
      ▼
 Trích xuất cấu phần Exposure (Phơi nhiễm) cho 31 cơ sở hạ tầng
    """, language="text")
    
    st.markdown('---')
    st.markdown('<div class="sub-section-title">4. Dữ liệu đầu vào và xây dựng bộ mẫu huấn luyện</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Nghiên cứu sử dụng ảnh radar Sentinel-1 thu nhận trong mùa bão lũ năm 2025 làm nguồn dữ liệu cốt lõi. Sau khi thu thập, dữ liệu thô trải qua quy trình tiền xử lý chuẩn mực gồm: hiệu chỉnh quỹ đạo bay, giảm nhiễu speckle đặc thù của sóng radar, hiệu chỉnh địa hình bằng mô hình số độ cao (DEM) và đồng bộ về cùng một hệ tọa độ quy chiếu không gian đô thị.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Để huấn luyện thuật toán học máy phân loại chính xác mặt nước trong môi trường đô thị phức tạp, nghiên cứu đã tiến hành thu thập và xây dựng bộ dữ liệu mẫu tích hợp:</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><b>Khối lượng mẫu:</b> Tổng cộng trích xuất 630 điểm vị trí mẫu được thu thập đồng bộ tại 13 thời điểm thiên tai trọng điểm trong năm 2025 (bao gồm giai đoạn xảy ra chuỗi 4 trận lũ lịch sử tại Huế).</li>
            <li><b>Nguồn dữ liệu mẫu:</b> Kết hợp từ số liệu đo đạc thực địa của IWRP, báo cáo kỹ thuật của các cơ quan quản lý lũ lụt địa phương, kết hợp đối chiếu thông tin phạm vi ngập từ phương tiện truyền thông và dữ liệu bản đồ cộng đồng (crowdsourcing).</li>
            <li><b>Phân vùng đặc trưng sử dụng đất:</b> Toàn bộ 630 điểm mẫu được phân tách tỉ mỉ thành các nhóm loại hình sử dụng đất khác nhau, tập trung vào hai vùng có tính chất phản xạ sóng radar khác biệt hoàn toàn là Khu vực Đô thị kiên cố và Khu vực Nông nghiệp/Nông thôn để đảm bảo mô hình không bị lệch dòng phân loại.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">5. Huấn luyện và lựa chọn mô hình học máy</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Xác định phạm vi ngập tại các khu vực đô thị mật độ xây dựng cao luôn là một trong những thách thức hàng đầu của ngành viễn thám, do hiện tượng bóng radar của nhà cao tầng và phản xạ đa hướng của bề mặt bê tông dễ gây ra lỗi phân loại sai. Do đó, thay vì áp dụng các phương pháp phân ngưỡng đơn giản (Thresholding) dễ sai lệch, nghiên cứu lựa chọn giải pháp Học máy (Machine Learning) kết hợp bộ chỉ số đầu vào đa tầng dữ liệu nhằm tối ưu hóa độ chính xác, tốc độ trích xuất mà vẫn đảm bảo tính tiện lợi cao về mặt vận hành (chi phí đầu vào thấp, không đòi hỏi máy chủ siêu cấu hình).</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Nghiên cứu tiến hành huấn luyện thử nghiệm song song nhiều thuật toán học máy trên 3 nhóm cấu phần dữ liệu đầu vào khác nhau để đánh giá mức độ cải thiện độ chính xác:</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><i>Nhóm 1:</i> Chỉ sử dụng dữ liệu độ tán xạ ngược (VV, VH) từ ảnh Sentinel-1.</li>
            <li><i>Nhóm 2:</i> Tích hợp dữ liệu ảnh Sentinel-1 kết hợp dữ liệu mô hình số độ cao địa hình (DEM).</li>
            <li><i>Nhóm 3:</i> Tích hợp đồng thời ảnh Sentinel-1, dữ liệu địa hình (DEM) và số liệu khí tượng thời gian thực (Lượng mưa tích lũy 3 ngày và 7 ngày, nhiệt độ nền).</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Các thuật toán được đánh giá chéo khách quan thông qua bộ chỉ số tiêu chuẩn khoa học bao gồm: Độ chính xác toàn cục (Accuracy), Độ chính xác phân loại nước (Precision), Khả năng bắt trúng vùng ngập (Recall) và Chỉ số cân bằng F1-score trên bộ mẫu kiểm định độc lập.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">6. Kết quả lựa chọn mô hình tối ưu</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Qua đối chiếu thực nghiệm giữa các thuật toán phân lớp phổ biến (Random Forest, XGBoost và Gradient Boosting Machine), thuật toán Random Forest kết hợp với nhóm dữ liệu đầu vào số 3 đạt hiệu quả phân loại và duy trì độ ổn định cao nhất trên toàn bộ các địa hình.</div>', unsafe_allow_html=True)
    
    # Bảng số liệu kiểm định Random Forest
    rf_metrics_df = pd.DataFrame([
        {"Khu vực kiểm định": "Toàn bộ lưu vực nghiên cứu", "Độ chính xác (Accuracy)": "95%", "Khả năng bắt trúng vùng ngập (Recall)": "94%", "Chỉ số cân bằng F1-score": "0.85"},
        {"Khu vực kiểm định": "Khu vực Đô thị lõi", "Độ chính xác (Accuracy)": "97%", "Khả năng bắt trúng vùng ngập (Recall)": "100%", "Chỉ số cân bằng F1-score": "0.89"}
    ])
    st.table(rf_metrics_df)
    
    st.markdown("""
        <ul class="academic-list">
            <li>Tại khu vực đô thị lõi, mô hình đạt tỷ lệ <b>Recall = 100%</b>, khẳng định toàn bộ các vùng ngập thực tế nằm trong tập dữ liệu kiểm định đều được thuật toán nhận diện thành công, không xảy ra hiện tượng bỏ sót túi rủi ro.</li>
            <li>Chỉ số F1-score đạt <b>0.89</b> thể hiện sự cân bằng tối ưu giữa độ chính xác và khả năng tách lọc vùng ngập trong điều kiện môi trường đô thị có mật độ nhiễu vật lý cao từ các công trình xây dựng. Kết quả này chứng minh mô hình hoàn toàn đáp ứng đầy đủ tiêu chuẩn khoa học để làm dữ liệu đầu vào trích xuất rủi ro cấp công trình.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="academic-quote">
        <p><b>Gợi ý giao diện Web:</b> Tích hợp hình ảnh Ma trận nhầm lẫn - Confusion Matrix Heatmap và biểu đồ đối chiếu giữa ảnh thực địa Ground Truth và bản đồ dự đoán Prediction của mô hình ngay dưới bảng số liệu này.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">7. Xây dựng bản đồ ngập theo các kịch bản lũ và trích xuất chỉ số độ phơi nhiễm</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Sau khi xác định mô hình tối ưu, thuật toán Random Forest được chạy tự động để trích xuất bản đồ ngập cho từng sự kiện mưa bão trong năm 2025. Các lớp dữ liệu đơn lẻ này sau đó được chồng xếp không gian và tính toán tần suất để thiết lập hệ thống bản đồ ngập độ phân giải 10 m đại diện cho 4 kịch bản lũ theo chu kỳ lặp: 5 năm (xác suất 20%), 10 năm (10%), 20 năm (5%) và 100 năm (1%).</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Cuối cùng, 4 lớp bản đồ kịch bản lũ này được chồng xếp không gian với tọa độ vị trí của 22 trường học và 9 cơ sở y tế trong môi trường GIS để trích xuất cấu phần Độ phơi nhiễm (Exposure) cho từng đơn vị. Các chỉ số được số hóa tự động bao gồm: Độ sâu ngập trung bình ngay tại vị trí công trình; Tỷ lệ diện tích ngập của khu vực lân cận xung quanh; Khoảng cách hình học ngắn nhất từ cơ sở đến mạng lưới sông/kênh chính; Các đặc trưng không gian liên quan đến nguy cơ gián đoạn tuyến đường giao thông tiếp cận.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">8. Sản phẩm đầu ra của hợp phần</div>', unsafe_allow_html=True)
    st.markdown("""
        <ol class="academic-list">
            <li>Hệ thống bản đồ số ngập lụt độ phân giải 10 m cho 4 kịch bản chu kỳ lũ tại 5 phường trung tâm thành phố Huế.</li>
            <li>Mô hình Random Forest đã được tối ưu hóa tham số cấu trúc, đạt độ chính xác 95–97%.</li>
            <li>Bộ cơ sở dữ liệu số cấu phần Phơi nhiễm (Exposure) đã được chuẩn hóa, sẵn sàng tích hợp với dữ liệu Độ nhạy cảm và Năng lực thích ứng để hoàn thiện Chỉ số rủi ro FVI.</li>
        </ol>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 4: XÁC ĐỊNH TRỌNG SỐ VÀ XÂY DỰNG FVI
# ==========================================
with tab_weights_pca:
    st.markdown('<div class="sub-section-title">Giới thiệu cấu phần</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Đây là một phần trong bước 6 của nghiên cứu. Sau khi chuẩn hóa dữ liệu, nghiên cứu sử dụng Phân tích thành phần chính (Principal Component Analysis – PCA) để xác định trọng số cho các chỉ số thành phần của Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) đối với từng ngành.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">PCA là một phương pháp thống kê đa biến được sử dụng rộng rãi trong xây dựng các chỉ số tổng hợp nhằm phân tích mối quan hệ giữa các biến và xác định mức độ đóng góp của từng chỉ số vào sự biến thiên của bộ dữ liệu. Khác với phương pháp phổ biến khác (gán trọng số bằng nhau hoặc hoàn toàn dựa trên ý kiến chuyên gia), PCA xác định trọng số dựa trên cấu trúc thống kê của dữ liệu khảo sát, qua đó giảm tính chủ quan và hạn chế ảnh hưởng của hiện tượng đa cộng tuyến giữa các chỉ số. Trong nghiên cứu này, PCA chỉ được sử dụng để xác định trọng số, trong khi việc lựa chọn các chỉ số đầu vào được thực hiện dựa trên khung lý thuyết của IPCC, tổng quan tài liệu và đặc thù của lĩnh vực giáo dục và y tế.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="academic-paragraph">Sau khi xác định trọng số, điểm FVI được tính theo phương pháp tổng hợp tuyến tính:</div>', unsafe_allow_html=True)
    st.latex(r"FVI = \sum_{i=1}^{n} w_i Z_i")
    st.markdown('<div class="academic-paragraph">Trong đó: Z_i là giá trị chuẩn hóa của chỉ số thứ i; w_i là trọng số được xác định từ kết quả PCA.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Xây dựng Chỉ số tổn thương lũ</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Các trọng số xác định từ kết quả PCA được kết hợp với các giá trị đã chuẩn hóa để tính điểm Chỉ số tổn thương lũ (FVI) cho từng trường học và cơ sở y tế. Điểm FVI phản ánh mức độ tổn thương tương đối của mỗi cơ sở trên cơ sở tích hợp ba thành phần Độ phơi nhiễm (Exposure), Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity).</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Kết quả phân tích PCA cho hệ thống trường học</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Phân tích PCA được thực hiện riêng cho ba nhóm chỉ số Độ phơi nhiễm (Exposure), Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity) của 22 trường học trong khu vực nghiên cứu nhằm xác định trọng số cho từng nhóm chỉ số thành phần.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-section-title">Bảng tổng hợp kết quả phân tích PCA cho hệ thống Trường học</div>', unsafe_allow_html=True)
    pca_school_df = pd.DataFrame([
        {"Nhóm chỉ số": "Exposure (Phơi nhiễm)", "Thành phần chính": "PC1", "Phương sai giải thích (%)": "53.48", "Yếu tố chi phối": "Mức độ ngập tại trường học", "Ý nghĩa": "Phản ánh tác động trực tiếp của ngập lụt đến công trình"},
        {"Nhóm chỉ số": "Exposure (Phơi nhiễm)", "Thành phần chính": "PC2", "Phương sai giải thích (%)": "26.28", "Yếu tố chi phối": "Mức độ ngập khu vực lân cận", "Ý nghĩa": "Phản ánh ảnh hưởng của điều kiện ngập xung quanh đến khả năng tiếp cận và vận hành"},
        {"Nhóm chỉ số": "Exposure Tổng", "Thành phần chính": "-", "Phương sai giải thích (%)": "79.76", "Yếu tố chi phối": "Hai thành phần chính phản ánh phần lớn đặc điểm phơi nhiễm của các trường học", "Ý nghĩa": "-"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC1", "Phương sai giải thích (%)": "46.69", "Yếu tố chi phối": "Vai trò là điểm sơ tán", "Ý nghĩa": "Phản ánh áp lực của trường học trong công tác ứng phó thiên tai"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC2", "Phương sai giải thích (%)": "22.35", "Yếu tố chi phối": "Quy mô hoạt động", "Ý nghĩa": "Phản ánh quy mô nhân sự và số lượng học sinh phục vụ"},
        {"Nhóm chỉ số": "Sensitivity (Độ nhạy)", "Thành phần chính": "PC3", "Phương sai giải thích (%)": "14.89", "Yếu tố chi phối": "Đặc điểm công trình", "Ý nghĩa": "Phản ánh tuổi và đặc điểm của công trình"},
        {"Nhóm chỉ số": "Sensitivity Tổng", "Thành phần chính": "-", "Phương sai giải thích (%)": "83.94", "Yếu tố chi phối": "Ba thành phần chính phản ánh phần lớn sự khác biệt về độ nhạy cảm giữa các trường học", "Ý nghĩa": "-"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC1", "Phương sai giải thích (%)": "53.91", "Yếu tố chi phối": "Phương tiện ứng cứu", "Ý nghĩa": "Phản ánh khả năng tiếp cận và hỗ trợ trong điều kiện ngập lụt"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC2", "Phương sai giải thích (%)": "16.76", "Yếu tố chi phối": "Công tác lập kế hoạch", "Ý nghĩa": "Phản ánh mức độ chuẩn bị và tổ chức ứng phó"},
        {"Nhóm chỉ số": "Adaptive Capacity (Thích ứng)", "Thành phần chính": "PC3", "Phương sai giải thích (%)": "12.73", "Yếu tố chi phối": "Điều kiện hạ tầng", "Ý nghĩa": "Phản ánh khả năng duy trì hoạt động của trường học khi xảy ra thiên tai"},
        {"Nhóm chỉ số": "Adaptive Capacity Tổng", "Thành phần chính": "-", "Phương sai giải thích (%)": "83.40", "Yếu tố chi phối": "Ba thành phần chính phản ánh phần lớn năng lực thích ứng của hệ thống trường học", "Ý nghĩa": "-"}
    ])
    st.table(pca_school_df)
    
    st.markdown('<div class="sub-section-title">Diễn giải chi tiết kết quả thống kê</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li>Ba nhóm PCA giải thích từ 79,76% đến 83,94% tổng phương sai của dữ liệu, cho thấy các thành phần được giữ lại phản ánh phần lớn thông tin của các chỉ số ban đầu và đủ cơ sở để xác định trọng số trong mô hình FVI.</li>
            <li><b>Đối với Độ phơi nhiễm (Exposure):</b> hai thành phần chính đầu tiên giải thích gần 80% phương sai, trong đó mức độ ngập tại trường học là yếu tố chi phối lớn nhất, tiếp theo là mức độ ngập của khu vực lân cận. Kết quả cho thấy mức độ phơi nhiễm chịu tác động đồng thời bởi điều kiện ngập tại công trình và môi trường xung quanh.</li>
            <li><b>Đối với Độ nhạy cảm (Sensitivity):</b> ba nhóm yếu tố chính gồm vai trò của trường học trong ứng phó thiên tai, quy mô hoạt động và đặc điểm công trình là những yếu tố tạo nên sự khác biệt về mức độ nhạy cảm giữa các trường học.</li>
            <li><b>Đối với Năng lực thích ứng (Adaptive Capacity):</b> phương tiện ứng cứu, công tác lập kế hoạch và điều kiện hạ tầng là ba nhóm yếu tố đóng góp lớn nhất vào khả năng duy trì hoạt động và ứng phó của các trường học khi xảy ra ngập lụt.</li>
        </ul>
    """, unsafe_allow_html=True)
