import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Hệ Thống Điều Hành & Kế Toán Tour Toàn Diện", layout="wide")
st.title("🏛️ HỆ THỐNG ĐIỀU HÀNH & KẾ TOÁN TOUR CÔNG TY TOÀN DIỆN")
st.caption("Giao diện Master Log Đám Mây: Kết hợp Nhập mới ➔ Sửa đổi Tour đã hoàn thành ➔ Đồng bộ 6 Phân hệ tài chính")

# --- FILE CƠ SỞ DỮ LIỆU CỐ ĐỊNH TRÊN MÁY CHỦ CLOUD ---
DATABASE_FILE = "master_data_tour.csv"

# --- HÀM TỰ ĐỘNG NẠP VÀ CHUẨN HÓA DỮ LIỆU THỰC TẾ ---
def load_database():
    if os.path.exists(DATABASE_FILE):
        try:
            df = pd.read_csv(DATABASE_FILE, encoding='utf-8-sig')
            df = df[df["NGÀY"].notna()]
            df = df[df["CODE"] != "CODE"]
            df["NGÀY"] = pd.to_datetime(df["NGÀY"], errors='coerce').dt.date
            df = df[df["NGÀY"].notna()]
            
            # Chuẩn hóa số liệu tài chính để tránh lỗi ma trận trống
            df["DOANH THU VND"] = pd.to_numeric(df["DOANH THU VND"], errors='coerce').fillna(0)
            df["GIÁ VỐN NCC"] = pd.to_numeric(df["GIÁ VỐN NCC"], errors='coerce').fillna(0)
            df["LỢI NHUẬN GỘP"] = pd.to_numeric(df["LỢI NHUẬN GỘP"], errors='coerce').fillna(0)
            df["HH sale 5%"] = pd.to_numeric(df["HH sale 5%"], errors='coerce').fillna(0)
            df["HH sale 10%"] = pd.to_numeric(df["HH sale 10%"], errors='coerce').fillna(0)
            df["SỐ PAX"] = pd.to_numeric(df["SỐ PAX"], errors='coerce').fillna(1)
            return df
        except Exception as e:
            st.error(f"Lỗi đọc file dữ liệu: {e}")
            return pd.DataFrame()
    else:
        # Khởi tạo khung cấu trúc cột chuẩn khớp 100% với tệp tin Nhật ký Excel của bạn
        df_empty = pd.DataFrame(columns=[
            "CODE", "NGÀY", "GIỜ", "DỊCH VỤ", "LOẠI", "TUYẾN", "XE", "LƯU Ý XE", 
            "BIỂN SỐ", "TÀI XẾ", "HDV", "SỐ PAX", "ĐỐI TÁC", "VAT", "TÊN KHÁCH", 
            "ĐIỂM ĐÓN", "Đ/C ĐÓN", "ĐIỂM TRẢ", "Đ/C TRẢ", "DOANH THU USD", "DOANH THU VND", 
            "PHƯƠNG THỨC TT", "Ngày TT", "CỌC", "TX THU", "GIÁ VỐN NCC", "NCC", 
            "SALES 01", "SALES 02", "LƯU Ý", "CHI PHÍ", "LỢI NHUẬN GỘP", "HH sale 5%", "HH sale 10%"
        ])
        df_empty.to_csv(DATABASE_FILE, index=False, encoding='utf-8-sig')
        return df_empty

# Nạp dữ liệu vào session state để quản lý biến động dữ liệu toàn cục
if 'master_df' not in st.session_state:
    st.session_state.master_df = load_database()

# --- SIDEBAR MENU ĐIỀU HƯỚNG ĐẦY ĐỦ 6 PHÂN HỆ KHÔNG THIẾU PHẦN NÀO ---
menu = st.sidebar.radio("PHÂN HỆ CHỨC NĂNG HỆ THỐNG", [
    "📥 1. Form Nhập Nhật Ký Mới",
    "🎯 2. Điều Hành Xe & Chỉnh Sửa Tour (Ops)",
    "💵 3. Quyết Toán Hoa Hồng Sales & Đại Lý",
    "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)",
    "🏦 5. Quản Lý Công Nợ Nhà Cung Cấp",
    "🗂️ 6. Bảng Tổng Hợp Master Log Toàn Diện"
])

