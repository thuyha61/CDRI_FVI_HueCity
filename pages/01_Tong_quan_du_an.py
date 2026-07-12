from pathlib import Path

import streamlit as st


# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Tổng quan dự án | FVI Huế",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ĐƯỜNG DẪN
# File này nằm trong thư mục pages/, vì vậy thư mục gốc dự án
# là thư mục cha của pages/.
# ============================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"

IWRP_LOGO = ASSETS_DIR / "iwrp.png"
CDRI_LOGO = ASSETS_DIR / "cdri.jpg"


# ============================================================
# CSS DÙNG RIÊNG CHO TRANG
# ============================================================
st.markdown(
    """
    <style>
        /* Giảm khoảng trống phía trên nội dung chính */
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f5fbff 0%, #eef6f8 100%);
            border-right: 1px solid #dbe7eb;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.2rem;
        }

        .sidebar-project-title {
            font-size: 0.98rem;
            font-weight: 700;
            line-height: 1.45;
            color: #123c4a;
            text-align: center;
            margin: 0.85rem 0 0.25rem 0;
        }

        .sidebar-project-subtitle {
            font-size: 0.78rem;
            line-height: 1.45;
            color: #58717a;
            text-align: center;
            margin-bottom: 0.8rem;
        }

        /* Hero banner */
        .hero-banner {
            padding: 2.2rem 2.4rem;
            border-radius: 22px;
            background:
                radial-gradient(circle at 92% 18%, rgba(255,255,255,0.18), transparent 25%),
                linear-gradient(120deg, #075985 0%, #087f8c 52%, #0f766e 100%);
            color: white;
            box-shadow: 0 12px 30px rgba(7, 89, 133, 0.16);
            margin-bottom: 1.25rem;
        }

        .hero-kicker {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            margin-bottom: 0.9rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.25);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-title {
            font-size: clamp(1.85rem, 3.2vw, 3.25rem);
            font-weight: 800;
            line-height: 1.16;
            margin: 0 0 0.8rem 0;
        }

        .hero-title-en {
            font-size: 1rem;
            line-height: 1.55;
            opacity: 0.90;
            max-width: 980px;
            margin-bottom: 1.25rem;
        }

        .hero-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem 0.85rem;
            margin-top: 0.75rem;
        }

        .hero-meta-item {
            padding: 0.42rem 0.72rem;
            border-radius: 10px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            font-size: 0.88rem;
        }

        /* Tiêu đề khu vực */
        .section-heading {
            margin: 0.35rem 0 0.25rem 0;
            color: #123c4a;
            font-size: 1.45rem;
            font-weight: 800;
        }

        .section-intro {
            color: #5a7078;
            margin-bottom: 1rem;
        }

        /* Quick links */
        .quick-link-card {
            min-height: 116px;
            padding: 1.05rem 1.1rem;
            border: 1px solid #dbe7eb;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 5px 16px rgba(22, 61, 73, 0.05);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .quick-link-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 9px 22px rgba(22, 61, 73, 0.09);
        }

        .quick-link-icon {
            font-size: 1.45rem;
            margin-bottom: 0.4rem;
        }

        .quick-link-title {
            color: #123c4a;
            font-size: 0.98rem;
            font-weight: 750;
            margin-bottom: 0.2rem;
        }

        .quick-link-note {
            color: #6a7f87;
            font-size: 0.82rem;
            line-height: 1.4;
        }

        /* Thẻ nội dung */
        .content-card {
            padding: 1.15rem 1.25rem;
            border: 1px solid #dfeaed;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 4px 14px rgba(22, 61, 73, 0.04);
            margin-bottom: 0.85rem;
        }

        .content-card h4 {
            color: #14556a;
            margin: 0 0 0.5rem 0;
        }

        .content-card p {
            margin-bottom: 0;
            color: #3f555d;
            line-height: 1.65;
        }

        /* Quote */
        .highlight-quote {
            margin: 1.1rem 0;
            padding: 1.05rem 1.25rem;
            border-left: 5px solid #0d9488;
            border-radius: 0 14px 14px 0;
            background: #ecfdf5;
            color: #115e59;
            font-size: 1.04rem;
            font-weight: 700;
            line-height: 1.55;
        }

        /* KPI */
        .kpi-card {
            height: 100%;
            padding: 1rem 0.85rem;
            text-align: center;
            border: 1px solid #dce8eb;
            border-radius: 15px;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbfc 100%);
        }

        .kpi-value {
            color: #075985;
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .kpi-label {
            color: #61767e;
            font-size: 0.82rem;
            line-height: 1.35;
            margin-top: 0.35rem;
        }

        /* Contribution cards */
        .contribution-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #e0f2fe;
            color: #075985;
            font-weight: 800;
            margin-bottom: 0.65rem;
        }

        /* Table */
        .project-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5rem;
            font-size: 0.93rem;
        }

        .project-table th {
            padding: 0.75rem;
            background: #eaf4f6;
            color: #194a59;
            text-align: left;
            border: 1px solid #d8e5e9;
        }

        .project-table td {
            padding: 0.75rem;
            border: 1px solid #e0e9ec;
            vertical-align: top;
            color: #3f555d;
        }

        .project-table tr:nth-child(even) td {
            background: #fafcfd;
        }

        /* Timeline */
        .timeline-item {
            padding: 0.75rem 0.9rem;
            border-left: 4px solid #0d9488;
            background: #f7fbfb;
            border-radius: 0 12px 12px 0;
            margin-bottom: 0.65rem;
            color: #3f555d;
        }

        .timeline-item strong {
            color: #14556a;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            font-size: 0.91rem;
            font-weight: 700;
        }

        /* Footer */
        .page-footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #dfe8eb;
            color: #71858c;
            font-size: 0.8rem;
            text-align: center;
        }

        @media (max-width: 768px) {
            .hero-banner {
                padding: 1.5rem 1.25rem;
            }

            .hero-title {
                font-size: 1.75rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HÀM HỖ TRỢ
# ============================================================
def show_sidebar() -> None:
    """Hiển thị logo và thông tin dự án ở thanh bên trái."""
    with st.sidebar:
        logo_col_1, logo_col_2 = st.columns([1, 1], gap="small")

        with logo_col_1:
            if IWRP_LOGO.exists():
                st.image(str(IWRP_LOGO), use_container_width=True)
            else:
                st.caption("Thiếu file assets/iwrp.png")

        with logo_col_2:
            if CDRI_LOGO.exists():
                st.image(str(CDRI_LOGO), use_container_width=True)
            else:
                st.caption("Thiếu file assets/cdri.jpg")

        st.markdown(
            """
            <div class="sidebar-project-title">
                BẢN ĐỒ RỦI RO NGẬP LỤT THEO NGÀNH
            </div>
            <div class="sidebar-project-subtitle">
                Tăng cường ứng phó và thích ứng với biến đổi khí hậu
                tại Thành phố Huế
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        st.caption("CDRI Fellowship Programme 2025–2026")
        st.caption("Đơn vị thực hiện: Viện Quy hoạch Thủy lợi")
        st.caption("Khu vực nghiên cứu: Thành phố Huế, Việt Nam")


def quick_link_card(icon: str, title: str, note: str) -> None:
    """Hiển thị thẻ liên kết nhanh dạng tĩnh."""
    st.markdown(
        f"""
        <div class="quick-link-card">
            <div class="quick-link-icon">{icon}</div>
            <div class="quick-link-title">{title}</div>
            <div class="quick-link-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(value: str, label: str) -> None:
    """Hiển thị một KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def content_card(title: str, body: str) -> None:
    """Hiển thị khối nội dung dạng card."""
    st.markdown(
        f"""
        <div class="content-card">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
show_sidebar()


# ============================================================
# HERO BANNER
# ============================================================
st.markdown(
    """
    <section class="hero-banner">
        <div class="hero-kicker">CDRI Fellowship 2025–2026</div>
        <h1 class="hero-title">
            Bản đồ rủi ro ngập lụt theo ngành nhằm tăng cường ứng phó
            và thích ứng với biến đổi khí hậu tại Thành phố Huế
        </h1>
        <div class="hero-title-en">
            Sectoral Flood Risk Mapping to Enhance Climate Change Response
            and Adaptation in Hue City, Vietnam
        </div>
        <div class="hero-meta">
            <div class="hero-meta-item">🏛️ Viện Quy hoạch Thủy lợi (IWRP)</div>
            <div class="hero-meta-item">🤝 Coalition for Disaster Resilient Infrastructure (CDRI)</div>
            <div class="hero-meta-item">📍 Thành phố Huế, Việt Nam</div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TRUY CẬP NHANH
# ============================================================
st.markdown('<div class="section-heading">Truy cập nhanh</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-intro">Khám phá bản đồ, báo cáo và dữ liệu của dự án.</div>',
    unsafe_allow_html=True,
)

quick_col_1, quick_col_2, quick_col_3 = st.columns(3, gap="medium")

with quick_col_1:
    quick_link_card(
        "🗺️",
        "Khám phá bản đồ tương tác",
        "Tra cứu vị trí, điểm FVI và mức độ tổn thương của từng cơ sở.",
    )
    if st.button(
        "Mở trang Bản đồ và kết quả",
        key="open_map_page",
        use_container_width=True,
        type="primary",
    ):
        try:
            st.switch_page("pages/04_Ban_do_va_ket_qua.py")
        except Exception:
            st.info("Trang Bản đồ và kết quả sẽ được kích hoạt sau khi file Trang 4 được tạo.")

with quick_col_2:
    quick_link_card(
        "📄",
        "Báo cáo nghiên cứu",
        "Báo cáo tổng hợp sẽ được cập nhật sau khi hoàn thành nghiệm thu.",
    )
    st.button(
        "Chưa có tệp tải xuống",
        key="report_placeholder",
        use_container_width=True,
        disabled=True,
    )

with quick_col_3:
    quick_link_card(
        "📂",
        "Dữ liệu mở",
        "Bộ dữ liệu sẽ được công bố sau khi kết quả nghiên cứu được phê duyệt.",
    )
    st.button(
        "Chưa công bố dữ liệu",
        key="data_placeholder",
        use_container_width=True,
        disabled=True,
    )

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# CÁC TAB NỘI DUNG
# ============================================================
tab_overview, tab_contribution, tab_project, tab_results = st.tabs(
    [
        "1. Tổng quan",
        "2. Đóng góp của nghiên cứu",
        "3. Dự án nghiên cứu",
        "4. Kết quả và giá trị ứng dụng",
    ]
)


# ------------------------------------------------------------
# TAB 1: TỔNG QUAN
# ------------------------------------------------------------
with tab_overview:
    st.markdown("### Bối cảnh nghiên cứu")

    st.markdown(
        """
        Lũ lụt là một trong những loại hình thiên tai gây thiệt hại nghiêm trọng
        đối với hệ thống hạ tầng đô thị. Dưới tác động của biến đổi khí hậu,
        tần suất và cường độ của các hiện tượng mưa cực đoan có xu hướng gia tăng,
        đặc biệt tại các đô thị ven biển và vùng đồng bằng thấp.

        Tại Việt Nam, khu vực miền Trung thường xuyên chịu ảnh hưởng của các đợt
        ngập lụt kéo dài. Thành phố Huế có mức độ rủi ro cao do đặc điểm địa hình
        thấp trũng, mạng lưới sông dày đặc và lượng mưa lớn. Đợt mưa lịch sử năm
        2025, với lượng mưa 24 giờ đạt 1.739 mm, tiếp tục cho thấy yêu cầu cấp
        thiết phải nâng cao năng lực chống chịu của hệ thống hạ tầng thiết yếu.
        """
    )

    st.markdown(
        """
        Trường học và cơ sở y tế giữ vai trò quan trọng trong bảo đảm an sinh,
        duy trì dịch vụ thiết yếu, hỗ trợ sơ tán và cứu trợ khẩn cấp. Khi các
        công trình này bị ngập hoặc bị cô lập, tác động không chỉ giới hạn ở
        thiệt hại vật chất mà còn làm gián đoạn khả năng tiếp cận giáo dục, y tế
        và làm suy giảm năng lực phục hồi của cộng đồng.
        """
    )

    st.markdown(
        """
        Dự án **“Bản đồ rủi ro ngập lụt theo ngành nhằm tăng cường ứng phó và
        thích ứng với biến đổi khí hậu tại Thành phố Huế”** ứng dụng dữ liệu
        viễn thám, hệ thống thông tin địa lý (GIS), khảo sát thực địa và phân
        tích thống kê để đánh giá 31 cơ sở giáo dục và y tế tại 5 phường trung
        tâm thành phố Huế. Nghiên cứu xây dựng bản đồ phơi nhiễm ngập lụt và
        Chỉ số tổn thương lũ ở cấp từng cơ sở.
        """
    )

    st.markdown(
        """
        <div class="highlight-quote">
            💡 Không phải mọi cơ sở nằm trong cùng một vùng ngập đều có mức độ
            tổn thương giống nhau.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        Khả năng chống chịu và tốc độ phục hồi của từng công trình không chỉ phụ
        thuộc vào mức độ ngập, mà còn chịu ảnh hưởng bởi đặc điểm công trình,
        quy mô phục vụ, trang thiết bị và năng lực ứng phó tại chỗ. Vì vậy,
        Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) được xây dựng để
        tích hợp các yếu tố không gian và các đặc trưng nội tại, qua đó làm rõ
        sự khác biệt giữa từng cơ sở.

        Kết quả nghiên cứu hỗ trợ cơ quan quản lý lồng ghép thông tin rủi ro vào
        quy hoạch, xác định công trình cần ưu tiên đầu tư và chủ động xây dựng
        kế hoạch thích ứng.
        """
    )

    st.markdown("### Các chỉ số nổi bật")
    kpi_cols = st.columns(6, gap="small")
    kpis = [
        ("31", "Cơ sở được đánh giá"),
        ("22", "Trường học"),
        ("9", "Cơ sở y tế"),
        ("5", "Phường nghiên cứu"),
        ("10 m", "Độ phân giải bản đồ"),
        ("95–97%", "Độ chính xác mô hình"),
    ]

    for column, (value, label) in zip(kpi_cols, kpis):
        with column:
            kpi_card(value, label)

    st.markdown("### Các sản phẩm của dự án")
    st.markdown(
        """
        Dự án xây dựng một hệ thống sản phẩm phục vụ đồng thời công tác quản lý,
        nghiên cứu và chia sẻ dữ liệu.
        """
    )

    st.markdown(
        """
        <table class="project-table">
            <thead>
                <tr>
                    <th style="width:34%">Sản phẩm</th>
                    <th>Nội dung</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>🗺️ <strong>Bản đồ phơi nhiễm ngập lụt</strong></td>
                    <td>Phạm vi và mức độ ngập theo các kịch bản khác nhau.</td>
                </tr>
                <tr>
                    <td>📍 <strong>Bản đồ Chỉ số tổn thương lũ (FVI)</strong></td>
                    <td>Đánh giá mức độ tổn thương của từng trường học và cơ sở y tế.</td>
                </tr>
                <tr>
                    <td>📊 <strong>Cơ sở dữ liệu FVI</strong></td>
                    <td>Bộ dữ liệu chuẩn hóa phục vụ phân tích, cập nhật và quản lý.</td>
                </tr>
                <tr>
                    <td>💻 <strong>Website tương tác</strong></td>
                    <td>Tra cứu bản đồ, dữ liệu và kết quả nghiên cứu.</td>
                </tr>
                <tr>
                    <td>📄 <strong>Báo cáo nghiên cứu</strong></td>
                    <td>Trình bày phương pháp, kết quả và khuyến nghị.</td>
                </tr>
                <tr>
                    <td>📑 <strong>Khuyến nghị chính sách</strong></td>
                    <td>Hỗ trợ quản lý rủi ro và thích ứng với biến đổi khí hậu.</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# TAB 2: ĐÓNG GÓP CỦA NGHIÊN CỨU
# ------------------------------------------------------------
with tab_contribution:
    st.markdown("### Khoảng trống trong các nghiên cứu hiện nay")
    st.markdown(
        """
        Mặc dù đã có nhiều nghiên cứu và bản đồ ngập lụt được xây dựng, việc
        chuyển hóa kết quả thành thông tin hỗ trợ ra quyết định đối với từng
        công trình hạ tầng thiết yếu vẫn còn một số hạn chế.
        """
    )

    gap_col_1, gap_col_2 = st.columns(2, gap="large")

    with gap_col_1:
        content_card(
            "Thiếu bộ chỉ số đánh giá theo từng lĩnh vực",
            """
            Phần lớn các nghiên cứu sử dụng một bộ chỉ số chung cho nhiều loại
            hình hạ tầng. Cách tiếp cận này chưa phản ánh đầy đủ sự khác biệt về
            chức năng, yêu cầu vận hành và tiêu chí chống chịu giữa trường học
            và cơ sở y tế.
            """,
        )
        st.markdown(
            """
            Đối với **trường học**, các yếu tố như quy mô học sinh, khả năng duy
            trì hoạt động giảng dạy, vai trò là điểm sơ tán và công tác bảo đảm
            an toàn cho học sinh cần được xem xét.

            Đối với **cơ sở y tế**, khả năng duy trì hoạt động khám chữa bệnh,
            nguồn điện dự phòng, trang thiết bị y tế, hệ thống cấp nước và năng
            lực cấp cứu khẩn cấp lại có ý nghĩa quyết định.
            """
        )

    with gap_col_2:
        content_card(
            "Thiếu đánh giá ở cấp từng cơ sở",
            """
            Nhiều nghiên cứu đánh giá rủi ro theo đơn vị hành chính hoặc theo
            ô lưới không gian. Cách tiếp cận này phù hợp để mô tả xu hướng chung
            nhưng chưa cung cấp đủ thông tin để quản lý và ưu tiên đầu tư cho
            từng công trình cụ thể.
            """,
        )
        st.markdown(
            """
            Các cơ sở nằm trong cùng một khu vực ngập có thể có mức độ tổn
            thương rất khác nhau do sự khác biệt về vị trí, cao độ nền, điều
            kiện cơ sở vật chất, quy mô phục vụ, trang thiết bị và năng lực ứng
            phó. Đánh giá ở cấp cơ sở giúp nhận diện chính xác hơn các đơn vị
            cần ưu tiên.
            """
        )

    st.markdown("### Ba đóng góp chính của nghiên cứu")
    contribution_cols = st.columns(3, gap="medium")

    contributions = [
        (
            "1",
            "Phát triển bộ chỉ số theo từng lĩnh vực",
            """
            Xây dựng hai bộ chỉ số riêng cho giáo dục và y tế, phản ánh đặc điểm
            hoạt động và yêu cầu chống chịu của từng nhóm hạ tầng.
            """,
        ),
        (
            "2",
            "Đánh giá ở cấp từng cơ sở",
            """
            Tính toán chỉ số tổn thương cho từng trường học và từng cơ sở y tế,
            thay vì chỉ đánh giá ở cấp phường hoặc ô lưới không gian.
            """,
        ),
        (
            "3",
            "Tích hợp đa nguồn dữ liệu",
            """
            Kết hợp Sentinel-1, GIS, khảo sát thực địa và phân tích thống kê để
            đánh giá toàn diện mức độ tổn thương của từng cơ sở.
            """,
        ),
    ]

    for column, (number, title, body) in zip(contribution_cols, contributions):
        with column:
            st.markdown(
                f"""
                <div class="content-card" style="height:100%;">
                    <div class="contribution-number">{number}</div>
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ------------------------------------------------------------
# TAB 3: DỰ ÁN NGHIÊN CỨU
# ------------------------------------------------------------
with tab_project:
    st.markdown("### Mục tiêu nghiên cứu")
    st.markdown(
        """
        Dự án hướng tới xây dựng một hệ thống thông tin hỗ trợ quản lý rủi ro
        ngập lụt đối với trường học và cơ sở y tế tại thành phố Huế thông qua
        bốn mục tiêu chính:
        """
    )

    objectives = [
        "Xây dựng bản đồ phơi nhiễm ngập lụt độ phân giải cao bằng dữ liệu viễn thám và công nghệ học máy.",
        "Phát triển Chỉ số tổn thương lũ (Flood Vulnerability Index – FVI) cho từng trường học và cơ sở y tế.",
        "Phân tích các yếu tố ảnh hưởng đến mức độ tổn thương nhằm hỗ trợ xác định ưu tiên đầu tư.",
        "Phát triển bản đồ tương tác và cơ sở dữ liệu phục vụ quản lý, quy hoạch và nghiên cứu.",
    ]

    for index, objective in enumerate(objectives, start=1):
        st.markdown(
            f"""
            <div class="timeline-item">
                <strong>Mục tiêu {index}.</strong> {objective}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Phạm vi nghiên cứu")
    st.markdown(
        """
        <table class="project-table">
            <thead>
                <tr>
                    <th style="width:32%">Nội dung</th>
                    <th>Thông tin</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Khu vực nghiên cứu</strong></td>
                    <td>5 phường trung tâm thành phố Huế</td>
                </tr>
                <tr>
                    <td><strong>Đối tượng</strong></td>
                    <td>22 trường học và 9 cơ sở y tế</td>
                </tr>
                <tr>
                    <td><strong>Quy mô khảo sát</strong></td>
                    <td>31 cơ sở</td>
                </tr>
                <tr>
                    <td><strong>Nguồn dữ liệu</strong></td>
                    <td>Sentinel-1, GIS, số liệu thống kê và khảo sát thực địa</td>
                </tr>
                <tr>
                    <td><strong>Thời gian thực hiện</strong></td>
                    <td>2025–2026</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Phương pháp tiếp cận")
    method_cols = st.columns(5, gap="small")
    methods = [
        ("🛰️", "Ảnh viễn thám Sentinel-1"),
        ("🌐", "Hệ thống thông tin địa lý"),
        ("📋", "Khảo sát thực địa"),
        ("📐", "Chuẩn hóa và PCA"),
        ("📊", "Chỉ số FVI"),
    ]

    for column, (icon, label) in zip(method_cols, methods):
        with column:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="quick-link-icon">{icon}</div>
                    <div class="kpi-label" style="font-weight:700;color:#194a59;">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Quy trình xây dựng bản đồ ngập và Chỉ số FVI được trình bày chi tiết "
        "tại Trang “Phương pháp nghiên cứu”."
    )

    st.markdown("### Tiến độ thực hiện")
    timeline = [
        "Thiết kế nghiên cứu",
        "Thu thập và tổng hợp dữ liệu",
        "Khảo sát thực địa",
        "Xây dựng bản đồ ngập",
        "Xây dựng Chỉ số FVI",
        "Phân tích kết quả",
        "Phát triển website và công bố sản phẩm",
    ]

    for index, item in enumerate(timeline, start=1):
        st.markdown(
            f"""
            <div class="timeline-item">
                <strong>{index:02d}</strong>&nbsp;&nbsp;{item}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# TAB 4: KẾT QUẢ VÀ GIÁ TRỊ ỨNG DỤNG
# ------------------------------------------------------------
with tab_results:
    st.markdown("### Kết quả nổi bật")
    st.markdown(
        """
        Nghiên cứu đã xây dựng bản đồ phơi nhiễm ngập lụt độ phân giải 10 m và
        Chỉ số tổn thương lũ cho 31 trường học và cơ sở y tế tại thành phố Huế.
        Mô hình phát hiện vùng ngập từ ảnh Sentinel-1 đạt độ chính xác 95–97%,
        tạo nền tảng cho việc đánh giá rủi ro ở cấp từng cơ sở.

        Kết quả phân tích xác định **5 cơ sở có mức độ tổn thương cao** và
        **1 cơ sở có mức độ tổn thương tương đối cao**, đồng thời làm rõ các yếu
        tố chính ảnh hưởng đến mức độ tổn thương của từng đơn vị.
        """
    )

    result_kpi_cols = st.columns(5, gap="small")
    result_kpis = [
        ("31", "Cơ sở được đánh giá"),
        ("5", "Mức tổn thương cao"),
        ("1", "Mức tương đối cao"),
        ("10 m", "Độ phân giải bản đồ"),
        ("95–97%", "Độ chính xác mô hình"),
    ]

    for column, (value, label) in zip(result_kpi_cols, result_kpis):
        with column:
            kpi_card(value, label)

    st.markdown("### Giá trị ứng dụng")
    application_cols = st.columns(3, gap="medium")

    applications = [
        (
            "🏛️ Đối với cơ quan quản lý",
            """
            Hỗ trợ xác định các cơ sở cần ưu tiên đầu tư, nâng cấp; đồng thời
            lồng ghép thông tin rủi ro vào quy hoạch, kế hoạch phòng chống thiên
            tai và thích ứng với biến đổi khí hậu.
            """,
        ),
        (
            "🏫 Đối với ngành giáo dục và y tế",
            """
            Cung cấp cơ sở để từng đơn vị rà soát hạn chế về cơ sở vật chất,
            trang thiết bị và năng lực ứng phó, từ đó xây dựng kế hoạch nâng cao
            khả năng chống chịu phù hợp.
            """,
        ),
        (
            "🔬 Đối với nghiên cứu và phát triển",
            """
            Đề xuất quy trình đánh giá rủi ro ở cấp cơ sở có thể mở rộng sang
            các loại hình hạ tầng khác hoặc áp dụng tại các địa phương có điều
            kiện tương tự.
            """,
        ),
    ]

    for column, (title, body) in zip(application_cols, applications):
        with column:
            content_card(title, body)


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="page-footer">
        Viện Quy hoạch Thủy lợi (IWRP) · CDRI Fellowship Programme 2025–2026
        <br>
        Bản đồ rủi ro ngập lụt theo ngành tại Thành phố Huế
    </div>
    """,
    unsafe_allow_html=True,
)
