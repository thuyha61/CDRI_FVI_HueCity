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
            
    df["Vulnerability"] = df["FVI"].apply(classify_vulnerability)
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
