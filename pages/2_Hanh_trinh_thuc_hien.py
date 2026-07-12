import streamlit as st
import plotly.express as px
from utils import inject_custom_css, load_project_data

inject_custom_css()
df = load_project_data()

st.markdown('<div class="section-title">Lộ trình triển khai dự án</div>', unsafe_allow_html=True)

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