# Kiểm tra dữ liệu thô toàn hệ thống
df_active = st.session_state.master_df.copy()

# Đồng bộ bộ lọc thời gian toàn cục ngay trên Sidebar để các phân hệ báo cáo tự nhảy số
if not df_active.empty:
    df_active["NGÀY"] = pd.to_datetime(df_active["NGÀY"], errors='coerce').dt.date
    df_active["Tháng"] = pd.to_datetime(df_active["NGÀY"], errors='coerce').dt.to_period("M").astype(str)
    df_active["Năm"] = pd.to_datetime(df_active["NGÀY"], errors='coerce').dt.year
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 📅 Lọc Dữ Liệu Thời Gian")
    f_mode = st.sidebar.radio("Xem báo cáo theo:", ["Toàn thời gian", "Khoảng Ngày cụ thể", "Tháng", "Năm"])
    
    if f_mode == "Khoảng Ngày cụ thể":
        col_d1, col_d2 = st.sidebar.columns(2)
        with col_d1: start_d = st.date_input("Từ ngày:", datetime.date(2026, 7, 1))
        with col_d2: end_d = st.date_input("Đến ngày:", datetime.date(2026, 12, 31))
        df_active = df_active[(df_active["NGÀY"] >= start_d) & (df_active["NGÀY"] <= end_d)]
    elif f_mode == "Tháng":
        m_list = sorted(list(df_active["Tháng"].dropna().unique()))
        m_select = st.sidebar.selectbox("Chọn tháng tài chính:", m_list if m_list else [str(datetime.date.today())[:7]])
        df_active = df_active[df_active["Tháng"] == m_select]
    elif f_mode == "Năm":
        y_list = sorted(list(df_active["Năm"].dropna().unique()))
        y_select = st.sidebar.selectbox("Chọn năm tài chính:", y_list if y_list else [datetime.date.today().year])
        df_active = df_active[df_active["Năm"] == y_select]

