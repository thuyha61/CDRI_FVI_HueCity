import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import inject_custom_css, load_project_data

inject_custom_css()
df = load_project_data()

st.markdown('<div class="section-title">Bản đồ tính dễ bị tổn thương do lũ lụt</div>', unsafe_allow_html=True)

if df.empty:
    st.warning("Dữ liệu trống, không thể hiển thị kết quả phân tích.")
else:
    tab_map, tab_descriptive, tab_detail_facility = st.tabs([
        "BẢN ĐỒ TƯƠNG TÁC & TỔNG QUAN KẾT QUẢ",
        "THỐNG KÊ DỮ LIỆU ĐẦU VÀO",
        "TRA CỨU CHI TIẾT TỪNG CƠ SỞ"
    ])
    
    with tab_map:
        # Khu vực lọc dữ liệu
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sel_sector = st.selectbox("Lĩnh vực:", ["Tất cả", "Y tế", "Giáo dục"])
        with col_f2:
            sel_vul = st.selectbox("Mức độ tổn thương:", ["Tất cả", "Cao", "Tương đối cao", "Trung bình", "Thấp"])
        with col_f3:
            sel_comm = st.selectbox("Phường nghiên cứu:", ["Tất cả", "Thuận Hòa", "Phú Xuân", "Vỹ Dạ", "Mỹ Thượng", "Dương Nỗ"])
            
        # Áp dụng các bộ lọc dữ liệu
        map_df = df.copy()
        if sel_sector != "Tất cả":
            map_df = map_df[map_df["TypeofOrg"] == sel_sector]
        if sel_vul != "Tất cả":
            map_df = map_df[map_df["Vulnerability"] == sel_vul]
        if sel_comm != "Tất cả":
            map_df = map_df[map_df["Commune"] == sel_comm]
            
        # Vẽ bản đồ bằng Plotly Mapbox
        st.markdown("<div class='sub-section-title'>Vị trí không gian các cơ sở hạ tầng thiết yếu</div>", unsafe_allow_html=True)
        color_map_scheme = {"Cao": "#ef4444", "Tương đối cao": "#f97316", "Trung bình": "#eab308", "Thấp": "#22c55e"}
        
        fig_mapbox = px.scatter_mapbox(
            map_df,
            lat="CoordY",
            lon="CoordX",
            color="Vulnerability",
            color_discrete_map=color_map_scheme,
            hover_name="Name",
            hover_data={"FVI": ":.2f", "Exposure": ":.2f", "Sensitivity": ":.2f", "Adaptive": ":.2f", "Address": True},
            zoom=12.2,
            height=480,
            mapbox_style="carto-positron"
        )
        fig_mapbox.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, font_family="Roboto")
        st.plotly_chart(fig_mapbox, use_container_width=True)
        
        # Thống kê nhanh dạng KPI Cards
        st.markdown("<div class='sub-section-title'>Chỉ số tổng hợp toàn khu vực nghiên cứu</div>", unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
        col_kpi1.metric("Cơ sở đánh giá", len(df), "Trường học + Y tế")
        col_kpi2.metric("Mức CAO", len(df[df["Vulnerability"] == "Cao"]), "Cần ưu tiên gấp")
        col_kpi3.metric("Mức TƯƠNG ĐỐI CAO", len(df[df["Vulnerability"] == "Tương đối cao"]), "Kế hoạch ngắn hạn")
        col_kpi4.metric("Mức TRUNG BÌNH", len(df[df["Vulnerability"] == "Trung bình"]), "Theo dõi định kỳ")
        col_kpi5.metric("Mức THẤP", len(df[df["Vulnerability"] == "Thấp"]), "An toàn tốt")
        
        # Biểu đồ phân phối
        col_hist1, col_hist2 = st.columns(2)
        with col_hist1:
            st.markdown("<div class='sub-section-title'>Histogram phân bố điểm Chỉ số FVI</div>", unsafe_allow_html=True)
            fig_hist = px.histogram(
                df,
                x="FVI",
                color="TypeofOrg",
                nbins=12,
                labels={"FVI": "Điểm FVI", "count": "Tần suất"},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_hist.update_layout(font_family="Roboto", legend_title="Ngành")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_hist2:
            st.markdown("<div class='sub-section-title'>Tỷ lệ phân loại các mức độ tổn thương</div>", unsafe_allow_html=True)
            fig_pie = px.pie(
                df,
                names="Vulnerability",
                color="Vulnerability",
                color_discrete_map=color_map_scheme,
                hole=0.4
            )
            fig_pie.update_layout(font_family="Roboto")
            st.plotly_chart(fig_pie, use_container_width=True)

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
            "FVI": "{:.2f}",
            "Exposure": "{:.2f}",
            "Sensitivity": "{:.2f}",
            "Adaptive": "{:.2f}",
            "HeightFromTheRoad": "{:.1f}"
        }), use_container_width=True)
        
        st.markdown('<div class="sub-section-title">Thống kê tóm tắt các tham số phân phối</div>', unsafe_allow_html=True)
        summary_table = data_table[["FVI", "Exposure", "Sensitivity", "Adaptive", "HeightFromTheRoad"]].describe().T
        st.table(summary_table[["min", "max", "mean", "std"]])

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
            # So sánh điểm của cơ sở với trung bình toàn đô thị
            m_exposure = df["Exposure"].mean()
            m_sensitivity = df["Sensitivity"].mean()
            m_adaptive = df["Adaptive"].mean()
            
            headers = ['Phơi nhiễm (Exposure)', 'Nhạy cảm (Sensitivity)', 'Thích ứng (Adaptive)']
            
            fig_bar_compare = go.Figure()
            fig_bar_compare.add_trace(go.Bar(
                name='Cơ sở được chọn',
                x=headers,
                y=[row_facility['Exposure'], row_facility['Sensitivity'], row_facility['Adaptive']],
                marker_color='#3b82f6'
            ))
            fig_bar_compare.add_trace(go.Bar(
                name='Trung bình toàn đô thị',
                x=headers,
                y=[m_exposure, m_sensitivity, m_adaptive],
                marker_color='#94a3b8'
            ))
            
            fig_bar_compare.update_layout(
                barmode='group',
                title=f"So sánh các cấu phần FVI của {sel_facility}",
                font_family="Roboto"
            )
            st.plotly_chart(fig_bar_compare, use_container_width=True)
            
        # Đưa ra nhận xét tự động
        st.markdown('<div class="sub-section-title">Đánh giá chuyên sâu và Nhận xét tự động</div>', unsafe_allow_html=True)
        if row_facility['Vulnerability'] == "Cao":
            st.error(f"CẢNH BÁO NGUY CƠ CAO: Cơ sở {row_facility['Name']} có mức độ tổn thương ngập lụt đô thị rất cao (FVI = {row_facility['FVI']:.2f}). Đề nghị chính quyền địa phương đưa cơ sở này vào danh sách ưu tiên ngân sách nâng nền cấu trúc công trình chính, cải thiện hệ thống bơm thoát nước lân cận trước mùa lũ năm nay.")
        elif row_facility['Vulnerability'] == "Tương đối cao":
            st.warning(f"KHUYẾN NGHỊ: Cơ sở {row_facility['Name']} có chỉ số rủi ro ngập lụt tương đối cao (FVI = {row_facility['FVI']:.2f}). Đơn vị quản lý cần xây dựng ngay phương án di dời kho lưu trữ thiết bị, thuốc men lên tầng hai và lập kế hoạch phối hợp với lực lượng cứu hộ địa phương khi có cảnh báo lũ.")
        else:
            st.success(f"AN TOÀN: Cơ sở {row_facility['Name']} có mức độ tổn thương thiên tai thấp hoặc trung bình, kết cấu hạ tầng có năng lực tự chống chịu cơ bản tốt. Cần tiếp tục duy trì trạng thái hoạt động bảo trì định kỳ.")
