import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Mũi Né Express - Hệ Thống Số Hóa Vận Hành", layout="wide")
st.title("🏛️ HỆ THỐNG ĐIỀU HÀNH & KẾ TOÁN TOUR MŨI NÉ EXPRESS")
st.caption("Giải pháp số hóa vận hành tích hợp hệ thống Core Dataset & Luồng xử lý dữ liệu tự động BPM")

# --- ĐƯỜNG DẪN DATABASE LƯU TRỮ TRÊN ĐÁM MÂY CLOUD ---
DATA_FILE = "master_data_tour.csv"

# --- HÀM XỬ LÝ VÀ CHUẨN HÓA DỮ LIỆU LOG GỐC DOANH NGHIỆP ---
@st.cache_data
def load_and_clean_master_log():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    try:
        # Đọc dữ liệu gốc, dọn dẹp khoảng trắng thừa và lỗi font chữ tiếng Việt
        df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
        
        # Bóc tách và giữ lại mảng Nhật ký điều hành thực tế (Bỏ các dòng tổng gộp của Excel cũ)
        df = df[df["NGÀY"].notna()]
        df = df[df["CODE"] != "CODE"]
        df = df[~df["NGÀY"].str.contains("Total|Tổng|Chỉ tiêu", case=False, na=False)]
        
        # Đồng bộ và ép kiểu dữ liệu an toàn phục vụ các hàm kế toán tính toán
        df["NGÀY_DT"] = pd.to_datetime(df["NGÀY"], errors='coerce').dt.date
        df = df[df["NGÀY_DT"].notna()]
        
        df["DOANH THU VND"] = pd.to_numeric(df["DOANH THU VND"], errors='coerce').fillna(0)
        df["GIÁ VỐN NCC"] = pd.to_numeric(df["GIÁ VỐN NCC"], errors='coerce').fillna(0)
        df["LỢI NHUẬN GỘP"] = pd.to_numeric(df["LỢI NHUẬN GỘP"], errors='coerce').fillna(0)
        df["HH sale 5%"] = pd.to_numeric(df["HH sale 5%"], errors='coerce').fillna(0)
        df["HH sale 10%"] = pd.to_numeric(df["HH sale 10%"], errors='coerce').fillna(0)
        df["CHI PHÍ"] = pd.to_numeric(df["CHI PHÍ"], errors='coerce').fillna(0)
        df["SỐ PAX"] = pd.to_numeric(df["SỐ PAX"], errors='coerce').fillna(1)
        
        # Tự động đồng bộ hóa các trường thông tin trống để tránh lỗi giao diện
        df["TÀI XẾ"] = df["TÀI XẾ"].fillna("Chưa điều xe")
        df["BIỂN SỐ"] = df["BIỂN SỐ"].fillna("Chưa có")
        df["HDV"] = df["HDV"].fillna("Không có")
        df["NCC"] = df["NCC"].fillna("Nội bộ")
        df["SALES 01"] = df["SALES 01"].fillna("Văn phòng")
        df["PHƯƠNG THỨC TT"] = df["PHƯƠNG THỨC TT"].fillna("Chưa xác định")
        
        return df
    except Exception as e:
        st.error(f"Lỗi phân rã cấu trúc file Master: {e}")
        return pd.DataFrame()

# Tải dữ liệu vào bộ nhớ đệm an toàn hệ thống
df_master = load_and_clean_master_log()

# --- SIDEBAR MENU: ĐỒNG BỘ 100% THEO CHUẨN 6 NỘI DUNG GIẢI PHÁP ---
menu = st.sidebar.radio("TRUNG TÂM SỐ HÓA VẬN HÀNH (BASE BPM)", [
    "📥 1. Tiếp Nhận Booking (Sales Form)",
    "🎯 2. Điều Phối Xe & Tài Xế (Ops)",
    "💵 3. Quyết Toán Hoa Hồng Sales",
    "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)",
    "🏦 5. Quản Lý Giá Vốn & Công Nợ NCC",
    "🗂️ 6. Bảng Tra Cứu Dữ Liệu Toàn Diện"
])

if df_master.empty:
    st.error(f"⚠️ Hệ thống trống dữ liệu! Hãy đảm bảo file `{DATA_FILE}` trên GitHub chứa đầy đủ nội dung dòng nhật ký thực tế.")
