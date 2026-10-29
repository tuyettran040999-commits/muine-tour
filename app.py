import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Hệ Thống Điều Hành & Kế Toán Tour", layout="wide")
st.title("🏛️ HỆ THỐNG ĐIỀU HÀNH & KẾ TOÁN TOUR CÔNG TY TOÀN DIỆN")
st.caption("Giao diện Cloud thông minh: Nhập liệu Form ➔ Tự động lưu Database ➔ Kết xuất báo cáo kế toán (P&L)")

# --- FILE CƠ SỞ DỮ LIỆU CỐ ĐỊNH TRÊN MÁY CHỦ CLOUD ---
DATABASE_FILE = "data_master_log.csv"

# --- HÀM KHỞI TẠO VÀ ĐỌC DỮ LIỆU AN TOÀN ---
def load_database():
    if os.path.exists(DATABASE_FILE):
        try:
            df = pd.read_csv(DATABASE_FILE)
            # Chuyển đổi định dạng ngày an toàn
            df["NGÀY"] = pd.to_datetime(df["NGÀY"], errors='coerce').dt.date
            return df
        except Exception as e:
            st.error(f"Lỗi đọc file dữ liệu: {e}")
            return pd.DataFrame()
    else:
        # Nếu chưa có file, khởi tạo khung dữ liệu chuẩn y hệt cấu trúc file gốc của bạn
        df_init = pd.DataFrame(columns=[
            "CODE", "NGÀY", "GIỜ", "DỊCH VỤ", "LOẠI", "TUYẾN", "XE", "LƯU Ý XE", 
            "BIỂN SỐ", "TÀI XẾ", "HDV", "SỐ PAX", "ĐỐI TÁC", "VAT", "TÊN KHÁCH", 
            "ĐIỂM ĐÓN", "Đ/C ĐÓN", "ĐIỂM TRẢ", "Đ/C TRẢ", "DOANH THU USD", "DOANH THU VND", 
            "PHƯƠNG THỨC TT", "Ngày TT", "CỌC", "TX THU", "GIÁ VỐN NCC", "NCC", 
            "SALES 01", "SALES 02", "LƯU Ý", "CHI PHÍ", "LỢI NHUẬN GỘP", "HH sale 5%", "HH sale 10%"
        ])
        # Nạp dữ liệu mẫu ban đầu từ file log của bạn để hệ thống có sẵn số liệu đối soát
        init_records = [
            {"CODE": "MTG-2607001", "NGÀY": datetime.date(2026, 7, 1), "GIỜ": "04:30:00", "DỊCH VỤ": "Tour", "LOẠI": "Ind.", "TUYẾN": "Mekong Only", "XE": "7", "TÀI XẾ": "Hùng", "HDV": "Xuân Lâm", "SỐ PAX": 4, "ĐỐI TÁC": "Ms. An - Hoàng Ngọc", "TÊN KHÁCH": "Mr. Kaczorowski Przemyslaw", "ĐIỂM ĐÓN": "Mũi Né", "DOANH THU VND": 7800000, "GIÁ VỐN NCC": 3000000, "LỢI NHUẬN GỘP": 4800000, "SALES 01": "Như", "HH sale 10%": 480000, "PHƯƠNG THỨC TT": "HDV thu khách"},
            {"CODE": "MTG-2607002", "NGÀY": datetime.date(2026, 7, 7), "GIỜ": "05:30:00", "DỊCH VỤ": "Tour", "LOẠI": "Ind.", "TUYẾN": "Dalat Premium", "XE": "7", "TÀI XẾ": "Đức Anh", "HDV": "Quốc Uy", "SỐ PAX": 3, "ĐỐI TÁC": "", "TÊN KHÁCH": "Tarasov Aleksandr", "ĐIỂM ĐÓN": "Mũi Né", "DOANH THU VND": 7047000, "GIÁ VỐN NCC": 3209000, "LỢI NHUẬN GỘP": 3838000, "SALES 01": "Ân", "HH sale 5%": 191900, "PHƯƠNG THỨC TT": "HDV thu khách"},
            {"CODE": "MTG-2607003", "NGÀY": datetime.date(2026, 7, 8), "GIỜ": "08:00:00", "DỊCH VỤ": "Tour", "LOẠI": "Ind.", "TUYẾN": "Jeep tour with guide", "XE": "Jeep", "TÀI XẾ": "Trương", "HDV": "Đình An", "SỐ PAX": 3, "ĐỐI TÁC": "RRPT", "TÊN KHÁCH": "Willnow Karsten", "ĐIỂM ĐÓN": "Tiến Thành", "DOANH THU VND": 2821500, "GIÁ VỐN NCC": 744000, "LỢI NHUẬN GỘP": 2077500, "SALES 01": "Vân", "HH sale 10%": 207750, "PHƯƠNG THỨC TT": "Công nợ"}
        ]
        df_init = pd.concat([df_init, pd.DataFrame(init_records)], ignore_index=True)
        df_init.to_csv(DATABASE_FILE, index=False, encoding='utf-8-sig')
        return df_init

