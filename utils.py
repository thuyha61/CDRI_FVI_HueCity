import streamlit as st
import pandas as pd
import numpy as np
import os
import json

def inject_custom_css():
    """Nhúng font Roboto và chuẩn hóa giao diện học thuật"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&display=swap');
        
        html, body, [class*="css"], .stApp {
            font-family: 'Roboto', sans-serif !important;
        }
        
        .hero-banner {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #f8fafc;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        .hero-title-vn {
            font-size: 26px;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 8px;
            color: #f8fafc;
        }
        
        .hero-title-en {
            font-size: 19px;
            font-weight: 400;
            font-style: italic;
            line-height: 1.4;
            margin-bottom: 24px;
            color: #cbd5e1;
        }
        
        .hero-meta {
            font-size: 14px;
            color: #94a3b8;
            line-height: 1.6;
        }
        
        .section-title {
            font-size: 22px;
            font-weight: 500;
            color: #0f172a;
            margin-top: 20px;
            margin-bottom: 15px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }
        
        .sub-section-title {
            font-size: 17px;
            font-weight: 500;
            color: #1e293b;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        
        .academic-paragraph {
            font-size: 15px;
            line-height: 1.6;
            color: #334155;
            text-align: justify;
            margin-bottom: 15px;
        }
        
        .highlight-box {
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 15px;
            border-radius: 0 4px 4px 0;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.6;
            color: #1e293b;
        }
        
        .card-team {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .card-team-title {
            font-weight: 500;
            font-size: 16px;
            color: #0f172a;
        }
        
        .card-team-sub {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

def pure_jenks_breaks(data_list, n_classes=4):
    """
    Thuật toán Jenks Natural Breaks viết bằng Python thuần, không dùng thư viện ngoài.
    Trả về danh sách các điểm phân lớp (breaks).
    """
    # Sắp xếp và loại bỏ các giá trị NaN
    data_list = sorted([x for x in data_list if not np.isnan(x)])
    n_data = len(data_list)
    
    if n_data <= n_classes:
        return [min(data_list)] + data_list + [max(data_list)] * (n_classes - n_data)

    # Khởi tạo ma trận
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
    yte_path = "data/Flood_Vulnerability_Survey_Results_yte.xlsx"
    gd_path = "data/Flood_Vulnerability_Survey_Results.xlsx"
    
    df_yte = pd.DataFrame()
    df_gd = pd.DataFrame()
    
    # Đọc dữ liệu y tế
    if os.path.exists(yte_path):
        try:
            df_yte = pd.read_excel(yte_path)
            df_yte.columns = df_yte.columns.str.strip()
            df_yte["TypeofOrg"] = "Y tế"
        except Exception as e:
            st.error(f"Lỗi khi đọc file y tế: {e}")
            
    # Đọc dữ liệu giáo dục
    if os.path.exists(gd_path):
        try:
            df_gd = pd.read_excel(gd_path)
            df_gd.columns = df_gd.columns.str.strip()
            df_gd["TypeofOrg"] = "Giáo dục"
        except Exception as e:
            st.error(f"Lỗi khi đọc file giáo dục: {e}")
            
    # Gộp 2 nguồn dữ liệu
    if not df_yte.empty or not df_gd.empty:
        df = pd.concat([df_yte, df_gd], ignore_index=True)
    else:
        # Trả về tập dữ liệu trống có cấu trúc chuẩn nếu không tìm thấy file vật lý
        st.warning("Không tìm thấy các file dữ liệu Excel trong thư mục data/. Đang khởi tạo dữ liệu mẫu.")
        return pd.DataFrame(columns=["Name", "Commune", "TypeofOrg", "FVI", "Exposure", "Sensitivity", "Adaptive", "CoordX", "CoordY"])

    # Xử lý chuẩn hóa tên cơ sở
    if "OrganizationType" in df.columns:
        df["Name"] = df["OrganizationType"].fillna(df["TypeofOrg"])
    else:
        df["Name"] = df["TypeofOrg"]
        
    # Ép kiểu số cho các trường dữ liệu GIS & PCA
    for col in ["FVI", "exp_score", "sen_score", "ada_score", "CoordX", "CoordY", "HeightFromTheRoad"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Xử lý các giá trị khuyết thiếu (NaN)
    df["FVI"] = df["FVI"].fillna(0.0)
    df["Exposure"] = df["exp_score"].fillna(0.0)
    df["Sensitivity"] = df["sen_score"].fillna(0.0)
    df["Adaptive"] = df["ada_score"].fillna(0.0)
    df["HeightFromTheRoad"] = df["HeightFromTheRoad"].fillna(0)
    
    # Khớp tên phường từ viết tắt sang dạng đầy đủ
    commune_map = {
        "TH": "Thuận Hóa",
        "PX": "Phú Xuân",
        "VD": "Vỹ Dạ",
        "MT": "Mỹ Thượng",
        "DN": "Dương Nỗ"
    }
    if "Commune" in df.columns:
        df["Commune"] = df["Commune"].astype(str).str.strip().replace(commune_map)
    else:
        df["Commune"] = "Khác"
        
    # --- PHẦN SỬA ĐỔI: JENKS CHUẨN - KHÔNG DÙNG CHỐT CỐ ĐỊNH SAI LỆCH ---
    fvi_values = df["FVI"].dropna().tolist()
    unique_fvi_count = len(set(fvi_values))
    
    labels = ["Thấp", "Trung bình", "Tương đối cao", "Cao"]
    num_classes = 4
    
    # Đảm bảo dữ liệu đủ đa dạng để phân thành 4 nhóm
    if unique_fvi_count >= num_classes:
        try:
            # Tính toán các điểm đứt gãy tự nhiên động bằng thuật toán Jenks
            breaks = pure_jenks_breaks(fvi_values, n_classes=num_classes)
            
            def classify_vulnerability_jenks(score):
                for i in range(num_classes):
                    if score <= breaks[i+1]:
                        return labels[i]
                return labels[-1]
                
            df["Vulnerability"] = df["FVI"].apply(classify_vulnerability_jenks)
            
        except Exception:
            # PHƯƠNG ÁN DỰ PHÒNG 1: Nếu thuật toán Jenks thuần gặp lỗi do dữ liệu, 
            # chúng ta chuyển sang phân vị động (Quantiles) từ pandas thay vì dùng số chốt cứng 0.70.
            try:
                df["Vulnerability"] = pd.qcut(df["FVI"], q=num_classes, labels=labels, duplicates='drop')
            except Exception:
                # PHƯƠNG ÁN DỰ PHÒNG 2: Chia khoảng đều (Equal Intervals) dựa trên Min-Max động của bộ dữ liệu
                min_val = df["FVI"].min()
                max_val = df["FVI"].max()
                if max_val > min_val:
                    step = (max_val - min_val) / num_classes
                    dynamic_breaks = [min_val + step * i for i in range(num_classes + 1)]
                    
                    def classify_dynamic_equal(score):
                        for i in range(num_classes):
                            if score <= dynamic_breaks[i+1]:
                                return labels[i]
                        return labels[-1]
                    df["Vulnerability"] = df["FVI"].apply(classify_dynamic_equal)
                else:
                    df["Vulnerability"] = "Trung bình"
    else:
        # Nếu bộ dữ liệu cực nhỏ (ví dụ chỉ có 1-2 dòng dữ liệu), tự động gán nhãn theo thứ hạng thực tế
        # bằng cách chia đôi dựa trên trung vị (median) của chính bộ dữ liệu đó
        median_val = df["FVI"].median()
        df["Vulnerability"] = df["FVI"].apply(lambda x: "Cao" if x >= median_val else "Thấp")
    # -----------------------------------------------------------------
        
    return df

@st.cache_data
def load_aoi_geojson():
    """Đọc dữ liệu ranh giới khu vực nghiên cứu"""
    geojson_path = "data/AOI_Hue.geojson"
    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Lỗi tải GeoJSON: {e}")
            return None
    return None
