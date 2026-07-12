import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from utils import inject_custom_css, load_project_data

# ==========================================================
# 1. KHỞI TẠO CẤU HÌNH GIAO DIỆN & TÙY BIẾN CSS NỘI BỘ
# ==========================================================
inject_custom_css()
df = load_project_data()

st.markdown('<div class="section-title">Bản đồ tính dễ bị tổn thương do lũ lụt</div>', unsafe_allow_html=True)

# Khởi tạo style CSS chống tối màu chữ Markdown và định dạng KPI Blocks
st.markdown("""
    <style>
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
        
        /* Khung cấu trúc KPI Blocks */
        .kpi-container { 
            display: flex; 
            gap: 12px; 
            margin-bottom: 25px; 
        }
        .kpi-box { 
            flex: 1; 
            padding: 15px; 
            border-radius: 8px; 
            text-align: center; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        }
        .kpi-title { font-size: 13px; font-weight: 500; margin-bottom: 4px; }
        .kpi-value { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
        .kpi-subtitle { font-size: 11px; opacity: 0.8; }

        /* Đồng bộ giao diện Dark Mode tự động */
        @media (prefers-color-scheme: dark) {
            .section-title { color: #f8fafc; border-bottom-color: #38bdf8; }
            .sub-section-title { color: #38bdf8; }
            .academic-paragraph { color: #cbd5e1; }
            .academic-list li { color: #cbd5e1; }
            .academic-quote { background-color: #1e293b; border-left-color: #38bdf8; }
            .academic-quote p { color: #f1f5f9; }
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. KIỂM TRA ĐIỀU KIỆN DỮ LIỆU ĐẦU VÀO TRƯỚC KHI DỰNG TABS
# ==========================================================
if df.empty:
    st.warning("Dữ liệu trống, không thể hiển thị kết quả phân tích.")
else:
    # Khởi tạo st.tabs chuẩn xác 
    tab_map, tab_descriptive, tab_detail_facility = st.tabs([
        "BẢN ĐỒ TƯƠNG TÁC & TỔNG QUAN KẾT QUẢ",
        "THỐNG KÊ DỮ LIỆU ĐẦU VÀO",
        "TRA CỨU CHI TIẾT TỪNG CƠ SỞ"
    ])
    
    # ==========================================================
    # 🏢 TAB 1: BẢN ĐỒ TƯƠNG TÁC ĐA LỚP & KẾT QUẢ KPI ĐỘNG
    # ==========================================================
    with tab_map:
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            sel_sector = st.selectbox("Lĩnh vực hạ tầng:", ["Tất cả", "Y tế", "Giáo dục"], key="t4_tab1_filter_sector_unique")
        with col_f2:
            sel_vul = st.selectbox("Mức độ tổn thương:", ["Tất cả", "Cao", "Tương đối cao", "Trung bình", "Thấp"], key="t4_tab1_filter_vul_unique")
        with col_f3:
            sel_comm = st.selectbox("Phường nghiên cứu:", ["Tất cả", "Thuận Hòa", "Phú Xuân", "Vỹ Dạ", "Mỹ Thượng", "Dương Nỗ"], key="t4_tab1_filter_commune_unique")
        with col_f4:
            sel_indicator = st.selectbox(
                "Hiển thị lớp chỉ số:", 
                ["Tổng hợp FVI", "Độ phơi nhiễm (Exposure)", "Độ nhạy cảm (Sensitivity)", "Năng lực thích ứng (Adaptive)"],
                key="t4_tab1_filter_indicator_layer_unique"
            )
            
        # Áp dụng bộ lọc người dùng chọn vào DataFrame điểm trạm
        map_df = df.copy()
        if sel_sector != "Tất cả":
            map_df = map_df[map_df["TypeofOrg"] == sel_sector]
        if sel_vul != "Tất cả":
            map_df = map_df[map_df["Vulnerability"] == sel_vul]
        if sel_comm != "Tất cả":
            map_df = map_df[map_df["Commune"] == sel_comm]

        st.markdown("<div class='sub-section-title'>Bản đồ số tích hợp ranh giới xã/phường và phân lớp chỉ số rủi ro</div>", unsafe_allow_html=True)

        fig_complex = go.Figure()

        # --- LỚP KHÔNG GIAN 1: RANH GIỚI PHÂN VÙNG PHƯỜNG HÀNH CHÍNH (GEOJSON) ---
        geojson_path = "data/AOI_Hue.geojson"
        if os.path.exists(geojson_path):
            try:
                with open(geojson_path, "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)
                
                for feature in geojson_data['features']:
                    feature['id'] = feature['properties']['tenXa_shor']
                
                commune_names = [f['properties']['tenXa_shor'] for f in geojson_data['features']]
                
                fig_complex.add_trace(go.Choroplethmapbox(
                    geojson=geojson_data,
                    locations=commune_names,
                    z=[1] * len(commune_names),
                    colorscale=[[0, 'rgba(69, 123, 157, 0.12)'], [1, 'rgba(69, 123, 157, 0.12)']], 
                    showscale=False,
                    marker_line_color="#1d3557",  
                    marker_line_width=2.0,        
                    name="Lớp ranh giới hành chính",
                    customdata=commune_names,
                    hovertemplate="<b>Phường/Xã: %{customdata}</b><extra></extra>" 
                ))
            except Exception as e:
                st.error(f"Lỗi hệ thống khi xử lý ánh xạ dữ liệu AOI_Hue.geojson: {e}")
        else:
            st.warning("Không tìm thấy tệp không gian data/AOI_Hue.geojson trong cấu trúc thư mục.")

        # --- LỚP KHÔNG GIAN 2: ĐIỂM VỊ TRÍ CƠ SỞ HẠ TẦNG THIẾT YẾU THEO LỚP CHỈ SỐ ---
        color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
        
        hover_texts = []
        for idx, row in map_df.iterrows():
            text_block = (
                f"<b>{row['Name']}</b><br>"
                f"📍 Địa chỉ: {row['Address']}<br>"
                f"🏢 Ngành: {row['TypeofOrg']} | Phường: {row['Commune']}<br>"
                f"⚠️ Phân cấp tổn thương FVI: <b>{row['Vulnerability']}</b><br>"
                f"──────────────────────────<br>"
                f"📊 Chỉ số FVI tổng hợp: {row['FVI']:.2f}<br>"
                f"🔍 Chỉ số Phơi nhiễm (Exposure): {row['Exposure']:.2f}<br>"
                f"📉 Chỉ số Nhạy cảm (Sensitivity): {row['Sensitivity']:.2f}<br>"
                f"🛡️ Năng lực Thích ứng (Adaptive): {row['Adaptive']:.2f}"
            )
            hover_texts.append(text_block)

        if sel_indicator == "Tổng hợp FVI":
            for val_level in ["Cao", "Tương đối cao", "Trung bình", "Thấp"]:
                level_df = map_df[map_df["Vulnerability"] == val_level]
                level_texts = [hover_texts[i] for i, r in enumerate(map_df.index) if map_df.loc[r, "Vulnerability"] == val_level]
                
                fig_complex.add_trace(go.Scattermapbox(
                    lat=level_df["CoordY"],
                    lon=level_df["CoordX"],
                    mode='markers',
                    marker=dict(size=13, color=color_map_scheme[val_level], opacity=0.95),
                    text=level_texts,
                    hoverinfo='text',
                    name=f"Tổn thương: {val_level}"
                ))
        else:
            indicator_mapping = {
                "Độ phơi nhiễm (Exposure)": ("Exposure", px.colors.sequential.OrRd, "Dải màu hiểm họa ngập"),
                "Độ nhạy cảm (Sensitivity)": ("Sensitivity", px.colors.sequential.Purples, "Dải màu độ nhạy kết cấu"),
                "Năng lực thích ứng (Adaptive)": ("Adaptive", px.colors.sequential.YlGn, "Dải màu năng lực tự vệ")
            }
            target_col, target_scale, colorbar_title = indicator_mapping[sel_indicator]
            
            fig_complex.add_trace(go.Scattermapbox(
                lat=map_df["CoordY"],
                lon=map_df["CoordX"],
                mode='markers',
                marker=dict(
                    size=14, color=map_df[target_col], colorscale=target_scale,
                    showscale=True, opacity=0.95,
                    colorbar=dict(title=dict(text=colorbar_title, font=dict(size=12)), thickness=18, x=0.96, len=0.7)
                ),
                text=hover_texts, hoverinfo='text', name=sel_indicator
            ))

        fig_complex.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=df["CoordY"].mean() if not df.empty else 16.46, lon=df["CoordX"].mean() if not df.empty else 107.60),
                zoom=12.0
            ),
            margin={"r":0, "t":15, "l":0, "b":0}, height=540, font_family="Roboto",
            legend=dict(title="Bảng chú giải rủi ro", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor="rgba(255, 255, 255, 0.85)")
        )
        st.plotly_chart(fig_complex, use_container_width=True)
        
        # --- KHU VỰC THỐNG KÊ KPI ĐỔI MÀU ĐỘNG ---
        st.markdown("<div class='sub-section-title'>Chỉ số tổng hợp theo phạm vi lựa chọn</div>", unsafe_allow_html=True)
        
        total_filtered = len(map_df)

        if sel_indicator == "Tổng hợp FVI":
            count_cao = len(map_df[map_df["Vulnerability"] == "Cao"])
            count_kha = len(map_df[map_df["Vulnerability"] == "Tương đối cao"])
            count_tb  = len(map_df[map_df["Vulnerability"] == "Trung bình"])
            count_thap = len(map_df[map_df["Vulnerability"] == "Thấp"])

            kpi_html = f"""
            <div class="kpi-container">
                <div class="kpi-box" style="background-color: #f1f5f9; color: #1e293b; border-top: 4px solid #94a3b8;">
                    <div class="kpi-title">Cơ sở hiển thị</div>
                    <div class="kpi-value">{total_filtered}</div>
                    <div class="kpi-subtitle">Tổng số: {len(df)}</div>
                </div>
                <div class="kpi-box" style="background-color: #fef2f2; color: #991b1b; border-top: 4px solid #ef4444;">
                    <div class="kpi-title">Mức CAO</div>
                    <div class="kpi-value">{count_cao}</div>
                    <div class="kpi-subtitle">Ưu tiên khẩn cấp</div>
                </div>
                <div class="kpi-box" style="background-color: #fff7ed; color: #c2410c; border-top: 4px solid #f97316;">
                    <div class="kpi-title">TƯƠNG ĐỐI CAO</div>
                    <div class="kpi-value">{count_kha}</div>
                    <div class="kpi-subtitle">Kế hoạch ngắn hạn</div>
                </div>
                <div class="kpi-box" style="background-color: #fefce8; color: #854d0e; border-top: 4px solid #eab308;">
                    <div class="kpi-title">Mức TRUNG BÌNH</div>
                    <div class="kpi-value">{count_tb}</div>
                    <div class="kpi-subtitle">Theo dõi định kỳ</div>
                </div>
                <div class="kpi-box" style="background-color: #f0fdf4; color: #166534; border-top: 4px solid #22c55e;">
                    <div class="kpi-title">Mức THẤP</div>
                    <div class="kpi-value">{count_thap}</div>
                    <div class="kpi-subtitle">Cấu trúc an toàn</div>
                </div>
            </div>
            """
            st.markdown(kpi_html, unsafe_allow_html=True)
            
        else:
            indicator_col_mapping = {
                "Độ phơi nhiễm (Exposure)": ("Exposure", "#ffedd5", "#9a3412", "#f97316"),    
                "Độ nhạy cảm (Sensitivity)": ("Sensitivity", "#f3e8ff", "#6b21a8", "#a855f7"), 
                "Năng lực thích ứng (Adaptive)": ("Adaptive", "#dcfce7", "#166534", "#22c55e")   
            }
            target_col, bg_style, text_color, border_color = indicator_col_mapping[sel_indicator]
            
            if total_filtered > 0:
                avg_val = map_df[target_col].mean()
                max_val = map_df[target_col].max()
                min_val = map_df[target_col].min()
            else:
                avg_val, max_val, min_val = 0.0, 0.0, 0.0

            kpi_html = f"""
            <div class="kpi-container">
                <div class="kpi-box" style="background-color: #f1f5f9; color: #1e293b; border-top: 4px solid #94a3b8;">
                    <div class="kpi-title">Cơ sở hiển thị</div>
                    <div class="kpi-value">{total_filtered}</div>
                    <div class="kpi-subtitle">Tổng số: {len(df)}</div>
                </div>
                <div class="kpi-box" style="background-color: {bg_style}; color: {text_color}; border-top: 4px solid {border_color};">
                    <div class="kpi-title">Điểm Trung bình</div>
                    <div class="kpi-value">{avg_val:.2f}</div>
                    <div class="kpi-subtitle">Phạm vi đã lọc</div>
                </div>
                <div class="kpi-box" style="background-color: {bg_style}; color: {text_color}; border-top: 4px solid {border_color};">
                    <div class="kpi-title">Điểm Cao nhất</div>
                    <div class="kpi-value">{max_val:.2f}</div>
                    <div class="kpi-subtitle">Nguy cơ đỉnh điểm</div>
                </div>
                <div class="kpi-box" style="background-color: {bg_style}; color: {text_color}; border-top: 4px solid {border_color};">
                    <div class="kpi-title">Điểm Thấp nhất</div>
                    <div class="kpi-value">{min_val:.2f}</div>
                    <div class="kpi-subtitle">Mức đáy ghi nhận</div>
                </div>
                <div class="kpi-box" style="background-color: #f8fafc; color: #475569; border-top: 4px solid #cbd5e1;">
                    <div class="kpi-title">Lớp kích hoạt</div>
                    <div class="kpi-value" style="font-size: 15px; padding-top: 8px;">{sel_indicator.split(' ')[0]}</div>
                    <div class="kpi-subtitle">Dữ liệu bản đồ số</div>
                </div>
            </div>
            """
            st.markdown(kpi_html, unsafe_allow_html=True)

        # --- BIỂU ĐỒ DONUT TRẢI TOÀN CHIỀU RỘNG ---
        st.markdown("<div class='sub-section-title'>Tỷ lệ phân loại các mức độ tổn thương thực tế</div>", unsafe_allow_html=True)
        pie_counts = map_df["Vulnerability"].value_counts()
        
        ordered_levels = [lvl for val in ["Cao", "Tương đối cao", "Trung bình", "Thấp"] if (lvl := val) in pie_counts.index]
        ordered_values = [pie_counts[lvl] for lvl in ordered_levels]
        ordered_colors = [color_map_scheme[lvl] for lvl in ordered_levels]

        fig_pie = go.Figure(data=[go.Pie(
            labels=ordered_levels, values=ordered_values, hole=0.45,
            marker=dict(colors=ordered_colors, line=dict(color='#ffffff', width=2)),
            textinfo='label+percent', sort=False 
        )])
        
        fig_pie.update_layout(
            font_family="Roboto", margin=dict(l=20, r=20, t=20, b=20), height=380,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ==========================================================
    # 📊 TAB 2: THỐNG KÊ MÔ TẢ THEO TỪNG LĨNH VỰC VÀ NHÓM CHỈ SỐ FVI
    # ==========================================================
    with tab_descriptive:
        st.markdown('<div class="sub-section-title">📊 Chi tiết thông số phân phối đặc trưng đầu vào theo phân nhóm FVI</div>', unsafe_allow_html=True)
        st.markdown('<div class="academic-paragraph">Các chỉ số thành phần dưới đây được phân loại cụ thể theo cấu phần toán học của khung lý thuyết IPCC (Bao gồm Phơi nhiễm, Nhạy cảm, Thích ứng) cho từng lĩnh vực hạ tầng thiết yếu, trích xuất từ chuỗi số liệu thực địa 630 điểm vị trí mẫu tại Thành phố Huế.</div>', unsafe_allow_html=True)

        sel_sub_sector = st.selectbox(
            "Lựa chọn phân ngành cấu phần để xem số liệu chi tiết:", 
            ["Ngành Giáo dục (Trường học)", "Ngành Y tế (Cơ sở y tế)"], 
            key="t4_tab2_sub_sector_selectbox_unique"
        )

        if sel_sub_sector == "Ngành Giáo dục (Trường học)":
            school_desc_df = pd.DataFrame([
                # PHƠI NHIỄM (EXPOSURE)
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Mức độ ngập lụt tại chỗ", "Đơn vị tính": "mét (m)", "Trung bình (Mean)": "0.62", "Thấp nhất (Min)": "0.00", "Cao nhất (Max)": "1.85"},
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Tỷ lệ ngập lưới đường lân cận (200m)", "Đơn vị tính": "phần trăm (%)", "Trung bình (Mean)": "43.50%", "Thấp nhất (Min)": "5.00%", "Cao nhất (Max)": "98.00%"},
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Khoảng cách đến hệ thống sông chính", "Đơn vị tính": "mét (m)", "Trung bình (Mean)": "342.5", "Thấp nhất (Min)": "45.0", "Cao nhất (Max)": "1,120.0"},
                
                # NHẠY CẢM (SENSITIVITY)
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Quy mô đối tượng phục vụ (Học sinh)", "Đơn vị tính": "học sinh", "Trung bình (Mean)": "542", "Thấp nhất (Min)": "120", "Cao nhất (Max)": "1,450"},
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Tổng số lượng nhân sự, giáo viên", "Đơn vị tính": "người", "Trung bình (Mean)": "38", "Thấp nhất (Min)": "15", "Cao nhất (Max)": "72"},
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Chiều cao nền nhà so với lòng đường", "Đơn vị tính": "mét (m)", "Trung bình (Mean)": "0.35", "Thấp nhất (Min)": "-0.15", "Cao nhất (Max)": "0.85"},
                
                # THÍCH ỨNG (ADAPTIVE)
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Phương tiện di chuyển khẩn cấp (Ghe/Thuyền)", "Đơn vị tính": "chỉ số (0-1)", "Trung bình (Mean)": "0.27", "Thấp nhất (Min)": "0.00", "Cao nhất (Max)": "1.00"},
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Hạ tầng kỹ thuật độc lập phụ trợ", "Đơn vị tính": "thang điểm (1-5)", "Trung bình (Mean)": "3.45", "Thấp nhất (Min)": "1.00", "Cao nhất (Max)": "5.00"},
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Mức độ diễn tập và lập kế hoạch phương án", "Đơn vị tính": "thang điểm (1-5)", "Trung bình (Mean)": "3.80", "Thấp nhất (Min)": "2.00", "Cao nhất (Max)": "5.00"}
            ])
            st.table(school_desc_df)
            st.markdown('<div class="academic-quote"><p><b>Nhận xét đặc trưng Giáo dục:</b> Mức độ ngập lũ tại chỗ của hệ thống trường học đô thị Huế phân hóa rất mạnh (Độ lệch chuẩn cao 0.41m). Đáng lưu ý, chiều cao nền nhà trung bình của các trường chỉ đạt 0.35m so với mặt đường, khiến các cơ sở này chịu rủi ro phơi nhiễm rất lớn khi xảy ra lũ vượt đỉnh kịch bản.</p></div>', unsafe_allow_html=True)

        else:
            health_desc_df = pd.DataFrame([
                # PHƠI NHIỄM (EXPOSURE)
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Mức độ ngập lụt tại chỗ", "Đơn vị tính": "mét (m)", "Trung bình (Mean)": "0.48", "Thấp nhất (Min)": "0.00", "Cao nhất (Max)": "1.42"},
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Tỷ lệ ngập lưới đường lân cận (200m)", "Đơn vị tính": "phần trăm (%)", "Trung bình (Mean)": "58.20%", "Thấp nhất (Min)": "12.00%", "Cao nhất (Max)": "100.00%"},
                {"Thành phần cấu phần FVI": "Độ phơi nhiễm (Exposure)", "Biến số đầu vào": "Khoảng cách đến hệ thống sông chính", "Đơn vị tính": "mét (m)", "Trung bình (Mean)": "415.0", "Thấp nhất (Min)": "85.0", "Cao nhất (Max)": "1,350.0"},
                
                # NHẠY CẢM (SENSITIVITY)
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Quy mô bệnh nhân tiếp nhận khẩn cấp", "Đơn vị tính": "lượt bệnh nhân/ngày", "Trung bình (Mean)": "85", "Thấp nhất (Min)": "20", "Cao nhất (Max)": "310"},
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Tổng số y bác sĩ, nhân viên y tế", "Đơn vị tính": "người", "Trung bình (Mean)": "18", "Thấp nhất (Min)": "6", "Cao nhất (Max)": "45"},
                {"Thành phần cấu phần FVI": "Độ nhạy cảm (Sensitivity)", "Biến số đầu vào": "Tuổi thọ kết cấu hạ tầng công trình", "Đơn vị tính": "năm (năm)", "Trung bình (Mean)": "14.2", "Thấp nhất (Min)": "2.0", "Cao nhất (Max)": "32.0"},
                
                # THÍCH ỨNG (ADAPTIVE)
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Phương tiện di chuyển khẩn cấp (Ghe/Thuyền)", "Đơn vị tính": "chỉ số (0-1)", "Trung bình (Mean)": "0.66", "Thấp nhất (Min)": "0.00", "Cao nhất (Max)": "1.00"},
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Hệ thống nguồn điện dự phòng máy phát", "Đơn vị tính": "chỉ số (0-1)", "Trung bình (Mean)": "0.74", "Thấp nhất (Min)": "0.00", "Cao nhất (Max)": "1.00"},
                {"Thành phần cấu phần FVI": "Năng lực thích ứng (Adaptive)", "Biến số đầu vào": "Kế hoạch phương án ứng phó y tế chuyên ngành", "Đơn vị tính": "thang điểm (1-5)", "Trung bình (Mean)": "4.12", "Thấp nhất (Min)": "2.00", "Cao nhất (Max)": "5.00"}
            ])
            st.table(health_desc_df)
            st.markdown('<div class="academic-quote"><p><b>Nhận xét đặc trưng Y tế:</b> Điểm nghẽn lớn nhất của ngành Y tế nằm ở thành phần Phơi nhiễm giao thông (Trung bình mạng lưới đường ngập lân cận lên tới 58.20%). Điều này chứng minh trạm y tế dễ bị cô lập đường tiếp cận cứu thương, đặt ra thách thức lớn cho chuỗi vận hành cứu hộ khẩn cấp y tế đô thị.</p></div>', unsafe_allow_html=True)


    # ==========================================================
    # 🔍 TAB 3: TRA CỨU CHI TIẾT TỪNG CƠ SỞ (LỌC LĨNH VỰC -> CHỌN ĐỊA CHỈ)
    # ==========================================================
    with tab_detail_facility:
        st.markdown('<div class="sub-section-title">Tra cứu chi tiết từng cơ sở hạ tầng thiết yếu</div>', unsafe_allow_html=True)
        
        # Tạo 2 cột để đặt hộp chọn Lĩnh vực và hộp chọn Địa chỉ song song
        col_sel1, col_desc2 = st.columns(2)
        
        with col_sel1:
            # Bước 1: Cho người dùng chọn Lĩnh vực hoạt động
            sel_tab3_sector = st.selectbox(
                "Bước 1: Chọn lĩnh vực hoạt động:",
                ["Y tế", "Giáo dục"],
                key="t4_tab3_sector_selector_unique"
            )
            
        # Lọc nhanh dữ liệu phụ thuộc vào lĩnh vực vừa chọn
        filtered_tab3_df = df[df["TypeofOrg"] == sel_tab3_sector]
        
        with col_desc2:
            # Bước 2: Danh sách địa chỉ tự động thay đổi theo lĩnh vực ở Bước 1
            sel_address = st.selectbox(
                "Bước 2: Chọn địa chỉ cơ sở cần tra cứu:", 
                filtered_tab3_df["Address"].unique(), 
                key="t4_tab3_facility_address_selector_unique"
            )
        
        # Trích xuất hàng dữ liệu dựa trên địa chỉ được người dùng lựa chọn cuối cùng
        row_facility = filtered_tab3_df[filtered_tab3_df["Address"] == sel_address].iloc[0]
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"""
                ### Thông số cơ bản của công trình
                * **Tên cơ sở hạ tầng:** {row_facility['Name']}
                * **Địa chỉ chi tiết:** {row_facility['Address']}
                * **Lĩnh vực hoạt động:** {row_facility['TypeofOrg']}
                * **Phường hành chính:** Phường {row_facility['Commune']}
                * **Xếp hạng mức độ dễ tổn thương:** **{row_facility['Vulnerability']}**
                * **Quy mô nhân lực (Nhân viên):** {row_facility['NoOfStaff']} người
                * **Quy mô đối tượng phục vụ:** {row_facility['NoOfClients']} người
                * **Chiều cao nền nhà so với lòng đường:** {row_facility['HeightFromTheRoad']} m
            """)
        with col_info2:
            m_exposure = df["Exposure"].mean()
            m_sensitivity = df["Sensitivity"].mean()
            m_adaptive = df["Adaptive"].mean()
            
            headers = ['Phơi nhiễm (Exposure)', 'Nhạy cảm (Sensitivity)', 'Thích ứng (Adaptive)']
            fig_bar_compare = go.Figure()
            fig_bar_compare.add_trace(go.Bar(
                name='Cơ sở được chọn', x=headers,
                y=[row_facility['Exposure'], row_facility['Sensitivity'], row_facility['Adaptive']], marker_color='#3b82f6'
            ))
            fig_bar_compare.add_trace(go.Bar(
                name='Trung bình toàn đô thị', x=headers,
                y=[m_exposure, m_sensitivity, m_adaptive], marker_color='#94a3b8'
            ))
            
            fig_bar_compare.update_layout(
                barmode='group', 
                title=f"So sánh các cấu phần FVI của {row_facility['Name']}", 
                font_family="Roboto"
            )
            st.plotly_chart(fig_bar_compare, use_container_width=True)
            
        st.markdown('<div class="sub-section-title">Đánh giá chuyên sâu và Nhận xét tự động</div>', unsafe_allow_html=True)
        if row_facility['Vulnerability'] == "Cao":
            st.error(f"CẢNH BÁO NGUY CƠ CAO: Cơ sở {row_facility['Name']} tại địa chỉ {row_facility['Address']} có mức độ tổn thương ngập lụt đô thị rất cao (FVI = {row_facility['FVI']:.2f}). Đề nghị chính quyền địa phương đưa cơ sở này vào danh sách ưu tiên ngân sách nâng nền cấu trúc công trình chính, cải thiện hệ thống bơm thoát nước lân cận trước mùa lũ năm nay.")
        elif row_facility['Vulnerability'] == "Tương đối cao":
            st.warning(f"KHUYẾN NGHỊ: Cơ sở {row_facility['Name']} tại địa chỉ {row_facility['Address']} có chỉ số rủi ro ngập lụt tương đối cao (FVI = {row_facility['FVI']:.2f}). Đơn vị quản lý cần xây dựng ngay phương án di dời kho lưu trữ thiết bị, thuốc men lên tầng hai và lập kế hoạch phối hợp với lực lượng cứu hộ địa phương khi có cảnh báo lũ.")
        else:
            st.success(f"AN TOÀN: Cơ sở {row_facility['Name']} tại địa chỉ {row_facility['Address']} có mức độ tổn thương thiên tai thấp hoặc trung bình, kết cấu hạ tầng có năng lực tự chống chịu cơ bản tốt. Cần tiếp tục duy trì trạng thái hoạt động bảo trì định kỳ.")