else:
    # Thiết lập bộ lọc thời gian nâng cao dùng chung cho toàn bộ các phân hệ báo cáo
    df_master["Tháng"] = pd.to_datetime(df_master["NGÀY_DT"]).dt.to_period("M").astype(str)
    df_master["Năm"] = pd.to_datetime(df_master["NGÀY_DT"]).dt.year
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 🔍 Bộ Lọc Kỳ Kế Toán")
    f_type = st.sidebar.radio("Lọc số liệu theo:", ["Khoảng Ngày tự chọn", "Tổng Hợp Tháng", "Tổng Hợp Năm"])
    
    if f_type == "Khoảng Ngày tự chọn":
        s_d = st.sidebar.date_input("Từ ngày:", datetime.date(2026, 7, 1))
        e_d = st.sidebar.date_input("Đến ngày:", datetime.date(2026, 8, 31))
        df_active = df_master[(df_master["NGÀY_DT"] >= s_d) & (df_master["NGÀY_DT"] <= e_d)]
    elif f_type == "Tổng Hợp Tháng":
        m_sel = st.sidebar.selectbox("Chọn tháng báo cáo:", sorted(list(df_master["Tháng"].unique())))
        df_active = df_master[df_master["Tháng"] == m_sel]
    elif f_type == "Tổng Hợp Năm":
        y_sel = st.sidebar.selectbox("Chọn năm báo cáo:", sorted(list(df_master["Năm"].unique())))
        df_active = df_master[df_master["Năm"] == y_sel]

    # ==========================================
    # --- PHÂN HỆ 1: TIẾP NHẬN BOOKING (SALES FORM) ---
    # ==========================================
    if menu == "📥 1. Tiếp Nhận Booking (Sales Form)":
        st.subheader("📥 Tiếp Nhận Yêu Cầu Đặt Chỗ - Cấp Mã Đơn Tự Động")
        
        with st.form("new_booking_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("##### 📝 1. Thông Tin Tuyến Đi")
                in_code = st.text_input("Mã CODE Đơn Hàng (Cấp tự động) *", value=f"MTG-{datetime.date.today().strftime('%y%m')}{len(st.session_state.get('master_df', df_master))+1:03d}")
                in_ngay = st.date_input("NGÀY khởi hành *", datetime.date(2026, 7, 1))
                in_gio = st.text_input("GIỜ đón khách", value="04:30:00")
                in_dichvu = st.selectbox("DỊCH VỤ CỐ ĐỊNH", ["Tour", "Transfer", "Vé", "Events", "Hotel"])
                in_tuyen = st.text_input("TUYẾN ĐƯỜNG / TÊN TOUR *")
            with col2:
                st.markdown("#####    2. Điều Phối Dự Kiến")
                in_xe = st.text_input("Loại xe yêu cầu (Ví dụ: 4, 7, 16, Jeep)")
                in_pax = st.number_input("SỐ PAX (Số lượng khách) *", min_value=1, step=1, value=2)
                in_khach = st.text_input("TÊN KHÁCH HÀNG / ĐOÀN KHÁCH")
                in_don = st.text_input("ĐIỂM ĐÓN KHÁCH")
                in_tra = st.text_input("ĐIỂM TRẢ KHÁCH")
            with col3:
                st.markdown("##### 💰 3. Kế Toán Tài Chính")
                in_rev = st.number_input("DOANH THU VND *", min_value=0, value=0, step=100000)
                in_cost = st.number_input("GIÁ VỐN NCC (Chi phí gốc) *", min_value=0, value=0, step=100000)
                in_sales = st.text_input("NHÂN VIÊN SALES 01 phụ trách *", value="Như")
                in_doitac = st.text_input("ĐỐI TÁC / ĐẠI LÝ GỬI")
                in_tt = st.text_input("PHƯƠNG THỨC TT (TX thu / HDV thu / Công nợ)")
                
            if st.form_submit_button("💾 Xác Nhận Tạo Hồ Sơ Booking Mới"):
                if in_tuyen and in_sales:
                    g_profit = in_rev - in_cost
                    new_row = {
                        "CODE": in_code, "NGÀY": in_ngay, "GIỜ": in_gio, "DỊCH VỤ": in_dichvu, "LOẠI": "Ind.", 
                        "TUYẾN": in_tuyen, "XE": in_xe, "LƯU Ý XE": "", "BIỂN SỐ": "Chưa gán", "TÀI XẾ": "Chưa điều xe", 
                        "HDV": "Không có", "SỐ PAX": in_pax, "ĐỐI TÁC": in_doitac, "VAT": "", "TÊN KHÁCH": in_khach, 
                        "ĐIỂM ĐÓN": in_don, "Đ/C ĐÓN": "", "ĐIỂM TRẢ": in_tra, "Đ/C TRẢ": "", "DOANH THU USD": 0, 
                        "DOANH THU VND": in_rev, "PHƯƠNG THỨC TT": in_tt, "Ngày TT": "", "CỌC": 0, "TX THU": 0, 
                        "GIÁ VỐN NCC": in_cost, "NCC": "Chưa gán", "SALES 01": in_sales, "SALES 02": "", "LƯU Ý": "", 
                        "CHI PHÍ": in_cost, "LỢI NHUẬN GỘP": g_profit, "HH sale 5%": 0, "HH sale 10%": (g_profit * 0.1 if g_profit > 0 else 0)
                    }
                    # Tiến hành nối dòng dữ liệu mới và thực hiện ghi đè lưu trữ vĩnh viễn
                    df_extended = pd.concat([df_master, pd.DataFrame([new_row])], ignore_index=True)
                    df_extended.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                    st.success(f"✔️ Đã lập hồ sơ thành công cho Đơn hàng {in_code}!")
                    st.rerun()

        st.markdown("### 📜 Đơn hàng vừa nhập gần đây")
        st.dataframe(df_master.tail(5), use_container_width=True)

    # ==========================================
    # --- PHÂN HỆ 2: ĐIỀU PHỐI XE & TÀI XẾ (OPS) ---
    # ==========================================
    elif menu == "🎯 2. Điều Phối Xe & Tài Xế (Ops)":
        st.subheader("🎯 Lịch Điều Xe Dùng Chung & Cập Nhật Trạng Thái Vận Hành")
        
        # Khung công cụ Chỉnh sửa/Điều xe cho cả các đơn đã hoàn thành
        with st.expander("🛠️ Click mở form cập nhật thông tin Tài Xế / Biển Số / HDV cho Chuyến đi"):
            list_codes = df_master["CODE"].dropna().tolist()
            select_code = st.selectbox("Chọn Mã CODE chuyến xe cần điều phối / sửa đổi:", list_codes)
            idx = df_master[df_master["CODE"] == select_code].index
            row_data = df_master.loc[idx].iloc[0]
            
            with st.form("ops_edit_form"):
                o_c1, o_c2, o_c3 = st.columns(3)
                with o_c1:
                    u_txe = st.text_input("Đổi Tên Tài Xế:", value=str(row_data["TÀI XẾ"]))
                    u_bso = st.text_input("Đổi Biển Số Xe:", value=str(row_data["BIỂN SỐ"]))
                with o_c2:
                    u_hdv = st.text_input("Đổi Hướng Dẫn Viên:", value=str(row_data["HDV"]))
                    u_tt = st.text_input("Cập nhật Phương thức TT / Trạng thái:", value=str(row_data["PHƯƠNG THỨC TT"]))
                with o_c3:
                    u_rev = st.number_input("Sửa Doanh Thu VND:", value=int(row_data["DOANH THU VND"]))
                    u_cost = st.number_input("Sửa Chi Phí NCC:", value=int(row_data["GIÁ VỐN NCC"]))
                    
                if st.form_submit_button("🔄 Xác Nhận Cập Nhật Lịch Điều Xe"):
                    df_master.loc[idx, ["TÀI XẾ", "BIỂN SỐ", "HDV", "PHƯƠNG THỨC TT", "DOANH THU VND", "GIÁ VỐN NCC", "LỢI NHUẬN GỘP"]] = [u_txe, u_bso, u_hdv, u_tt, u_rev, u_cost, (u_rev - u_cost)]
                    df_master.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                    st.success(f"✔️ Đã đồng bộ trạng thái mới cho chuyến {select_code}!")
                    st.rerun()
                    
        st.markdown("### 📋 Nhật Ký Điều Phối Vận Tải Toàn Đoàn")st.dataframe(df_active[["CODE", "NGÀY", "GIỜ", "DỊCH VỤ", "TUYẾN", "XE", "BIỂN SỐ", "TÀI XẾ", "HDV", "SỐ PAX", "PHƯƠNG THỨC TT"]], use_container_width=True)

# ==========================================
# --- PHÂN HỆ 3: QUYẾT TOÁN HOA HỒNG SALES ---
# ==========================================
elif menu == "💵 3. Quyết Toán Hoa Hồng Sales":
    st.subheader("💵 Quyết Toán Lương Thưởng Hoa Hồng Nhân Viên Kinh Doanh")
    df_active["Tổng Hoa Hồng Chi"] = df_active["HH sale 5%"] + df_active["HH sale 10%"]
    df_sales = df_active.groupby("SALES 01").agg({
        "CODE": "count",
        "SỐ PAX": "sum",
        "DOANH THU VND": "sum",
        "Tổng Hoa Hồng Chi": "sum"
    }).reset_index().rename(columns={
        "SALES 01": "Nhân Viên Sales Phụ Trách",
        "CODE": "Số Lượng Đơn Chốt",
        "SỐ PAX": "Tổng Pax Mang Về",
        "DOANH THU VND": "Doanh Số Mang Về (VND)",
        "Tổng Hoa Hồng Chi": "Tiền Hoa Hồng Nhận (VND)"
    })
    st.dataframe(df_sales, use_container_width=True)
    st.metric("Tổng chi ngân sách hoa hồng trích thưởng trong kỳ:", f"{df_sales['Tiền Hoa Hồng Nhận (VND)'].sum():,.0f} VND")

# ==========================================
# --- PHÂN HỆ 4: TRUNG TÂM BÁO CÁO TÀI CHÍNH ---
# ==========================================
elif menu == "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)":
    st.subheader("🏛️ Báo Cáo Lãi Lỗ Doanh Nghiệp (P&L) - Kết Quả Thu Chi")
    df_active["HH_Tổng"] = df_active["HH sale 5%"] + df_active["HH sale 10%"]
    df_active["Lợi_Nhuận_Thuần"] = df_active["LỢI NHUẬN GỘP"] - df_active["HH_Tổng"]
    r_gross = df_active["DOANH THU VND"].sum()
    c_ncc = df_active["GIÁ VỐN NCC"].sum()
    p_gross = df_active["LỢI NHUẬN GỘP"].sum()
    c_comm = df_active["HH_Tổng"].sum()
    p_net = df_active["Lợi_Nhuận_Thuần"].sum()
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Doanh Thu Hoạt Động (Gross)", f"{r_gross:,.0f} VND")
    mc2.metric("Chi Phí Giá Vốn Đầu Vào", f"{c_ncc:,.0f} VND")
    mc3.metric("Chi Phí Hoa Hồng Trích Chi", f"{c_comm:,.0f} VND")
    mc4.metric("LỢI NHUẬN THUẦN (NET)", f"{p_net:,.0f} VND", delta=f"{((p_net/r_gross)*100) if r_gross > 0 else 0:.1f}% ROS")
    
    p_l_df = pd.DataFrame([
        {"Chỉ tiêu tài chính doanh nghiệp": "1. TỔNG DOANH THU HOẠT ĐỘNG KINH DOANH TOUR & VẬN TẢI", "Giá trị (VND)": r_gross},
        {"Chỉ tiêu tài chính doanh nghiệp": "2. CHI PHÍ GIÁ VỐN DỊCH VỤ (Trả Đội xe, Land tour, Vé...)", "Giá trị (VND)": c_ncc},
        {"Chỉ tiêu tài chính doanh nghiệp": "3. LỢI NHUẬN GỘP KINH DOANH SƠ CẤP (Mục 1 - Mục 2)", "Giá trị (VND)": p_gross},
        {"Chỉ tiêu tài chính doanh nghiệp": "4. TỔNG CHI PHÍ HOA HỒNG (Thưởng Sales & Đối tác đại lý)", "Giá trị (VND)": c_comm},
        {"Chỉ tiêu tài chính doanh nghiệp": "5. LỢI NHUẬN THUẦN TRƯỚC THUẾ DOANH NGHIỆP THU VỀ (Mục 3 - Mục 4)", "Giá trị (VND)": p_net}
    ])
    st.table(p_l_df)

# ==========================================
# --- PHÂN HỆ 5: QUẢN LÝ GIÁ VỐN & CÔNG NỢ NCC ---
# ==========================================
elif menu == "🏦 5. Quản Lý Giá Vốn & Công Nợ NCC":
    st.subheader("🏦 Bảng Đối Soát Giá Vốn & Nghĩa Vụ Thanh Toán Nhà Cung Cấp")
    df_active = df_active[df_active["NCC"].notna() & (df_active["NCC"] != "0") & (df_active["NCC"] != " ")]
    df_ncc_debt = df_active.groupby("NCC").agg({
        "CODE": "count",
        "GIÁ VỐN NCC": "sum"
    }).reset_index().rename(columns={
        "NCC": "Tên Đơn Vị Nhà Cung Cấp / Nhà Xe Đối Tác",
        "CODE": "Số Chuyến Đi Đã Phục Vụ",
        "GIÁ VỐN NCC": "Nghĩa Vụ Thanh Toán Nợ Tích Lũy (VND)"
    })
    st.dataframe(df_ncc_debt, use_container_width=True)
    st.metric("Tổng giá trị công nợ đầu vào NCC toàn hệ thống:", f"{df_ncc_debt['Nghĩa Vụ Thanh Toán Nợ Tích Lũy (VND)'].sum():,.0f} VND")

# ==========================================
# --- PHÂN HỆ 6: BẢNG TỔNG HỢP MASTER LOG TOÀN DIỆN ---
# ==========================================
elif menu == "🗂️ 6. Bảng Tổng Hợp Dữ Liệu Toàn Diện":
    st.subheader("🗂️ Trung Tâm Tra Cứu & Kết Xuất Dữ Liệu Master Log")
    f1, f2, f3 = st.columns(3)
    with f1: 
        s_t = st.text_input("Lọc nhanh theo Tuyến / Tên Tour:")
