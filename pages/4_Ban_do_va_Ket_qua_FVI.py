import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from utils import inject_custom_css, load_project_data

# 1. Khởi tạo cấu hình giao diện nền
inject_custom_css()
df = load_project_data()

st.markdown('<div class="section-title">Bản đồ tính dễ bị tổn thương do lũ lụt</div>', unsafe_allow_html=True)

# 2. Kiểm tra điều kiện dữ liệu trước khi dựng các Tab
if df.empty:
    st.warning("Dữ liệu trống, không thể hiển thị kết quả phân tích.")
else:
    tab_map, tab_descriptive, tab_detail_facility = st.tabs([
        "BẢN ĐỒ TƯƠNG TÁC & TỔNG QUAN KẾT QUẢ",
        "THỐNG KÊ DỮ LIỆU ĐẦU VÀO",
        "TRA CỨU CHI TIẾT TỪNG CƠ SỞ"
    ])
    
# ==========================================================
    # TẦNG HIỂN THỊ 1: BẢN ĐỒ TƯƠNG TÁC ĐA LỚP & KPI ĐỔI MÀU ĐỘNG
    # ==========================================================
    with tab_map:
        # Bộ lọc nâng cao chia thành 4 cột song song gọn gàng
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            sel_sector = st.selectbox("Lĩnh vực hạ tầng:", ["Tất cả", "Y tế", "Giáo dục"], key="map_sec")
        with col_f2:
            sel_vul = st.selectbox("Mức độ tổn thương:", ["Tất cả", "Cao", "Tương đối cao", "Trung bình", "Thấp"], key="map_vul")
        with col_f3:
            sel_comm = st.selectbox("Phường nghiên cứu:", ["Tất cả", "Thuận Hòa", "Phú Xuân", "Vỹ Dạ", "Mỹ Thượng", "Dương Nỗ"], key="map_comm")
        with col_f4:
            # Hộp chọn chuyển đổi linh hoạt các tầng bản đồ chuyên sâu
            sel_indicator = st.selectbox(
                "Hiển thị lớp chỉ số:", 
                ["Tổng hợp FVI", "Độ phơi nhiễm (Exposure)", "Độ nhạy cảm (Sensitivity)", "Năng lực thích ứng (Adaptive)"],
                key="map_ind"
            )
            
        # Áp dụng bộ lọc người dùng chọn vào DataFrame điểm trạm
        map_df = df.copy()
        if sel_sector != "Tất cả":
            map_df = map_df[map_df["TypeofOrg"] == sel_sector]
        if sel_vul != "Tất cả":
            map_df = map_df[map_df["Vulnerability"] == sel_vul]
        if sel_comm != "Tất cả":
            map_df = map_df[map_df["Commune"] == sel_comm]

        st.markdown("<div class='sub-section-title'>Bản đồ số tích hợp ranh giới xã/phường và phân lớp chỉ số ô nhiễm/rủi ro</div>", unsafe_allow_html=True)

        # Khởi tạo đối tượng đồ họa bản đồ go.Figure đa tầng
        fig_complex = go.Figure()

        # --- TẦNG KHÔNG GIAN 1: RANH GIỚI PHÂN VÙNG PHƯỜNG HÀNH CHÍNH (GEOJSON) ---
        geojson_path = "data/AOI_Hue.geojson"
        if os.path.exists(geojson_path):
            try:
                with open(geojson_path, "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)
                
                # Ánh xạ thuộc tính 'id' trùng khớp với tên xã trơn trong GeoJSON để định vị
                for feature in geojson_data['features']:
                    feature['id'] = feature['properties']['tenXa_shor']
                
                commune_names = [f['properties']['tenXa_shor'] for f in geojson_data['features']]
                
                # Vẽ lớp vùng phủ màu có ranh giới phân xã lên bản đồ nền
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

        # --- TẦNG KHÔNG GIAN 2: ĐIỂM TRẠM CƠ SỞ HẠ TẦNG THEO TỪNG LỚP CHỈ SỐ LỰA CHỌN ---
        color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
        
        # Chuẩn hóa chuỗi văn bản Popup Hover bằng tiếng Việt thuần túy
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

        # Phân nhánh logic dựng điểm Marker dựa vào nhu cầu xem bản đồ
        if sel_indicator == "Tổng hợp FVI":
            # Hiển thị dạng phân loại màu định tính (Theo đúng thứ tự Đỏ - Cam - Vàng - Xanh)
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
            # Hiển thị dải màu gradient liên tục cho từng lớp cấu phần chuyên sâu
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
                    size=14,
                    color=map_df[target_col],
                    colorscale=target_scale,
                    showscale=True,
                    opacity=0.95,
                    colorbar=dict(
                        title=dict(text=colorbar_title, font=dict(size=12)),
                        thickness=18,
                        x=0.96,
                        len=0.7
                    )
                ),
                text=hover_texts,
                hoverinfo='text',
                name=sel_indicator
            ))

        # Thiết lập nền bản đồ có màu Open Street Map
        fig_complex.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=df["CoordY"].mean() if not df.empty else 16.46, lon=df["CoordX"].mean() if not df.empty else 107.60),
                zoom=12.0
            ),
            margin={"r":0, "t":15, "l":0, "b":0},
            height=540,
            font_family="Roboto",
            legend=dict(
                title="Bảng chú giải rủi ro",
                yanchor="top", y=0.98,
                xanchor="left", x=0.02,
                bgcolor="rgba(255, 255, 255, 0.85)"
            )
        )
        st.plotly_chart(fig_complex, use_container_width=True)
        
        # --- KHU VỰC THỐNG KÊ KPI ĐỔI MÀU ĐỘNG ---
        st.markdown("<div class='sub-section-title'>Chỉ số tổng hợp theo phạm vi lựa chọn</div>", unsafe_allow_html=True)
        st.markdown("""
            <style>
                .kpi-container { display: flex; gap: 12px; margin-bottom: 25px; }
                .kpi-box { flex: 1; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
                .kpi-title { font-size: 13px; font-weight: 500; margin-bottom: 4px; }
                .kpi-value { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
                .kpi-subtitle { font-size: 11px; opacity: 0.8; }
            </style>
        """, unsafe_allow_html=True)
        
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

        # --- BIỂU ĐỒ DONUT (ĐÃ SẮP XẾP ĐÚNG THỨ TỰ THIÊN TAI VÀ TRẢI RỘNG TOÀN CHIỀU RỘNG) ---
        st.markdown("<div class='sub-section-title'>Tỷ lệ phân loại các mức độ tổn thương thực tế</div>", unsafe_allow_html=True)
        
        # Đếm số lượng của tập dữ liệu đã lọc để vẽ biểu đồ hình bánh
        pie_counts = map_df["Vulnerability"].value_counts()
        
        # ĐỊNH HƯỚNG THỨ TỰ CỐ ĐỊNH: Đảm bảo thứ tự hiển thị luôn tuân thủ mạch logic khoa học
        ordered_levels = [lvl for val in ["Cao", "Tương đối cao", "Trung bình", "Thấp"] if (lvl := val) in pie_counts.index]
        ordered_values = [pie_counts[lvl] for lvl in ordered_levels]
        ordered_colors = [color_map_scheme[lvl] for lvl in ordered_levels]

        fig_pie = go.Figure(data=[go.Pie(
            labels=ordered_levels,
            values=ordered_values,
            hole=0.45,
            marker=dict(colors=ordered_colors, line=dict(color='#ffffff', width=2)),
            textinfo='label+percent',
            sort=False # Vô hiệu hóa tính năng tự động sắp xếp lớn bé của Plotly để ép theo thứ tự mảng tự định nghĩa
        )])
        
        fig_pie.update_layout(
            font_family="Roboto",
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================================
    # TẦNG HIỂN THỊ 1: BẢN ĐỒ TƯƠNG TÁC ĐA LỚP & KPI ĐỔI MÀU ĐỘNG
    # ==========================================================
    with tab_map:
        # Bộ lọc nâng cao chia thành 4 cột song song gọn gàng
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            sel_sector = st.selectbox("Lĩnh vực hạ tầng:", ["Tất cả", "Y tế", "Giáo dục"], key="map_sec")
        with col_f2:
            sel_vul = st.selectbox("Mức độ tổn thương:", ["Tất cả", "Cao", "Tương đối cao", "Trung bình", "Thấp"], key="map_vul")
        with col_f3:
            sel_comm = st.selectbox("Phường nghiên cứu:", ["Tất cả", "Thuận Hòa", "Phú Xuân", "Vỹ Dạ", "Mỹ Thượng", "Dương Nỗ"], key="map_comm")
        with col_f4:
            # Hộp chọn chuyển đổi linh hoạt các tầng bản đồ chuyên sâu
            sel_indicator = st.selectbox(
                "Hiển thị lớp chỉ số:", 
                ["Tổng hợp FVI", "Độ phơi nhiễm (Exposure)", "Độ nhạy cảm (Sensitivity)", "Năng lực thích ứng (Adaptive)"],
                key="map_ind"
            )
            
        # Áp dụng bộ lọc người dùng chọn vào DataFrame điểm trạm
        map_df = df.copy()
        if sel_sector != "Tất cả":
            map_df = map_df[map_df["TypeofOrg"] == sel_sector]
        if sel_vul != "Tất cả":
            map_df = map_df[map_df["Vulnerability"] == sel_vul]
        if sel_comm != "Tất cả":
            map_df = map_df[map_df["Commune"] == sel_comm]

        st.markdown("<div class='sub-section-title'>Bản đồ số tích hợp ranh giới xã/phường và phân lớp chỉ số ô nhiễm/rủi ro</div>", unsafe_allow_html=True)

        # Khởi tạo đối tượng đồ họa bản đồ go.Figure đa tầng
        fig_complex = go.Figure()

        # --- TẦNG KHÔNG GIAN 1: RANH GIỚI PHÂN VÙNG PHƯỜNG HÀNH CHÍNH (GEOJSON) ---
        geojson_path = "data/AOI_Hue.geojson"
        if os.path.exists(geojson_path):
            try:
                with open(geojson_path, "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)
                
                # Ánh xạ thuộc tính 'id' trùng khớp với tên xã trơn trong GeoJSON để định vị
                for feature in geojson_data['features']:
                    feature['id'] = feature['properties']['tenXa_shor']
                
                commune_names = [f['properties']['tenXa_shor'] for f in geojson_data['features']]
                
                # Vẽ lớp vùng phủ màu có ranh giới phân xã lên bản đồ nền
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

        # --- TẦNG KHÔNG GIAN 2: ĐIỂM TRẠM CƠ SỞ HẠ TẦNG THEO TỪNG LỚP CHỈ SỐ LỰA CHỌN ---
        color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
        
        # Chuẩn hóa chuỗi văn bản Popup Hover bằng tiếng Việt thuần túy
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

        # Phân nhánh logic dựng điểm Marker dựa vào nhu cầu xem bản đồ
        if sel_indicator == "Tổng hợp FVI":
            # Hiển thị dạng phân loại màu định tính (Theo đúng thứ tự Đỏ - Cam - Vàng - Xanh)
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
            # Hiển thị dải màu gradient liên tục cho từng lớp cấu phần chuyên sâu
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
                    size=14,
                    color=map_df[target_col],
                    colorscale=target_scale,
                    showscale=True,
                    opacity=0.95,
                    colorbar=dict(
                        title=dict(text=colorbar_title, font=dict(size=12)),
                        thickness=18,
                        x=0.96,
                        len=0.7
                    )
                ),
                text=hover_texts,
                hoverinfo='text',
                name=sel_indicator
            ))

        # Thiết lập nền bản đồ có màu Open Street Map
        fig_complex.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=df["CoordY"].mean() if not df.empty else 16.46, lon=df["CoordX"].mean() if not df.empty else 107.60),
                zoom=12.0
            ),
            margin={"r":0, "t":15, "l":0, "b":0},
            height=540,
            font_family="Roboto",
            legend=dict(
                title="Bảng chú giải rủi ro",
                yanchor="top", y=0.98,
                xanchor="left", x=0.02,
                bgcolor="rgba(255, 255, 255, 0.85)"
            )
        )
        st.plotly_chart(fig_complex, use_container_width=True)
        
        # --- KHU VỰC THỐNG KÊ KPI ĐỔI MÀU ĐỘNG ---
        st.markdown("<div class='sub-section-title'>Chỉ số tổng hợp theo phạm vi lựa chọn</div>", unsafe_allow_html=True)
        st.markdown("""
            <style>
                .kpi-container { display: flex; gap: 12px; margin-bottom: 25px; }
                .kpi-box { flex: 1; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
                .kpi-title { font-size: 13px; font-weight: 500; margin-bottom: 4px; }
                .kpi-value { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
                .kpi-subtitle { font-size: 11px; opacity: 0.8; }
            </style>
        """, unsafe_allow_html=True)
        
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

        # --- BIỂU ĐỒ DONUT (ĐÃ SẮP XẾP ĐÚNG THỨ TỰ THIÊN TAI VÀ TRẢI RỘNG TOÀN CHIỀU RỘNG) ---
        st.markdown("<div class='sub-section-title'>Tỷ lệ phân loại các mức độ tổn thương thực tế</div>", unsafe_allow_html=True)
        
        # Đếm số lượng của tập dữ liệu đã lọc để vẽ biểu đồ hình bánh
        pie_counts = map_df["Vulnerability"].value_counts()
        
        # ĐỊNH HƯỚNG THỨ TỰ CỐ ĐỊNH: Đảm bảo thứ tự hiển thị luôn tuân thủ mạch logic khoa học
        ordered_levels = [lvl for val in ["Cao", "Tương đối cao", "Trung bình", "Thấp"] if (lvl := val) in pie_counts.index]
        ordered_values = [pie_counts[lvl] for lvl in ordered_levels]
        ordered_colors = [color_map_scheme[lvl] for lvl in ordered_levels]

        fig_pie = go.Figure(data=[go.Pie(
            labels=ordered_levels,
            values=ordered_values,
            hole=0.45,
            marker=dict(colors=ordered_colors, line=dict(color='#ffffff', width=2)),
            textinfo='label+percent',
            sort=False # Vô hiệu hóa tính năng tự động sắp xếp lớn bé của Plotly để ép theo thứ tự mảng tự định nghĩa
        )])
        
        fig_pie.update_layout(
            font_family="Roboto",
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ==========================================================
    # TẦNG HIỂN THỊ 3: TRA CỨU CHI TIẾT TỪNG CƠ SỞ (TAB DETAIL) - GIỮ NGUYÊN
    # ==========================================================
    with tab_detail_facility:
        st.markdown('<div class="sub-section-title">Tra cứu chi tiết từng cơ sở hạ tầng thiết yếu</div>', unsafe_allow_html=True)
        sel_facility = st.selectbox("Chọn tên cơ sở cần tra cứu rủi ro:", df["Name"].unique())
        
        row_facility = df[df["Name"] == sel_facility].iloc[0]
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
            fig_bar_compare.update_layout(barmode='group', title=f"So sánh các cấu phần FVI của {sel_facility}", font_family="Roboto")
            st.plotly_chart(fig_bar_compare, use_container_width=True)
            
        st.markdown('<div class="sub-section-title">Đánh giá chuyên sâu và Nhận xét tự động</div>', unsafe_allow_html=True)
        if row_facility['Vulnerability'] == "Cao":
            st.error(f"CẢNH BÁO NGUY CƠ CAO: Cơ sở {row_facility['Name']} có mức độ tổn thương ngập lụt đô thị rất cao (FVI = {row_facility['FVI']:.2f}). Đề nghị chính quyền địa phương đưa cơ sở này vào danh sách ưu tiên ngân sách nâng nền cấu trúc công trình chính, cải thiện hệ thống bơm thoát nước lân cận trước mùa lũ năm nay.")
        elif row_facility['Vulnerability'] == "Tương đối cao":
            st.warning(f"KHUYẾN NGHỊ: Cơ sở {row_facility['Name']} có chỉ số rủi ro ngập lụt tương đối cao (FVI = {row_facility['FVI']:.2f}). Đơn vị quản lý cần xây dựng ngay phương án di dời kho lưu trữ thiết bị, thuốc men lên tầng hai và lập kế hoạch phối hợp với lực lượng cứu hộ địa phương khi có cảnh báo lũ.")
        else:
            st.success(f"AN TOÀN: Cơ sở {row_facility['Name']} có mức độ tổn thương thiên tai thấp hoặc trung bình, kết cấu hạ tầng có năng lực tự chống chịu cơ bản tốt. Cần tiếp tục duy trì trạng thái hoạt động bảo trì định kỳ.")
