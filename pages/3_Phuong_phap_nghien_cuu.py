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
st.markdown('<div class="section-title">PHƯƠNG PHÁP NGHIÊN CỨU</div>', unsafe_allow_html=True)
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
            <li><b>Độ phơi nhiễm - Exposure</b> – phản ánh mức độ tiếp xúc của cơ sở với ngập lụt.</li>
            <li><b>Độ nhạy cảm - Sensitivity</b> – phản ánh những đặc điểm làm gia tăng mức độ ảnh hưởng khi xảy ra ngập.</li>
            <li><b>Khả năng thích ứng - Adaptive Capacity</b> – phản ánh khả năng chuẩn bị, ứng phó và phục hồi của cơ sở.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="academic-paragraph">Về mặt khái niệm:</div>', unsafe_allow_html=True)
    st.latex(r"Flood\ Vulnerability = f(Exposure,\ Sensitivity,\ Adaptive\ Capacity)")
    st.markdown('<div class="academic-paragraph">Trong đó, mức độ tổn thương tăng khi Exposure và Sensitivity tăng, đồng thời giảm khi Adaptive Capacity được cải thiện.</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: XÂY DỰNG CHỈ SỐ FVI
# ==========================================
with tab_workflow:
    st.markdown('<div class="sub-section-title">Giới thiệu tổng quan</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) được xây dựng nhằm lượng hóa mức độ tổn thương của từng trường học và cơ sở y tế trước nguy cơ ngập lụt. Khác với các chỉ số được tính toán ở cấp xã, phường hoặc trên các ô lưới không gian, FVI trong nghiên cứu này được xây dựng ở cấp từng cơ sở, cho phép phản ánh sự khác biệt về điều kiện hạ tầng, quy mô hoạt động và năng lực ứng phó của từng đơn vị.</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Quy trình xây dựng FVI được thiết kế theo sáu bước độc lập nhằm đảm bảo tính minh bạch, khả năng lặp lại và có thể mở rộng cho các nghiên cứu tương tự.</div>', unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown('<div class="section-title" style="font-size: 22px; border-bottom: 2px solid #457b9d;">CHI TIẾT 6 BƯỚC TRIỂN KHAI KỸ THUẬT</div>', unsafe_allow_html=True)
    
    # --- BƯỚC 1 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 1. Xác định phạm vi đánh giá</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Bước đầu tiên của quá trình xây dựng FVI là xác định rõ đối tượng và phạm vi đánh giá. Nghiên cứu tập trung vào các cơ sở cơ sở hạ tầng thiết yếu, bao gồm trường học và cơ sở y tế thuộc năm phường trung tâm thành phố Huế.
    </div>
    <div class="academic-paragraph">
        Khác với nhiều nghiên cứu đánh giá ở cấp đơn vị hành chính, đơn vị phân tích trong nghiên cứu này là <b>từng cơ sở</b>. Mỗi trường học hoặc cơ sở y tế được xem như một đơn vị độc lập với tập hợp các đặc điểm riêng về vị trí, điều kiện cơ sở vật chất, quy mô phục vụ và năng lực ứng phó. Cách tiếp cận này giúp phản ánh chính xác hơn sự khác biệt về mức độ tổn thương giữa các cơ sở, đồng thời hỗ trợ trực tiếp cho việc xác định thứ tự ưu tiên trong đầu tư và quản lý.
    </div>
    """, unsafe_allow_html=True)
    
    # --- BƯỚC 2 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 2. Lựa chọn bộ chỉ số chuyên biệt</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Hệ thống chỉ số được lựa chọn dựa trên ba cơ sở: (i) khung lý thuyết của IPCC về đánh giá rủi ro thiên tai; (ii) tổng quan các nghiên cứu về chỉ số tổn thương do lũ; và (iii) đặc điểm hoạt động của hệ thống giáo dục và y tế tại Việt Nam.
    </div>
    <div class="academic-paragraph">
        Thay vì sử dụng một bộ chỉ số chung cho nhiều loại hình hạ tầng, nghiên cứu xây dựng hai bộ chỉ số riêng cho lĩnh vực giáo dục và lĩnh vực y tế nhằm phản ánh đúng yêu cầu vận hành và khả năng chống chịu của từng nhóm đối tượng.
    </div>
    <div class="academic-paragraph">
        Sau khi tổng hợp danh mục chỉ số ban đầu, các biến được rà soát để loại bỏ những biến trùng lặp thông tin hoặc có chất lượng dữ liệu không đảm bảo. Phân tích tương quan Pearson được sử dụng để nhận diện các cặp biến có mức tương quan cao, trong khi mức độ đầy đủ và khả năng thu thập dữ liệu cũng được xem xét nhằm đảm bảo tính khả thi của bộ chỉ số cuối cùng.
    </div>
    """, unsafe_allow_html=True)

    # Chèn bảng phân bổ ma trận chỉ số ngay dưới Bước 2 để minh họa trực quan
    indicator_df = pd.DataFrame([
        {"Thành phần cấu phần": "Exposure (Độ phơi nhiễm)", "Ngành Giáo dục (Trường học)": "Tính toán từ mô hình viễn thám", "Ngành Y tế (Cơ sở y tế)": "Tính toán từ mô hình viễn thám", "Nguồn dữ liệu tích hợp": "Bản đồ ngập từ Sentinel-1 và hệ thống GIS"},
        {"Thành phần cấu phần": "Sensitivity (Độ nhạy cảm)", "Ngành Giáo dục (Trường học)": "Quy mô học sinh, tuổi công trình, điểm sơ tán", "Ngành Y tế (Cơ sở y tế)": "Quy mô giường bệnh, nhân lực, thiết bị đặc thù", "Nguồn dữ liệu tích hợp": "Số liệu thống kê và Khảo sát thực địa"},
        {"Thành phần cấu phần": "Adaptive Capacity (Năng lực thích ứng)", "Ngành Giáo dục (Trường học)": "Phương tiện tại chỗ, kế hoạch diễn tập, hạ tầng", "Ngành Y tế (Cơ sở y tế)": "Nguồn điện dự phòng, thuốc men, năng lực ứng cứu", "Nguồn dữ liệu tích hợp": "Phiếu điều tra khảo sát thực địa trực tiếp"}
    ])
    st.table(indicator_df)
    
    # --- BƯỚC 3 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 3. Tổng hợp và tích hợp dữ liệu đa nguồn</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Dữ liệu phục vụ xây dựng FVI được thu thập từ nhiều nguồn khác nhau, bao gồm ảnh viễn thám, dữ liệu không gian, số liệu thống kê và khảo sát thực địa.
    </div>
    <div class="academic-paragraph">
        Các nguồn dữ liệu có sự khác biệt về định dạng, độ phân giải và đơn vị đo. Do đó, toàn bộ dữ liệu được chuẩn hóa về cùng hệ quy chiếu không gian và liên kết thông qua mã định danh của từng cơ sở. Quá trình này tạo thành một cơ sở dữ liệu thống nhất, trong đó mỗi trường học hoặc cơ sở y tế được mô tả bằng đầy đủ các biến thuộc ba nhóm thành phần của FVI.
    </div>
    """, unsafe_allow_html=True)
    
    # --- BƯỚC 4 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 4. Tiền xử lý dữ liệu và kiểm soát hướng tác động</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Trước khi tính toán chỉ số, các biến đầu vào được kiểm tra nhằm đảm bảo tính nhất quán và phù hợp với phân tích thống kê. Quá trình tiền xử lý bao gồm: kiểm tra dữ liệu thiếu và giá trị ngoại lệ; xác định chiều tác động của từng chỉ số; mã hóa các biến định tính; chuẩn hóa cấu trúc dữ liệu giữa các nguồn.
    </div>
    <div class="academic-paragraph">
        Đối với các biến có tác động làm gia tăng mức độ tổn thương (ví dụ: độ sâu ngập hoặc quy mô đối tượng phục vụ), giá trị được giữ theo chiều thuận. Ngược lại, các biến phản ánh khả năng chống chịu (ví dụ: máy phát điện dự phòng, trang thiết bị ứng cứu hoặc kế hoạch ứng phó) được quy đổi theo chiều nghịch để đảm bảo tính nhất quán trong quá trình tổng hợp chỉ số.
    </div>
    """, unsafe_allow_html=True)
    
    # --- BƯỚC 5 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 5. Chuẩn hóa dữ liệu bằng phương pháp Z-score</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Các biến đầu vào của FVI có đơn vị đo và phạm vi giá trị rất khác nhau, bao gồm mét, số người, năm xây dựng, khoảng cách và các biến nhị phân. Vì vậy, việc chuẩn hóa dữ liệu là cần thiết nhằm loại bỏ ảnh hưởng của đơn vị đo và đưa các biến về cùng một thang đo.
    </div>
    <div class="academic-paragraph">
        Nghiên cứu sử dụng phương pháp chuẩn hóa Z-score, trong đó mỗi giá trị được chuyển đổi dựa trên giá trị trung bình và độ lệch chuẩn của mẫu. Sau chuẩn hóa, các biến có giá trị trung bình bằng 0 và độ lệch chuẩn bằng 1, tạo điều kiện thuận lợi cho việc so sánh và tính toán trọng số.
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"Z_i = \frac{x_i - \bar{x}}{\sigma}")
    
    # --- BƯỚC 6 ---
    st.markdown('<div class="sub-section-title" style="color: #1d3557;">📍 Bước 6. Xác định trọng số PCA và tính toán tổng hợp FVI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="academic-paragraph">
        Sau khi chuẩn hóa bằng Z-score, các biến đầu vào được đưa vào phân tích Thành phần chính (PCA) để xác định hệ số tải và trọng số tương ứng ($w_i$). Các trọng số này được sử dụng để tính Chỉ số tổn thương lũ (FVI) theo phương pháp tổng hợp tuyến tính.
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"FVI = \sum_{i=1}^{n} w_i Z_i")
    st.markdown("""
    <div class="academic-paragraph">
        Sau khi tính toán điểm FVI, các cơ sở được phân thành bốn mức độ tổn thương gồm: <b>Thấp, Trung bình, Tương đối cao và Cao</b>. Việc phân nhóm được thực hiện bằng phương pháp Jenks Natural Breaks (Phân loại đứt gãy tự nhiên) nhằm tối đa hóa sự khác biệt giữa các nhóm và tối thiểu hóa sự khác biệt trong cùng một nhóm.
    </div>
    <div class="academic-paragraph">
        Nhờ đó, kết quả phân loại phản ánh tốt hơn đặc điểm phân bố thực tế của dữ liệu không gian, hỗ trợ trực quan hóa bản đồ và xác định chính xác các cơ sở cần ưu tiên cao nhất trong quản lý rủi ro thiên tai.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('<div class="sub-section-title">Kết quả và ý nghĩa của quy trình</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Sau khi hoàn thành sáu bước xử lý biệt lập này, nghiên cứu xây dựng được Chỉ số tổn thương lũ cho toàn bộ 32 cơ sở giáo dục và y tế trong khu vực nghiên cứu. Bộ chỉ số này không chỉ phản ánh mức độ tổn thương tổng hợp mà còn cho phép phân tích riêng từng thành phần Độ phơi nhiễm (Exposure), Độ nhạy cảm (Sensitivity) và Năng lực thích ứng (Adaptive Capacity), giúp nhận diện nguyên nhân gốc rễ dẫn đến mức độ tổn thương của từng cơ sở cụ thể.</div>', unsafe_allow_html=True)
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
    {
        "Tiêu chí": "Độ phân giải không gian", 
        "Bản đồ thủy lực (SPADE)": "Thô (90 m)", 
        "Viễn thám + Học máy": "Cao (10 m)"
    },
    {
        "Tiêu chí": "Năm xây dựng", 
        "Bản đồ thủy lực (SPADE)": "2016", 
        "Viễn thám + Học máy": "2026"
    },
    {
        "Tiêu chí": "Cung cấp thông tin ngập", 
        "Bản đồ thủy lực (SPADE)": "Có", 
        "Viễn thám + Học máy": "Có"
    },
    {
        "Tiêu chí": "Cung cấp thông tin độ cao và thời gian ngập", 
        "Bản đồ thủy lực (SPADE)": "Có", 
        "Viễn thám + Học máy": "Không"
    },
    {
        "Tiêu chí": "Nguồn ảnh đầu vào", 
        "Bản đồ thủy lực (SPADE)": "Thủy văn, khí tượng, địa hình, mặt cắt (phức tạp)", 
        "Viễn thám + Học máy": "Tích hợp đa nguồn miễn phí (Radar + DEM + Khí tượng)"
    },
    {
        "Tiêu chí": "Hiệu quả tại khu vực đô thị", 
        "Bản đồ thủy lực (SPADE)": "Rất thấp", 
        "Viễn thám + Học máy": "Cao hơn"
    },
    {
        "Tiêu chí": "Chi phí cập nhật", 
        "Bản đồ thủy lực (SPADE)": "Cao", 
        "Viễn thám + Học máy": "Thấp (Ảnh mở, khai thác hiệu năng thuật toán)"
    },
    {
        "Tiêu chí": "Độ phức tạp tính toán", 
        "Bản đồ thủy lực (SPADE)": "Cao", 
        "Viễn thám + Học máy": "Trung bình - Cao (Đảm bảo độ chính xác học thuật)"
    }
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
    st.markdown('<div class="academic-paragraph">Sau khi chuẩn hóa dữ liệu, nghiên cứu áp dụng phương pháp Phân tích Thành phần chính (PCA) để tự động hóa việc tính toán trọng số cho Chỉ số tổn thương lũ (FVI). Mô hình toán xác định tầm quan trọng của từng yếu tố dựa hoàn toàn trên cấu trúc thống kê khách quan của dữ liệu khảo sát thực tế, loại bỏ sự chủ quan và hiện tượng trùng lặp thông tin giữa các chỉ số đầu vào.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="academic-paragraph">Công thức tích hợp tuyến tính để thiết lập chỉ số FVI cuối cùng:</div>', unsafe_allow_html=True)
    st.latex(r"FVI = \sum_{i=1}^{n} w_i Z_i")
    st.markdown('<div class="academic-paragraph">Trong đó: Z_i là giá trị thực tế sau khi đã đưa về cùng thang đo chuẩn; w_i là trọng số tầm quan trọng được mô hình PCA xác định.</div>', unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown('<div class="sub-section-title">Bảng đối chiếu các yếu tố chi phối trọng số FVI: Trường học vs Y tế</div>', unsafe_allow_html=True)
    st.markdown('<div class="academic-paragraph">Bảng số liệu dưới đây mô tả tỷ lệ đóng góp (phương sai giải thích) và các yếu tố đời thường đóng vai trò quyết định, chi phối mạnh nhất đến việc hình thành nên trọng số của mô hình.</div>', unsafe_allow_html=True)

    # Đã sửa lỗi cú pháp: Đưa chữ in đậm vào trong chuỗi dữ liệu một cách hợp lệ
    pca_compact_df = pd.DataFrame([
        # --- ĐỘ PHƠI NHIỄM (EXPOSURE) ---
        {
            "Hợp phần FVI": "Exposure (Độ phơi nhiễm lũ)",
            "Thành phần chính": "Yếu tố cốt lõi 1",
            "Ngành Giáo dục (Trường học)": "57.36% | Ngập lụt trực tiếp tại vị trí trường",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "60.48% | Ngập đường lân cận (bán kính 200m)"
        },
        {
            "Hợp phần FVI": "",
            "Thành phần chính": "Yếu tố cốt lõi 2",
            "Ngành Giáo dục (Trường học)": "24.24% | Ngập đường lân cận (bán kính 200m)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "27.33% | Khoảng cách hình học tới sông chính"
        },
        {
            "Hợp phần FVI": "MỨC ĐỘ GIẢI THÍCH TÍCH LŨY",
            "Thành phần chính": "Tổng hợp mô hình",
            "Ngành Giáo dục (Trường học)": "81.60% (Đủ độ tin cậy khoa học)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "87.80% (Giải thích trọn vẹn đặc trưng)"
        },
        
        # --- ĐỘ NHẠY CẢM (SENSITIVITY) ---
        {
            "Hợp phần FVI": "Sensitivity (Độ nhạy cảm)",
            "Thành phần chính": "Yếu tố cốt lõi 1",
            "Ngành Giáo dục (Trường học)": "51.20% | Vai trò là điểm sơ tán tập trung",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "37.50% | Vai trò cứu trợ & Quy mô bệnh nhân"
        },
        {
            "Hợp phần FVI": "",
            "Thành phần chính": "Yếu tố cốt lõi 2",
            "Ngành Giáo dục (Trường học)": "24.40% | Quy mô con người (Học sinh & Giáo viên)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "28.67% | Mức độ xuống cấp theo tuổi công trình"
        },
        {
            "Hợp phần FVI": "MỨC ĐỘ GIẢI THÍCH TÍCH LŨY",
            "Thành phần chính": "Tổng hợp mô hình",
            "Ngành Giáo dục (Trường học)": "75.60% (Ưu tiên áp lực nhân sinh)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "66.17% (Kết hợp hạ tầng và tải bệnh nhân)"
        },
        
        # --- NĂNG LỰC THÍCH ỨNG (ADAPTIVITY) ---
        {
            "Hợp phần FVI": "Adaptivity (Năng lực thích ứng)",
            "Thành phần chính": "Yếu tố cốt lõi 1",
            "Ngành Giáo dục (Trường học)": "53.91% | Phương tiện đường thủy khẩn cấp (Ghe/Thuyền)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "53.91% | Phương tiện đường thủy khẩn cấp (Ghe/Thuyền)"
        },
        {
            "Hợp phần FVI": "",
            "Thành phần chính": "Yếu tố cốt lõi 2",
            "Ngành Giáo dục (Trường học)": "16.76% | Tính chủ động lập kế hoạch & Diễn tập",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "16.76% | Lập phương án tổ chức ứng phó y tế"
        },
        {
            "Hợp phần FVI": "",
            "Thành phần chính": "Yếu tố cốt lõi 3",
            "Ngành Giáo dục (Trường học)": "12.73% | Độ kiên cố của hệ thống hạ tầng kỹ thuật",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "12.73% | Nguồn điện và nước sạch dự phòng độc lập"
        },
        {
            "Hợp phần FVI": "MỨC ĐỘ GIẢI THÍCH TÍCH LŨY",
            "Thành phần chính": "Tổng hợp mô hình",
            "Ngành Giáo dục (Trường học)": "83.40% (Đầy đủ cấu phần giải pháp)",
            "Ngành Y tế (Trạm y tế / Bệnh viện)": "83.40% (Đảm bảo chuỗi y tế không đứt gãy)"
        }
    ])
    
    # Hiển thị bảng đối chiếu tinh gọn lên giao diện Streamlit
    st.table(pca_compact_df)
    
    st.markdown('<div class="sub-section-title">Luận cứ và phát hiện khoa học cốt lõi</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="academic-list">
            <li><b>Khác biệt lớn về Độ phơi nhiễm lũ:</b> Khả năng bị tổn thương của <b>Trường học</b> phụ thuộc trực tiếp vào việc bản thân khuôn viên trường có bị ngập sâu hay không (chiếm 57.36%). Ngược lại, <b>Cơ sở y tế</b> lại bị đe dọa lớn nhất bởi việc ngập các tuyến đường tiếp cận xung quanh trong bán kính 200m (chiếm 60.48%). Điều này phản ánh thực tế ngành y tế: nếu đường bị ngập cô lập, xe cứu thương không thể ra vào thì cơ sở y tế hoàn toàn bị tê liệt công năng khẩn cấp dù tòa nhà chính có khô ráo.</li>
            <li><b>Áp lực kép về Độ nhạy cảm:</b> Cả hai ngành đều phản ánh một điểm chung rất rõ: cơ sở hạ tầng nào được nhà nước chọn làm điểm sơ tán hoặc cứu trợ lũ cho người dân sẽ phải chịu áp lực tổn thương và quá tải cực kỳ lớn khi thiên tai xảy ra (yếu tố chi phối hàng đầu). Tuy nhiên, trường học nhạy cảm hơn về quy mô con người (số lượng học sinh lớn cần bảo vệ), trong khi trạm y tế nhạy cảm ở mức độ xuống cấp, tuổi thọ của công trình xây dựng.</li>
            <li><b>Sự đồng điệu trong Năng lực tự thích ứng:</b> Cấu trúc dữ liệu của cả hai ngành trùng khớp hoàn toàn về thứ tự ưu tiên các giải pháp chống chịu. Trọng số lớn nhất được mô hình gán cho phần cứng cứu nạn khẩn cấp tại chỗ (sự sẵn có của các phương tiện đường thủy), tiếp theo là phần mềm quản lý (chủ động diễn tập, lên phương án trước thiên tai) và cuối cùng là năng lực duy trì năng lượng độc lập (hệ thống máy phát điện, nước dự phòng) để sống sót khi đô thị bị cắt điện diện rộng.</li>
        </ul>
    """, unsafe_allow_html=True)
