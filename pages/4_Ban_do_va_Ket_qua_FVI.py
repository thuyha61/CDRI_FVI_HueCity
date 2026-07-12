import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

# --- Mở rộng phân khu code trong Tab 1 (tab_map) ---
with tab_map:
    # 1. Bổ sung Khu vực bộ lọc nâng cao
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        sel_sector = st.selectbox("Lĩnh vực:", ["Tất cả", "Y tế", "Giáo dục"], key="map_sec")
    with col_f2:
        sel_vul = st.selectbox("Mức độ tổn thương:", ["Tất cả", "Cao", "Tương đối cao", "Trung bình", "Thấp"], key="map_vul")
    with col_f3:
        sel_comm = st.selectbox("Phường nghiên cứu:", ["Tất cả", "Thuận Hòa", "Phú Xuân", "Vỹ Dạ", "Mỹ Thượng", "Dương Nỗ"], key="map_comm")
    with col_f4:
        # Hộp chọn tính năng: Cho phép người dùng chọn bản đồ hiển thị cấu phần FVI hoặc các chỉ số thành phần
        sel_indicator = st.selectbox(
            "Hiển thị lớp chỉ số:", 
            ["Tổng hợp FVI", "Độ phơi nhiễm (Exposure)", "Độ nhạy cảm (Sensitivity)", "Năng lực thích ứng (Adaptive)"],
            key="map_ind"
        )
        
    # Áp dụng bộ lọc vào DataFrame
    map_df = df.copy()
    if sel_sector != "Tất cả":
        map_df = map_df[map_df["TypeofOrg"] == sel_sector]
    if sel_vul != "Tất cả":
        map_df = map_df[map_df["Vulnerability"] == sel_vul]
    if sel_comm != "Tất cả":
        map_df = map_df[map_df["Commune"] == sel_comm]

    st.markdown("<div class='sub-section-title'>Bản đồ không gian tích hợp ranh giới nghiên cứu và các lớp chỉ số</div>", unsafe_allow_html=True)

    # 2. Khởi tạo đối tượng đồ họa bản đồ dạng nhiều lớp (Multi-layer go.Figure)
    fig_complex = go.Figure()

    # Lớp 1: Đọc và hiển thị vùng ranh giới nghiên cứu (AOI_Hue.geojson)
    geojson_path = "AOI_Hue.geojson"
    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            
            # Đưa ranh giới GeoJSON vào bản đồ dưới dạng lớp đa giác (Choropleth/Polygon Line)
            fig_complex.add_trace(go.Choroplethmapbox(
                geojson=geojson_data,
                locations=[0] * len(geojson_data['features']), # Định danh ánh xạ giả định
                z=[1] * len(geojson_data['features']),
                colorscale=[[0, 'rgba(69, 123, 157, 0.15)'], [1, 'rgba(69, 123, 157, 0.15)']], # Phủ màu xanh mờ trong lòng
                showscale=False,
                marker_line_color="#1d3557", # Đường viền ranh giới màu xanh đậm
                marker_line_width=2.5,       # Độ dày đường ranh giới vùng
                name="Ranh giới khu vực nghiên cứu (AOI)",
                hoverinfo="skip"             # Ẩn thông tin hover của nền vùng, tránh nhiễu điểm trạm
            ))
        except Exception as e:
            st.error(f"Lỗi cấu trúc khi đọc file AOI_Hue.geojson: {e}")
    else:
        st.warning("Không tìm thấy tệp không gian AOI_Hue.geojson trong thư mục gốc. Hệ thống chỉ hiển thị vị trí điểm cơ sở hạ tầng.")

    # 3. Xác định phân bố màu sắc và biến số mục tiêu dựa trên Selectbox lựa chọn của người dùng
    color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
    
    # Chuẩn bị văn bản chú thích linh hoạt hiển thị trong cửa sổ tương tác (Popup Hover)
    hover_texts = []
    for idx, row in map_df.iterrows():
        text_block = (
            f"<b>{row['Name']}</b><br>"
            f"📍 Địa chỉ: {row['Address']}<br>"
            f"🏢 Lĩnh vực: {row['TypeofOrg']} | Phường: {row['Commune']}<br>"
            f"⚠️ Mức độ tổn thương FVI: <b>{row['Vulnerability']}</b><br>"
            f"📊 Điểm FVI tổng hợp: {row['FVI']:.2f}<br>"
            f"🔍 Độ phơi nhiễm (Exposure): {row['Exposure']:.2f}<br>"
            f"📉 Độ nhạy cảm (Sensitivity): {row['Sensitivity']:.2f}<br>"
            f"🛡️ Năng lực thích ứng (Adaptive): {row['Adaptive']:.2f}"
        )
        hover_texts.append(text_block)

    # Khởi tạo định trị kích cỡ và thang màu động cho cấu phần chỉ số chuyên sâu
    if sel_indicator == "Tổng hợp FVI":
        # Bản đồ phân loại màu định tính theo 4 cấp bậc Tổn thương (Cao/Trung bình/Thấp)
        for val_level, color_hex in color_map_scheme.items():
            level_df = map_df[map_df["Vulnerability"] == val_level]
            level_texts = [hover_texts[i] for i, r in enumerate(map_df.index) if map_df.loc[r, "Vulnerability"] == val_level]
            
            fig_complex.add_trace(go.Scattermapbox(
                lat=level_df["CoordY"],
                lon=level_df["CoordX"],
                mode='markers',
                marker=dict(size=13, color=color_hex, opacity=0.9),
                text=level_texts,
                hoverinfo='text',
                name=f"Tổn thương: {val_level}"
            ))
    else:
        # Bản đồ hiển thị dải liên tục cho 3 chỉ số chuyên sâu (Exposure, Sensitivity, Adaptive)
        indicator_mapping = {
            "Độ phơi nhiễm (Exposure)": ("Exposure", px.colors.sequential.OrRd),    # Màu cam đỏ tăng dần
            "Độ nhạy cảm (Sensitivity)": ("Sensitivity", px.colors.sequential.Purples), # Màu tím nhạy cảm
            "Năng lực thích ứng (Adaptive)": ("Adaptive", px.colors.sequential.YlGn)    # Màu xanh lá thích ứng
        }
        target_col, target_scale = indicator_mapping[sel_indicator]
        
        fig_complex.add_trace(go.Scattermapbox(
            lat=map_df["CoordY"],
            lon=map_df["CoordX"],
            mode='markers',
            marker=dict(
                size=14,
                color=map_df[target_col],
                colorscale=target_scale,
                showscale=True,
                colorbar=dict(
                    title=dict(text=sel_indicator, font=dict(size=12)),
                    thickness=15,
                    x=0.95
                )
            ),
            text=hover_texts,
            hoverinfo='text',
            name=sel_indicator
        ))

    # 4. Thiết lập cấu hình Layout nền bản đồ có màu Open Street Map
    fig_complex.update_layout(
        mapbox=dict(
            style="open-street-map", # Giao diện bản đồ nền có màu sắc phân vùng rõ nét
            center=dict(lat=df["CoordY"].mean(), lon=df["CoordX"].mean()),
            zoom=12.2
        ),
        margin={"r":0, "t":10, "l":0, "b":0},
        height=550,
        font_family="Roboto",
        legend=dict(
            title="Phân loại rủi ro chính",
            yanchor="top", y=0.98,
            xanchor="left", x=0.02,
            bgcolor="rgba(255, 255, 255, 0.85)"
        )
    )

    # Đẩy bản đồ tích hợp lên Streamlit
    st.plotly_chart(fig_complex, use_container_width=True)
