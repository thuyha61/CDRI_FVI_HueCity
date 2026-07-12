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
    # TẦNG HIỂN THỊ 1: BẢN ĐỒ TƯƠNG TÁC ĐA LỚP (ĐÃ CẬP NHẬT CHUẨN GEOJSON)
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
                
                # Khắc phục thuật toán Plotly: Bắt buộc nhúng thuộc tính 'id' trùng khớp với tên xã trơn để ánh xạ bản đồ màu
                for feature in geojson_data['features']:
                    feature['id'] = feature['properties']['tenXa_shor']
                
                # Tạo danh sách các xã và gán giá trị z giả lập để giữ màu nền mờ ổn định
                commune_names = [f['properties']['tenXa_shor'] for f in geojson_data['features']]
                
                # Vẽ lớp vùng phủ màu có ranh giới phân xã lên bản đồ nền
                fig_complex.add_trace(go.Choroplethmapbox(
                    geojson=geojson_data,
                    locations=commune_names,
                    z=[1] * len(commune_names),
                    colorscale=[[0, 'rgba(69, 123, 157, 0.15)'], [1, 'rgba(69, 123, 157, 0.15)']], # Màu nền xanh ngọc mờ đồng nhất
                    showscale=False,
                    marker_line_color="#1d3557",  # Đường ranh giới xã màu xanh đậm sắc nét
                    marker_line_width=2.0,        # Độ dày nét vẽ ranh giới hành chính
                    name="Lớp ranh giới hành chính",
                    customdata=commune_names,
                    hovertemplate="<b>Phường/Xã: %{customdata}</b><extra></customdata></extra>" # Hiển thị tên xã đời thường khi rê chuột vào vùng trống
                ))
            except Exception as e:
                st.error(f"Lỗi hệ thống khi xử lý ánh xạ dữ liệu AOI_Hue.geojson: {e}")
        else:
            st.warning("Không tìm thấy tệp không gian data/AOI_Hue.geojson trong cấu trúc thư mục.")

        # --- TẦNG KHÔNG GIAN 2: ĐIỂM TRẠM CƠ SỞ HẠ TẦNG THEO TỪNG LỚP CHỈ SỐ LỰA CHỌN ---
        color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
        
        # Chuẩn hóa chuỗi văn bản Popup Hover bằng tiếng Việt thuần túy, loại bỏ hoàn toàn tên biến gốc
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

        # Phân nhánh logic dựng điểm Marker dựa vào nhu cầu xem bản đồ của chị Hà
        if sel_indicator == "Tổng hợp FVI":
            # Hiển thị dạng phân loại màu định tính (4 màu tương ứng 4 cấp độ tổn thương rủi ro)
            for val_level, color_hex in color_map_scheme.items():
                level_df = map_df[map_df["Vulnerability"] == val_level]
                level_texts = [hover_texts[i] for i, r in enumerate(map_df.index) if map_df.loc[r, "Vulnerability"] == val_level]
                
                fig_complex.add_trace(go.Scattermapbox(
                    lat=level_df["CoordY"],
                    lon=level_df["CoordX"],
                    mode='markers',
                    marker=dict(size=13, color=color_hex, opacity=0.95),
                    text=level_texts,
                    hoverinfo='text',
                    name=f"Cấp rủi ro: {val_level}"
                ))
        else:
            # Hiển thị dải màu gradient liên tục khoa học cho từng lớp cấu phần chuyên sâu
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

        # 5. Cấu hình hệ thống tọa độ trung tâm đô thị Huế và kiểu nền có màu sinh động
        fig_complex.update_layout(
            mapbox=dict(
                style="open-street-map", # Giữ bản đồ nền có màu sắc địa vật rõ nét
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
        
        # Thống kê nhanh dạng KPI Cards bên dưới bản đồ
        st.markdown("<div class='sub-section-title'>Chỉ số tổng hợp toàn khu vực nghiên cứu</div>", unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
        col_kpi1.metric("Cơ sở đánh giá", len(df), "Trường học + Y tế")
        col_kpi2.metric("Mức CAO", len(df[df["Vulnerability"] == "Cao"]), "Cần ưu tiên gấp")
        col_kpi3.metric("Mức TƯƠNG ĐỐI CAO", len(df[df["Vulnerability"] == "Tương đối cao"]), "Kế hoạch ngắn hạn")
        col_kpi4.metric("Mức TRUNG BÌNH", len(df[df["Vulnerability"] == "Trung bình"]), "Theo dõi định kỳ")
        col_kpi5.metric("Mức THẤP", len(df[df["Vulnerability"] == "Thấp"]), "An toàn tốt")
        
        # Biểu đồ phân phối Histogram và Pie Chart phụ trợ giữ nguyên
        col_hist1, col_hist2 = st.columns(2)
        with col_hist1:
            st.markdown("<div class='sub-section-title'>Histogram phân bố điểm Chỉ số FVI</div>", unsafe_allow_html=True)
            fig_hist = px.histogram(
                df, x="FVI", color="TypeofOrg", nbins=12,
                labels={"FVI": "Điểm FVI", "count": "Tần suất"},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_hist.update_layout(font_family="Roboto", legend_title="Ngành")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_hist2:
            st.markdown("<div class='sub-section-title'>Tỷ lệ phân loại các mức độ tổn thương</div>", unsafe_allow_html=True)
            fig_pie = px.pie(df, names="Vulnerability", color="Vulnerability", color_discrete_map=color_map_scheme, hole=0.4)
            fig_pie.update_layout(font_family="Roboto")
            st.plotly_chart(fig_pie, use_container_width=True)

    # ==========================================================
    # TẦNG HIỂN THỊ 2: THỐNG KÊ MÔ TẢ (TAB DESCRIPTIVE) - GIỮ NGUYÊN
    # ==========================================================
    with tab_descriptive:
        st.markdown('<div class="sub-section-title">Thống kê mô tả dữ liệu đầu vào của các chỉ số</div>', unsafe_allow_html=True)
        col_desc1, col_desc2 = st.columns(2)
        with col_desc1:
            filter_sector = st.selectbox("Lọc lĩnh vực thống kê:", ["Tất cả", "Y tế", "Giáo dục"], key="tab2_s")
        with col_desc2:
            filter_indicator = st.selectbox("Nhóm cấu phần chỉ số:", ["Tất cả", "Exposure", "Sensitivity", "Adaptive"], key="tab2_i")
            
        data_table = df.copy()
        if filter_sector != "Tất cả":
            data_table = data_table[data_table["TypeofOrg"] == filter_sector]
            
        cols_display = ["Name", "Commune", "TypeofOrg", "FVI", "Exposure", "Sensitivity", "Adaptive", "HeightFromTheRoad", "NoOfStaff", "NoOfClients"]
        st.dataframe(data_table[cols_display].style.format({
            "FVI": "{:.2f}", "Exposure": "{:.2f}", "Sensitivity": "{:.2f}", "Adaptive": "{:.2f}", "HeightFromTheRoad": "{:.1f}"
        }), use_container_width=True)
        
        st.markdown('<div class="sub-section-title">Thống kê tóm tắt các tham số phân phối</div>', unsafe_allow_html=True)
        summary_table = data_table[["FVI", "Exposure", "Sensitivity", "Adaptive", "HeightFromTheRoad"]].describe().T
        st.table(summary_table[["min", "max", "mean", "std"]])

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
