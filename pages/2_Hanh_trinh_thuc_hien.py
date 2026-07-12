import streamlit as st
import plotly.express as px
from utils import inject_custom_css, load_project_data

inject_custom_css()
df = load_project_data()

st.markdown('<div class="section-title">Hành trình thực hiện dự án</div>', unsafe_allow_html=True)

# Lộ trình triển khai Project Timeline
st.markdown('<div class="sub-section-title">Lộ trình triển khai dự án (Project Timeline)</div>', unsafe_allow_html=True)

with st.status("Tháng 08/2025 | Khởi động dự án (Kick-off)", expanded=False, state="complete"):
    st.write("Thống nhất mục tiêu, phạm vi và kế hoạch triển khai nghiên cứu. Nhóm thực hiện rà soát các tiêu chí kỹ thuật của CDRI Fellowship, hoàn thiện đề cương, xác định 5 phường trung tâm TP. Huế và lập danh mục 31 cơ sở y tế - giáo dục trọng điểm.")
    
with st.status("Tháng 09–10/2025 | Chuẩn bị dữ liệu và Khảo sát thực địa lần 1", expanded=False, state="complete"):
    st.write("Tổng hợp bản đồ, tài liệu nền hiện có về mạng lưới sông ngòi, địa hình, giao thông và niên giám thống kê. Thiết lập bộ tham số cơ bản thiết lập ma trận bảng hỏi và biểu mẫu phỏng vấn sâu.")
    st.write("*Thực tế triển khai:* Đợt khảo sát thực địa đầu tiên diễn ra trong điều kiện thời tiết cực đoan khi Huế hứng chịu mưa lớn và ngập lụt diện rộng. Nhóm nghiên cứu đã linh hoạt điều chỉnh lộ trình di chuyển để đảm bảo an toàn, đồng thời kết hợp ghi nhận trực quan các điểm ngập sâu thực tế và các tuyến đường tiếp cận bị cô lập.")
    
with st.status("Tháng 11–12/2025 | Khảo sát bổ sung và Hoàn thiện dữ liệu cơ sở", expanded=False, state="complete"):
    st.write("Triển khai đợt khảo sát thứ hai nhằm thu thập bổ sung cho các đơn vị chưa hoàn thiện ở đợt một, chốt dữ liệu thực địa cho toàn bộ 31 cơ sở. Tiến hành đo đạc đặc điểm công trình, cao độ nền, kiểm tra nguồn lực ứng phó tại chỗ và hoàn thiện cơ sở dữ liệu thuộc tính không gian.")
    
with st.status("Tháng 10/2025 – 04/2026 | Tích hợp và Phân tích số liệu", expanded=False, state="complete"):
    st.write("Tiến hành làm sạch dữ liệu khảo sát, mã hóa các biến định tính và kiểm tra logic để xử lý triệt để các trường thông tin khuyết (NA). Đồng bộ dữ liệu thực địa với dữ liệu lưới trích xuất từ vệ tinh Sentinel-1 để chuẩn bị cho các bước tính toán cấu phần rủi ro tiếp theo.")
    
with st.status("Tháng 05 – 06/2026 | Rà soát và Tối ưu hóa hệ thống", expanded=False, state="complete"):
    st.write("Trình bày kết quả mô hình sơ bộ và tiến hành hiệu chỉnh, tối ưu hóa thuật toán phân cụm, rà soát chiều tác động của các biến số theo đóng góp chuyên môn từ các chuyên gia kỹ thuật và cố vấn của CDRI.")
    
with st.status("Tháng 07/2026 | Hội thảo tham vấn và Chia sẻ kết quả [Đang triển khai]", expanded=True, state="running"):
    st.write("Tổ chức hoạt động tham vấn trực tiếp tại Thừa Thiên Huế với sự tham gia của các cơ quan quản lý, chính quyền địa phương, đại diện ngành y tế, giáo dục nhằm đánh giá tính thực tiễn của hệ thống bản đồ số và nhu cầu sử dụng dữ liệu quy hoạch.")
    
with st.status("Tháng 07 – 08/2026 | Hoàn thiện và Bàn giao sản phẩm [Kế hoạch]", expanded=False, state="complete"):
    st.write("Hoàn thiện toàn văn báo cáo tổng hợp, hệ thống hóa bộ dữ liệu mở (.CSV) phục vụ khoa học minh bạch và hoàn thiện cổng thông tin điện tử website tương tác.")

# Nhật ký thực địa
st.markdown('<div class="section-title">Nhật ký thực địa và Ghi nhận từ hiện trường</div>', unsafe_allow_html=True)
col_note1, col_note2 = st.columns([3, 2])

with col_note1:
    st.markdown("""
        <div class="academic-paragraph">
            <b>Khối lượng công việc đã hoàn thành:</b> Nhóm nghiên cứu đã trực tiếp đo đạc tọa độ không gian và phỏng vấn sâu lãnh đạo đơn vị tại 31 cơ sở hạ tầng thiết yếu (bao gồm 22 trường học và 9 cơ sở y tế) phân bổ tại 5 phường trung tâm Thành phố Huế.
        </div>
        <div class="academic-paragraph">
            <b>Rủi ro do gián đoạn tiếp cận giao thông:</b> Khảo sát thực địa minh chứng tác động của lũ không chỉ xuất hiện khi nước tràn vào nền nhà. Nhiều cơ sở hạ tầng hoàn toàn khô ráo nhưng bắt buộc phải ngừng vận hành do 100% mạng lưới đường giao thông bao quanh bị cô lập sâu, khiến nhân lực, vật tư và lực lượng cứu hộ không thể tiếp cận.
        </div>
        <div class="academic-paragraph">
            <b>Điểm nghẽn năng lực chống chịu nội tại:</b> Ghi nhận sự chênh lệch lớn về mức độ chuẩn bị giữa các cơ sở. Nhiều công trình có cao độ nền rất thấp (thấp hơn mặt đường từ -10cm đến -50cm) nhưng lại khuyết thiếu nghiêm trọng các phương tiện cốt lõi (không có máy phát điện độc lập, thiếu máy bơm công suất lớn, thiếu kịch bản diễn tập thích ứng tại chỗ và hoàn toàn thiếu hạ tầng tiếp cận chuyên biệt hỗ trợ người khuyết tật).
        </div>
    """, unsafe_allow_html=True)
    
with col_note2:
    if not df.empty:
        st.markdown("<div class='sub-section-title'>Phân bổ độ cao nền so với lòng đường</div>", unsafe_allow_html=True)
        fig_height = px.bar(
            df.sort_values(by="HeightFromTheRoad"),
            x="Name",
            y="HeightFromTheRoad",
            color="TypeofOrg",
            labels={"HeightFromTheRoad": "Chênh lệch cao độ nền (m)", "Name": "Tên cơ sở"},
            title="Độ chênh cao nền công trình so với mặt đường thực tế"
        )
        fig_height.update_layout(xaxis_showticklabels=False, font_family="Roboto", legend_title="Ngành")
        st.plotly_chart(fig_height, use_container_width=True)
