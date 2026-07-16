       </style>
   """, unsafe_allow_html=True)

def pure_jenks_breaks(data_list, n_classes=4):
    """
    Thuật toán Jenks Natural Breaks viết bằng Python thuần, không dùng thư viện ngoài.
    Trả về danh sách các điểm phân lớp (breaks).
    """
    # Sắp xếp dữ liệu đầu vào
    data_list = sorted([x for x in data_list if not np.isnan(x)])
    n_data = len(data_list)
    
    if n_data <= n_classes:
        return [min(data_list)] + data_list + [max(data_list)] * (n_classes - n_data)

    # Khởi tạo ma trận rỗng
    mat1 = np.zeros((n_data + 1, n_classes + 1))
    mat2 = np.zeros((n_data + 1, n_classes + 1))
    
    for i in range(1, n_data + 1):
        mat1[i][1] = 1
        mat2[i][1] = 0
        
    for j in range(2, n_classes + 1):
        mat1[1][j] = 1
        mat2[1][j] = 0
        
    for i in range(2, n_data + 1):
        for j in range(2, n_classes + 1):
            mat1[i][j] = float('inf')
            mat2[i][j] = 0

    for l in range(2, n_data + 1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = data_list[i3 - 1]
            s1 += val
            s2 += val * val
            w += 1
            variance = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
                for j in range(2, n_classes + 1):
                    if mat1[l][j] >= (variance + mat1[i4][j - 1]):
                        mat1[l][j] = variance + mat1[i4][j - 1]
                        mat2[l][j] = i3

    # Lấy các điểm đứt gãy ngược từ ma trận
    k = n_data
    kclass = [0.0] * (n_classes + 1)
    kclass[n_classes] = data_list[n_data - 1]
    kclass[0] = data_list[0]
    
    countNum = n_classes
    while countNum >= 2:
        id_val = int(mat2[k][countNum]) - 1
        kclass[countNum - 1] = data_list[id_val]
        k = int(mat2[k][countNum]) - 1
        countNum -= 1
        
    return kclass

@st.cache_data
def load_project_data():
"""Đọc và chuẩn hóa dữ liệu từ thư mục data/"""
@@ -170,18 +232,35 @@ def load_project_data():
else:
df["Commune"] = "Khác"

    # Phân loại mức độ tổn thương theo điểm số FVI
    def classify_vulnerability(score):
        if score >= 0.70:
            return "Cao"
        elif score >= 0.50:
            return "Tương đối cao"
        elif score >= 0.00:
            return "Trung bình"
        else:
            return "Thấp"
    # --- PHẦN PHÂN CHIA THEO THUẬT TOÁN JENKS THUẦN (4 LỚP) ---
    fvi_values = df["FVI"].dropna().tolist()
    unique_fvi_count = len(set(fvi_values))
    
    labels = ["Thấp", "Trung bình", "Tương đối cao", "Cao"]
    num_classes = 4 # Cố định 4 nhóm như yêu cầu
    
    if unique_fvi_count >= num_classes:
        try:
            # Gọi hàm tính breaks tự viết ở trên
            breaks = pure_jenks_breaks(fvi_values, n_classes=num_classes)

    df["Vulnerability"] = df["FVI"].apply(classify_vulnerability)
            # Hàm gán nhãn dựa trên các breaks tìm được
            def classify_vulnerability_jenks(score):
                for i in range(num_classes):
                    if score <= breaks[i+1]:
                        return labels[i]
                return labels[-1]
                
            df["Vulnerability"] = df["FVI"].apply(classify_vulnerability_jenks)
            
        except Exception as e:
            # Fallback nếu tính toán gặp lỗi bất ngờ
            df["Vulnerability"] = df["FVI"].apply(lambda x: "Cao" if x >= 0.70 else ("Tương đối cao" if x >= 0.50 else ("Trung bình" if x >= 0.25 else "Thấp")))
    else:
        # Nếu số lượng giá trị phân biệt quá ít, chia tạm theo ngưỡng trị cứng
        df["Vulnerability"] = df["FVI"].apply(lambda x: "Cao" if x >= 0.70 else "Thấp")
    # ---------------------------------------------------------
        
return df

@st.cache_data