# Nạp dữ liệu vào session state để quản lý tập trung
if 'master_df' not in st.session_state:
    st.session_state.master_df = load_database()

# --- SIDEBAR THANH ĐIỀU HƯỚNG ---
menu = st.sidebar.radio("PHÂN HỆ CHỨC NĂNG", [
    "📥 1. Form Nhập Liệu Điều Hành Mới",
    "🗂️ 2. Bảng Tổng Hợp Master Log",
    "📊 3. Báo Cáo Tài Chính Biến Động (P&L)"
])

# ==========================================
# --- PHÂN HỆ 1: FORM NHẬP LIỆU ĐIỀU HÀNH MỚI ---
# ==========================================
if menu == "📥 1. Form Nhập Liệu Điều Hành Mới":
    st.subheader("📥 Tiếp nhận dữ liệu đặt xe, đặt Tour lẻ và kết chuyển dòng tiền")
    
    with st.form("master_input_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### 📅 Tuyến Đi & Thời Gian")
            code = st.text_input("Mã CODE đơn hàng *", value=f"MTG-{datetime.date.today().strftime('%d%m')}{len(st.session_state.master_df)+1:02d}")
            ngay = st.date_input("NGÀY khởi hành *", datetime.date(2026, 7, 1))
            gio = st.text_input("GIỜ đón khách", value="04:30:00")
            dich_vu = st.selectbox("DỊCH VỤ *", ["Tour", "Transfer", "Vé", "Events", "Hotel"])
            loai = st.text_input("LOẠI HÌNH (Ví dụ: Đi tour, Drop-off, Ind.)")
            tuyen = st.text_input("TUYẾN ĐƯỜNG / TÊN TOUR CHI TIẾT *")
            so_pax = st.number_input("SỐ PAX (Số khách) *", min_value=1, step=1, value=2)
            ten_khach = st.text_input("TÊN KHÁCH HÀNG / ĐOÀN KHÁCH")

        with col2:
            st.markdown("##### 🚎 Điều Phối Xe & Địa Điểm")
            loai_xe = st.text_input("XE (Ví dụ: 4, 7, 16, Jeep)")
            luu_y_xe = st.text_input("LƯU Ý XE (Ví dụ: Ghế trẻ em, rộng)")
            bien_so = st.text_input("BIỂN SỐ XE")
            tai_xe = st.text_input("HỌ TÊN TÀI XẾ")
            hdv = st.text_input("HƯỚNG DẪN VIÊN")
            diem_don = st.text_input("ĐIỂM ĐÓN (Mũi Né / Tiến Thành / SGN)")
            dc_don = st.text_input("ĐỊA CHỈ ĐÓN CHI TIẾT")
            diem_tra = st.text_input("ĐIỂM TRẢ / ĐỊA CHỈ TRẢ")

        with col3:
            st.markdown("##### 💰 Doanh Thu, Giá Vốn & Sales")
            doanh_thu_vnd = st.number_input("DOANH THU VND *", min_value=0, value=0, step=50000)
            doanh_thu_usd = st.number_input("DOANH THU USD (Nếu có)", min_value=0.0, value=0.0, step=10.0)
            gia_von_ncc = st.number_input("GIÁ VỐN NCC (Chi phí trả đối tác) *", min_value=0, value=0, step=50000)
            ncc_name = st.text_input("NHÀ CUNG CẤP DỊCH VỤ (NCC)")
            sales_01 = st.text_input("NHÂN VIÊN SALES 01 phụ trách *", value="Như")
            doi_tac = st.text_input("ĐỐI TÁC / ĐẠI LÝ ĐẶT")
            phuong_thuc_tt = st.selectbox("PHƯƠNG THỨC TT", ["HDV thu khách", "TX thu khách", "Chuyển khoản", "Công nợ"])
            hh_rate = st.selectbox("TỶ LỆ HOA HỒNG TRÍCH THƯỞNG", ["10%", "5%", "0%"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Ghi Nhận Nhật Ký & Tự Động Phân Bổ Kế Toán"):
            if tuyen and sales_01:
                # Thuật toán tự động tính toán chi tiết tài chính theo cấu trúc file Excel của bạn
                loi_nhuan_gop = doanh_thu_vnd - gia_von_ncc
                hh_5 = loi_nhuan_gop * 0.05 if hh_rate == "5%" and loi_nhuan_gop > 0 else 0
                hh_10 = loi_nhuan_gop * 0.10 if hh_rate == "10%" and loi_nhuan_gop > 0 else 0
                
                new_record = {
                    "CODE": code, "NGÀY": ngay, "GIỜ": gio, "DỊCH VỤ": dich_vu, "LOẠI": loai, "TUYẾN": tuyen,
                    "XE": loai_xe, "LƯU Ý XE": luu_y_xe, "BIỂN SỐ": bien_so, "TÀI XẾ": tai_xe, "HDV": hdv,
                    "SỐ PAX": so_pax, "ĐỐI TÁC": doi_tac, "VAT": "", "TÊN KHÁCH": ten_khach, "ĐIỂM ĐÓN": diem_don,
                    "Đ/C ĐÓN": dc_don, "ĐIỂM TRẢ": diem_tra, "Đ/C TRẢ": "", "DOANH THU USD": doanh_thu_usd,
                    "DOANH THU VND": doanh_thu_vnd, "PHƯƠNG THỨC TT": phuong_thuc_tt, "Ngày TT": "", "CỌC": 0,
                    "TX THU": 0, "GIÁ VỐN NCC": gia_von_ncc, "NCC": ncc_name, "SALES 01": sales_01, "SALES 02": "",
                    "LƯU Ý": "", "CHI PHÍ": gia_von_ncc, "LỢI NHUẬN GỘP": loi_nhuan_gop, "HH sale 5%": hh_5, "HH sale 10%": hh_10
                }
                
                # Nối dòng dữ liệu mới và thực hiện lưu vĩnh viễn vào file cứng
                st.session_state.master_df = pd.concat([st.session_state.master_df, pd.DataFrame([new_record])], ignore_index=True)
                st.session_state.master_df.to_csv(DATABASE_FILE, index=False, encoding='utf-8-sig')
                
                st.success(f"✔️ Đã lưu thành công Tour {code} vào Database hệ thống tổng hợp!")
                st.rerun()

    st.write("### 📜 Dữ liệu 5 bản ghi vừa nhập gần nhất trên hệ thống")
    if not st.session_state.master_df.empty:
        st.dataframe(st.session_state.master_df.tail(5), use_container_width=True)

# ==========================================
# --- PHÂN HỆ 2: BẢNG TỔNG HỢP MASTER LOG ---
# ==========================================
elif menu == "🗂️ 2. Bảng Tổng Hợp Dữ Liệu Master Log":
    st.subheader("🗂️ Phân hệ tổng hợp dữ liệu chi tiết toàn hệ thống")
    st.caption("Bao gồm: Mã Tour, Loại hình Tour, Tuyến xe, Tài xế, Khách hàng và Nhân viên Sales phụ trách")
    
    df_master = st.session_state.master_df.copy()
    
    if not df_master.empty:
        # Khung công cụ tìm kiếm lọc thông tin siêu nhanh dữ liệu đa chiều
        st.markdown("##### 🔍 Bộ lọc tìm kiếm nhanh đa năng")
        f1, f2, f3 = st.columns(3)
        with f1: s_tuyen = st.text_input("Lọc theo Tuyến xe / Tên Tour:")
        with f2: s_sales = st.text_input("Lọc theo Nhân viên Sales (01):")
        with f3: s_txe = st.text_input("Lọc theo Tên Tài xế điều phối:")
        
        if s_tuyen:
            df_master = df_master[df_master["TUYẾN"].str.contains(s_tuyen, case=False, na=False)]
        if s_sales:
            df_master = df_master[df_master["SALES 01"].str.contains(s_sales, case=False, na=False)]
        if s_txe:
            df_master = df_master[df_master["TÀI XẾ"].str.contains(s_txe, case=False, na=False)]
            
        st.dataframe(df_master, use_container_width=True)
        
        # Nút Export một chạm xuất dữ liệu ra file Excel
        csv_bytes = df_master.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải Toàn Bộ Nhật Ký Master Log Về Máy (File Excel)",
            data=csv_bytes,
            file_name=f"Master_Log_Tour_PhanThiet_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("Chưa có dữ liệu vận hành. Vui lòng quay lại Phân hệ 1 để nhập dòng đơn đầu tiên.")

# ==========================================
# --- PHÂN HỆ 3: TRUNG TÂM BÁO CÁO TÀI CHÍNH ---
# ==========================================
elif menu == "📊 3. Báo Cáo Tài Chính Biến Động (P&L)":
    st.subheader("📊 Báo cáo kết quả hoạt động kinh doanh, Phân tích Doanh thu - Giá vốn - Hoa hồng")
    df_calc = st.session_state.master_df.copy()
    
    if not df_calc.empty:
        # Ép kiểu dữ liệu thời gian phục vụ lọc báo cáo theo Ngày/Tháng/Năm
        df_calc["NGÀY"] = pd.to_datetime(df_calc["NGÀY"], errors='coerce').dt.date
        df_calc["Tháng"] = pd.to_datetime(df_calc["NGÀY"], errors='coerce').dt.to_period("M").astype(str)
        df_calc["Năm"] = pd.to_datetime(df_calc["NGÀY"], errors='coerce').dt.year
        
        # Đồng bộ hóa công thức tài chính động
        df_calc["DOANH THU VND"] = pd.to_numeric(df_calc["DOANH THU VND"], errors='coerce').fillna(0)
        df_calc["GIÁ VỐN NCC"] = pd.to_numeric(df_calc["GIÁ VỐN NCC"], errors='coerce').fillna(0)
        df_calc["LỢI NHUẬN GỘP"] = df_calc["DOANH THU VND"] - df_calc["GIÁ VỐN NCC"]
        df_calc["HH_Tổng"] = pd.to_numeric(df_calc["HH sale 5%"], errors='coerce').fillna(0) + pd.to_numeric(df_calc["HH sale 10%"], errors='coerce').fillna(0)
        df_calc["Lợi_Nhuận_Thuần"] = df_calc["LỢI NHUẬN GỘP"] - df_calc["HH_Tổng"]
        
        # --- BỘ LỌC ĐỐI SOÁT THỜI GIAN THEO ĐÚNG FILE GỐC ---
        st.markdown("##### 📅 Cấu hình thời gian trích xuất số liệu")
        filter_mode = st.radio("Phương thức gom thời gian:", ["Khoảng Ngày tự chọn", "Lọc Theo Tháng", "Lọc Theo Năm"], horizontal=True)
        
        if filter_mode == "Khoảng Ngày tự chọn":
            col_d1, col_d2 = st.columns(2)
            with col_d1: 
                start = st.date_input("Từ ngày:", datetime.date(2026, 7, 1))
            with col_d2: 
                end = st.date_input("Đến ngày:", datetime.date(2026, 12, 31))
            df_filtered = df_calc[(df_calc["NGÀY"] >= start) & (df_calc["NGÀY"] <= end)]
        elif filter_mode == "Lọc Theo Tháng":
            df_filtered = df_calc[df_calc["Tháng"] == st.selectbox("Chọn tháng báo cáo:", sorted(list(df_calc["Tháng"].dropna().unique())))]
        elif filter_mode == "Lọc Theo Năm":
            df_filtered = df_calc[df_calc["Năm"] == st.selectbox("Chọn năm báo cáo:", sorted(list(df_calc["Năm"].dropna().unique())))]
            
        # Kết xuất 3 Tab báo cáo nghiệp vụ tài chính
        tab1, tab2, tab3 = st.tabs(["🏛️ 1. Kết Quả Kinh Doanh Doanh Nghiệp (P&L)", "🚎 2. Doanh Thu - Chi Phí - Lợi Nhuận Tour", "💵 3. Báo Cáo Hoa Hồng Sales & Đại Lý"])
        
        with tab1:
            st.markdown("#### Báo cáo Lãi lỗ tổng gộp")
            r_gross = df_filtered["DOANH THU VND"].sum()
            c_ncc = df_filtered["GIÁ VỐN NCC"].sum()
            p_gross = df_filtered["LỢI NHUẬN GỘP"].sum()
            c_comm = df_filtered["HH_Tổng"].sum()
            p_net = df_filtered["Lợi_Nhuận_Thuần"].sum()
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Doanh Thu Tổng (Gross)", f"{r_gross:,.0f} VND")
            mc2.metric("Chi Phí Giá Vốn NCC", f"{c_ncc:,.0f} VND")
            mc3.metric("Tổng Chi Hoa Hồng", f"{c_comm:,.0f} VND")
            mc4.metric("Lợi Nhuận Thuần Thực Thu", f"{p_net:,.0f} VND", delta=f"{((p_net/r_gross)*100) if r_gross > 0 else 0:.1f}% ROS")
            
            p_l_display = pd.DataFrame([
                {"Chỉ tiêu tài chính": "A. DOANH THU HOẠT ĐỘNG KINH DOANH TOUR & XE", "Giá trị kết chuyển (VND)": r_gross},
                {"Chỉ tiêu tài chính": "B. CHI PHÍ GIÁ VỐN DỊCH VỤ (Trả nhà xe, land đối tác, vé)", "Giá trị kết chuyển (VND)": c_ncc},
                {"Chỉ tiêu tài chính": "C. LỢI NHUẬN GỘP CHƯA TRỪ THƯỞNG (A - B)", "Giá trị kết chuyển (VND)": p_gross},
                {"Chỉ tiêu tài chính": "D. CHI PHÍ HOA HỒNG (Chiết khấu đại lý & thưởng Sales)", "Giá trị kết chuyển (VND)": c_comm},
                {"Chỉ tiêu tài chính": "E. LỢI NHUẬN THUẦN DOANH NGHIỆP THU VỀ (C - D)", "Giá trị kết chuyển (VND)": p_net}
            ])
            st.table(p_l_display)
            
        with tab2:
            st.markdown("#### Hiệu suất tài chính phân tách cụ thể theo dòng Tour")
            if not df_filtered.empty:
                df_tour = df_filtered.groupby("TUYẾN").agg({
                    "SỐ PAX": "sum",
                    "DOANH THU VND": "sum",
                    "GIÁ VỐN NCC": "sum",
                    "LỢI NHUẬN GỘP": "sum"
                }).reset_index().rename(columns={
                    "TUYẾN": "Dòng Tour / Tuyến xe chạy",
                    "SỐ PAX": "Tổng lượng Pax",
                    "DOANH THU VND": "Doanh Thu (VND)",
                    "GIÁ VỐN NCC": "Giá Vốn Chi Trả NCC (VND)",
                    "LỢI NHUẬN GỘP": "Lợi Nhuận Gộp Tour (VND)"
                })
                st.dataframe(df_tour, use_container_width=True)
                
        with tab3:
            st.markdown("#### Báo cáo trích thưởng hoa hồng lọc theo Sales/Đại lý")
            if not df_filtered.empty:
                df_sal = df_filtered.groupby("SALES 01").agg({
                    "CODE": "count",
                    "SỐ PAX": "sum",
                    "DOANH THU VND": "sum",
                    "HH_Tổng": "sum"
                }).reset_index().rename(columns={
                    "SALES 01": "Nhân Viên Sales / Đại Lý",
                    "CODE": "Số lượng đơn chốt thành công",
                    "SỐ PAX": "Tổng lượng Pax mang về",
                    "DOANH THU VND": "Tổng doanh số chốt đơn (VND)",
                    "HH_Tổng": "Tổng tiền hoa hồng được trích (VND)"
                })
                st.dataframe(df_sal, use_container_width=True)
                st.metric("Tổng chi phí ngân sách hoa hồng kỳ này:", f"{df_sal['Tổng tiền hoa hồng được trích (VND)'].sum():,.0f} VND")
    else:
        st.info("Không có dữ liệu tài chính trong khoảng thời gian lọc.")