# ==========================================
# --- PHÂN HỆ 1: FORM NHẬP NHẬT KÝ ĐIỀU HÀNH MỚI ---
# ==========================================
if menu == "📥 1. Form Nhập Nhật Ký Mới":
    st.subheader("📥 Tiếp nhận thông tin điều hành & Kết chuyển tài chính")
    with st.form("master_input_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### 📅 Tuyến Đi & Thời Gian")
            f_code = st.text_input("Mã CODE đơn hàng (Ví dụ: MTG-2607001) *")
            f_ngay = st.date_input("NGÀY khởi hành *", datetime.date(2026, 7, 1))
            f_gio = st.text_input("GIỜ đón khách", value="04:30:00")
            f_dich_vu = st.selectbox("DỊCH VỤ *", ["Tour", "Transfer", "Vé", "Events", "Hotel"])
            f_loai = st.text_input("LOẠI (Ví dụ: Đi tour, Drop-off, Ind.)")
            f_tuyen = st.text_input("TUYẾN ĐƯỜNG / TÊN TOUR KHỞI HÀNH *")
            f_so_pax = st.number_input("SỐ PAX (Số khách) *", min_value=1, step=1, value=2)
            f_ten_khach = st.text_input("TÊN KHÁCH HÀNG / ĐOÀN KHÁCH")

        with col2:
            st.markdown("##### 🚎 Điều Phối Xe & Hành Trình (Ops)")
            f_loai_xe = st.text_input("XE (Ví dụ: 4, 7, 16, Jeep)")
            f_luu_y_xe = st.text_input("LƯU Ý XE (Ví dụ: rộng, ghế trẻ em)")
            f_bien_so = st.text_input("BIỂN SỐ XE")
            f_tai_xe = st.text_input("HỌ TÊN TÀI XẾ")
            f_hdv = st.text_input("HƯỚNG DẪN VIÊN")
            f_diem_don = st.text_input("ĐIỂM ĐÓN (Mũi Né / Tiến Thành / SGN)")
            f_diem_tra = st.text_input("ĐIỂM TRẢ")
            f_ncc = st.text_input("NHÀ CUNG CẤP DỊCH VỤ (NCC)")

        with col3:
            st.markdown("##### 💰 Doanh Thu, Giá Vốn & Sales")
            f_revenue = st.number_input("DOANH THU VND *", min_value=0, value=0, step=100000)
            f_usd = st.number_input("DOANH THU USD (Nếu có)", min_value=0.0, value=0.0, step=10.0)
            f_cost = st.number_input("GIÁ VỐN NCC *", min_value=0, value=0, step=100000)
            f_sales_01 = st.text_input("NHÂN VIÊN SALES 01 phụ trách *", value="Như")
            f_sales_02 = st.text_input("NHÂN VIÊN SALES 02")
            f_doi_tac = st.text_input("ĐỐI TÁC / ĐẠI LÝ ĐẶT")
            f_pt_tt = st.text_input("PHƯƠNG THỨC TT (Ví dụ: Chuyển khoản, Công nợ)")
            f_hh_rate = st.selectbox("TỶ LỆ HOA HỒNG TRÍCH THƯỞNG", ["10%", "5%", "0%"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Lưu Nhật Ký & Tự Động Kết Chuyển Kế Toán"):
            if f_code and f_tuyen and f_sales_01:
                f_g_profit = f_revenue - f_cost
                f_hh_5 = f_g_profit * 0.05 if f_hh_rate == "5%" and f_g_profit > 0 else 0
                f_hh_10 = f_g_profit * 0.10 if f_hh_rate == "10%" and f_g_profit > 0 else 0
                
                new_record = {
                    "CODE": f_code, "NGÀY": f_ngay, "GIỜ": f_gio, "DỊCH VỤ": f_dich_vu, "LOẠI": f_loai, "TUYẾN": f_tuyen,
                    "XE": f_loai_xe, "LƯU Ý XE": f_luu_y_xe, "BIỂN SỐ": f_bien_so, "TÀI XẾ": f_tai_xe, "HDV": f_hdv,
                    "SỐ PAX": f_so_pax, "ĐỐI TÁC": f_doi_tac, "VAT": "", "TÊN KHÁCH": f_ten_khach, "ĐIỂM ĐÓN": f_diem_don,
                    "Đ/C ĐÓN": f_diem_don, "ĐIỂM TRẢ": f_diem_tra, "Đ/C TRẢ": f_diem_tra, "DOANH THU USD": f_usd,
                    "DOANH THU VND": f_revenue, "PHƯƠNG THỨC TT": f_pt_tt, "Ngày TT": "", "CỌC": 0,
                    "TX THU": 0, "GIÁ VỐN NCC": f_cost, "NCC": f_ncc, "SALES 01": f_sales_01, "SALES 02": f_sales_02,
                    "LƯU Ý": "", "CHI PHÍ": f_cost, "LỢI NHUẬN GỘP": f_g_profit, "HH sale 5%": f_hh_5, "HH sale 10%": f_hh_10
                }
                
                df_new_row = pd.DataFrame([new_record])
                st.session_state.master_df = pd.concat([st.session_state.master_df, df_new_row], ignore_index=True)
                st.session_state.master_df.to_csv(DATABASE_FILE, index=False, encoding='utf-8-sig')
                st.success(f"✔️ Đã lưu thành công và đồng bộ dòng nhật ký {f_code} vào tệp dữ liệu!")
                st.rerun()
            else:
                st.error("⚠️ Vui lòng điền đầy đủ các mục bắt buộc dấu (*)")

    st.write("### 📜 Top 5 bản ghi mới nhất vừa ghi nhận")
    if not st.session_state.master_df.empty:
        st.dataframe(st.session_state.master_df.tail(5), use_container_width=True)

# ==========================================
# --- PHÂN HỆ 2: ĐIỀU HÀNH XE & CHỈNH SỬA TOUR (OPS) ---
# ==========================================
elif menu == "🎯 2. Điều Hành Xe & Chỉnh Sửa Tour (Ops)":
    st.subheader("🎯 Quản lý Điều Hành & Chỉnh Sửa Dữ Liệu Tour / Xe Chạy")
    
    if not df_active.empty:
        st.markdown("### 📝 Cập nhật thông tin / Chỉnh sửa Tour")
        with st.expander("🛠️ Click vào đây để chỉnh sửa nhanh thông tin Tour bất kỳ"):
            list_codes = sorted(df_active["CODE"].dropna().unique().tolist())
            selected_code = st.selectbox("Chọn Mã CODE Tour cần sửa thông tin:", list_codes)
            
            # Khởi tạo bản ghi sửa đổi
            current_row = df_active[df_active["CODE"] == selected_code].iloc[0]
            
            with st.form("edit_form"):
                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    u_tuyen = st.text_input("Sửa Tuyến đường / Tên Tour:", value=str(current_row["TUYẾN"]))
                    u_pax = st.number_input("Sửa Số Pax:", min_value=1, value=int(current_row["SỐ PAX"]))
                     u_txe = st.text_input("Gán / Đổi Tài Xế:", value=str(current_row["TÀI XẾ"]) if pd.notna(current_row["TÀI XẾ"]) else "")
                with ec2:
                    u_bso = st.text_input("Sửa Biển Số Xe:", value=str(current_row["BIỂN SỐ"]) if pd.notna(current_row["BIỂN SỐ"]) else "")
                    u_hdv = st.text_input("Sửa Hướng Dẫn Viên:", value=str(current_row["HDV"]) if pd.notna(current_row["HDV"]) else "")
                    u_pt_tt = st.text_input("Sửa Phương thức TT / Trạng thái:", value=str(current_row["PHƯƠNG THỨC TT"]) if pd.notna(current_row["PHƯƠNG THỨC TT"]) else "")
                with ec3:
                    u_rev = st.number_input("Cập nhật lại Doanh Thu VND:", value=int(current_row["DOANH THU VND"]))
                    u_cost = st.number_input("Cập nhật lại Giá Vốn NCC:", value=int(current_row["GIÁ VỐN NCC"]))
                    u_luuy = st.text_input("Sửa Ghi chú / Lưu ý:", value=str(current_row["LƯU Ý"]) if pd.notna(current_row["LƯU Ý"]) else "")
                
                if st.form_submit_button("💾 Xác Nhận Cập Nhật Thay Đổi"):
                    u_g_profit = u_rev - u_cost
                    u_hh5 = u_g_profit * 0.05 if current_row["HH sale 5%"] > 0 and u_g_profit > 0 else 0
                    u_hh10 = u_g_profit * 0.10 if current_row["HH sale 10%"] > 0 and u_g_profit > 0 else 0
                    
                    st.session_state.master_df.loc[st.session_state.master_df["CODE"] == selected_code, [
                        "TUYẾN", "SỐ PAX", "TÀI XẾ", "BIỂN SỐ", "HDV", "PHƯƠNG THỨC TT", "DOANH THU VND", "GIÁ VỐN NCC", "LƯU Ý", "LỢI NHUẬN GỘP", "HH sale 5%", "HH sale 10%"
                    ]] = [u_tuyen, u_pax, u_txe, u_bso, u_hdv, u_pt_tt, u_rev, u_cost, u_luuy, u_g_profit, u_hh5, u_hh10]
                    
                    st.session_state.master_df.to_csv(DATABASE_FILE, index=False, encoding='utf-8-sig')
                    st.success(f"✔️ Đã cập nhật thành công dữ liệu chỉnh sửa của Tour {selected_code}!")
                    st.rerun()
                    
        st.markdown("---")
        st.markdown("### 🚎 Nhật Ký Điều Phối Vận Tải Toàn Đoàn")
        st.dataframe(df_active[["CODE", "NGÀY", "GIỜ", "DỊCH VỤ", "TUYẾN", "XE", "BIỂN SỐ", "TÀI XẾ", "HDV", "SỐ PAX", "PHƯƠNG THỨC TT"]], use_container_width=True)
    else:
        st.info("Chưa có dữ liệu vận hành điều xe trong kỳ lọc.")

# ==========================================
# --- PHÂN HỆ 3: QUYẾT TOÁN HOA HỒNG SALES ---
# ==========================================
elif menu == "💵 3. Quyết Toán Hoa Hồng Sales & Đại Lý":
    st.subheader("💵 Phân hệ kiểm soát và trích chi lương thưởng hoa hồng động")
    if not df_active.empty:
        df_active["HH_Tổng"] = df_active["HH sale 5%"].fillna(0) + df_active["HH sale 10%"].fillna(0)
        st.markdown("##### 🔍 Chi tiết nghĩa vụ hoa hồng phân bổ theo Nhân viên Sales")
        df_sales_group = df_active.groupby("SALES 01").agg({
            "CODE": "count",
            "SỐ PAX": "sum",
            "DOANH THU VND": "sum",
            "HH_Tổng": "sum"
        }).reset_index().rename(columns={
            "SALES 01": "Nhân Viên Sales / Đại Lý",
            "CODE": "Tổng Số Đơn Chốt",
            "SỐ PAX": "Tổng Số Pax Mang Về",
            "DOANH THU VND": "Doanh Số Đạt Được (VND)",
            "HH_Tổng": "Tổng Tiền Hoa Hồng Nhận (VND)"
        })
        st.dataframe(df_sales_group, use_container_width=True)
        st.metric("Tổng ngân sách trích chi hoa hồng toàn công ty:", f"{df_sales_group['Tổng Tiền Hoa Hồng Nhận (VND)'].sum():,.0f} VND")
    else:
        st.info("Chưa có dữ liệu đối soát hoa hồng trong kỳ lọc.")

# ==========================================
# --- PHÂN HỆ 4: TRUNG TÂM BÁO CÁO TÀI CHÍNH ---
# ==========================================
elif menu == "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)":
    st.subheader("📊 Hệ Thống Phân Tích Kết Quả Kinh Doanh & Hiệu Suất Sinh Lời")
    if not df_active.empty:
        df_active["HH_Tổng"] = df_active["HH sale 5%"].fillna(0) + df_active["HH sale 10%"].fillna(0)
        df_active["Lợi_Nhuận_Thuần"] = df_active["LỢI NHUẬN GỘP"] - df_active["HH_Tổng"]
        r_gross = df_active["DOANH THU VND"].sum()
        c_ncc = df_active["GIÁ VỐN NCC"].sum()
        p_gross = df_active["LỢI NHUẬN GỘP"].sum()
        c_comm = df_active["HH_Tổng"].sum()
        p_net = df_active["Lợi_Nhuận_Thuần"].sum()
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Doanh Thu Tổng (Gross)", f"{r_gross:,.0f} VND")
        mc2.metric("Chi Phí Giá Vốn NCC", f"{c_ncc:,.0f} VND")
        mc3.metric("Tổng Chi Hoa Hồng", f"{c_comm:,.0f} VND")
        mc4.metric("Lợi Nhuận Thuần Thực Thu", f"{p_net:,.0f} VND", delta=f"{((p_net/r_gross)*100) if r_gross > 0 else 0:.1f}% ROS")
        
        p_l_display = pd.DataFrame([
            {"Hạng mục tài chính doanh nghiệp": "A. TỔNG DOANH THU HOẠT ĐỘNG KINH DOANH TOUR & XE", "Giá trị kết chuyển (VND)": r_gross},
            {"Hạng mục tài chính doanh nghiệp": "B. CHI PHÍ GIÁ VỐN DỊCH VỤ (Trả nhà xe, land đối tác, vé)", "Giá trị kết chuyển (VND)": c_ncc},
            {"Hạng mục tài chính doanh nghiệp": "C. LỢI NHUẬN GỘP KINH DOANH SƠ CẤP (A - B)", "Giá trị kết chuyển (VND)": p_gross},
            {"Hạng mục tài chính doanh nghiệp": "D. CHI PHÍ BÁN HÀNG (Trích thưởng hoa hồng Sales 5% & 10%)", "Giá trị kết chuyển (VND)": c_comm},
            {"Hạng mục tài chính doanh nghiệp": "E. LỢI NHUẬN THUẦN DOANH NGHIỆP BIÊN ĐỘNG (C - D)", "Giá trị kết chuyển (VND)": p_net}
        ])
        st.table(p_l_display)
    else:
        st.info("Không có dữ liệu tài chính trong khoảng thời gian lọc.")

# ==========================================
# --- PHÂN HỆ 5: QUẢN LÝ CÔNG NỢ NHÀ CUNG CẤP ---
# ==========================================
elif menu == "🏦 5. Quản Lý Công Nợ Nhà Cung Cấp":
    st.subheader("🏦 Bảng đối soát nghĩa vụ thanh toán chi trả cho các Nhà cung cấp dịch vụ (NCC)")
    if not df_active.empty:
        df_debt_clean = df_active[df_active["NCC"].notna() & (df_active["NCC"] != "0") & (df_active["NCC"] != " ")]
        df_debt_group = df_debt_clean.groupby("NCC").agg({
            "CODE": "count",
            "GIÁ VỐN NCC": "sum"
        }).reset_index().rename(columns={
            "NCC": "Tên Nhà Cung Cấp (Đối Tác Đầu Vào)",
            "CODE": "Số Lượng Chuyến Đi Phục Vụ",
            "GIÁ VỐN NCC": "Tổng Tiền Công Ty Phải Trả (VND)"
        })
        st.dataframe(df_debt_group, use_container_width=True)
        st.metric("Tổng Số Tiền Phải Chi Trả NCC Tạm Tính:", f"{df_debt_group['Tổng Tiền Công Ty Phải Trả (VND)'].sum():,.0f} VND")
    else:
        st.info("Chưa có dữ liệu đối soát công nợ đối tác trong kỳ lọc.")

# ==========================================
# --- PHÂN HỆ 6: BẢNG TỔNG HỢP MASTER LOG TOÀN DIỆN ---
# ==========================================
elif menu == "🗂️ 6. Bảng Tổng Hợp Dữ Liệu Toàn Diện":
    st.subheader("🗂️ Bảng Phân Tích & Tổng Hợp Master Data Toàn Hệ Thống")
    st.caption("Dữ liệu thô đồng bộ thời gian thực phục vụ đối soát đa chiều.")
    if not df_active.empty:
        f1, f2, f3 = st.columns(3)
        with f1: 
            s_tuyen = st.text_input("Tìm nhanh theo Tuyến đường / Tên Tour:")
        with f2: 
            s_sales = st.text_input("Tìm nhanh theo Nhân viên Sales phụ trách:")
        with f3: 
            s_txe = st.text_input("Tìm nhanh theo Tên Tài xế:")
            
        if s_tuyen:
            df_active = df_active[df_active["TUYẾN"].str.contains(s_tuyen, case=False, na=False)]
        if s_sales:
            df_active = df_active[df_active["SALES 01"].str.contains(s_sales, case=False, na=False)]
        if s_txe:
            df_active = df_active[df_active["TÀI XẾ"].str.contains(s_txe, case=False, na=False)]
            
        st.dataframe(df_active, use_container_width=True)
        csv_bytes = df_active.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Xuất Bảng Tổng Hợp Dữ Liệu Ra File Excel (.CSV)",
            data=csv_bytes,
            file_name=f"Master_Log_Tour_All_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("Hệ thống dữ liệu trống trong khoảng thời gian lọc.")
