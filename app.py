import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Hệ Thống Quản Lý & Kế Toán Tour Toàn Diện", layout="wide")
st.title("🏛️ HỆ THỐNG ĐIỀU HÀNH & KẾ TOÁN TOUR CÔNG TY TOÀN DIỆN")
st.caption("Bản nâng cấp Master Log: Kết hợp Nhập liệu, Điều hành xe (Ops), Quản lý hoa hồng Sales và Công nợ NCC")

# --- ĐƯỜNG DẪN TỆP LƯU TRỮ DỮ LIỆU ---
MASTER_BOOKING_FILE = "master_bookings.csv"
MASTER_OPS_FILE = "master_ops.csv"

# --- HÀM TỰ ĐỘNG LƯU TRỮ VÀ KHỞI TẠO CƠ SỞ DỮ LIỆU CHUẨN ĐÚNG THEO FILE EXCEL ---
def load_system_data():
    if os.path.exists(MASTER_BOOKING_FILE):
        df_b = pd.read_csv(MASTER_BOOKING_FILE)
        df_b["Ngày Đi"] = pd.to_datetime(df_b["Ngày Đi"]).dt.date
    else:
        # Cấu trúc dòng dữ liệu mẫu chuẩn y hệt file Excel thực tế của bạn
        df_b = pd.DataFrame([
            {
                "Mã BK": "MTG-2607001", "Ngày Đi": datetime.date(2026, 7, 1), "Giờ Đón": "04:30:00",
                "Dịch Vụ": "Tour", "Loại Hình": "Ind.", "Tuyến Đi": "Mekong Only", "Mã Xe Ghép": "XE-7C-HUNG",
                "Số Pax": 4, "Đối Tác": "Ms. An - Hoàng Ngọc", "Tên Khách": "Mr. Kaczorowski Przemyslaw",
                "Điểm Đón": "Hoàng Ngọc", "Doanh Thu USD": 0.0, "Doanh Thu VND": 7800000,
                "Phương Thức TT": "HDV thu khách", "Giá Vốn NCC": 3000000, "Nhà Cung Cấp": "Chị Hường",
                "Tên Sales": "Như", "Tỷ Lệ HH": 0.1, "Lưu Ý": "Đã nhận 240$"
            },
            {
                "Mã BK": "MTG-2607002", "Ngày Đi": datetime.date(2026, 7, 7), "Giờ Đón": "05:30:00",
                "Dịch Vụ": "Tour", "Loại Hình": "Ind.", "Tuyến Đi": "Dalat Premium", "Mã Xe Ghép": "XE-7C-DUC-ANH",
                "Số Pax": 3, "Đối Tác": "Pegas", "Tên Khách": "Tarasov Aleksandr",
                "Điểm Đón": "Bamboo Resort", "Doanh Thu USD": 270.0, "Doanh Thu VND": 7047000,
                "Phương Thức TT": "HDV thu khách", "Giá Vốn NCC": 3209000, "Nhà Cung Cấp": "Đức Anh",
                "Tên Sales": "Ân", "Tỷ Lệ HH": 0.05, "Lưu Ý": "Đã nhận cọc"
            }
        ])
    
    if os.path.exists(MASTER_OPS_FILE):
        df_o = pd.read_csv(MASTER_OPS_FILE)
    else:
        df_o = pd.DataFrame([
            {
                "Mã Xe Ghép": "XE-7C-HUNG", "Tài Xế": "Hùng", "Biển Số": "86A-X1.23", "Hướng Dẫn Viên": "Xuân Lâm", "Lưu Ý Xe": "Xe sạch sẽ"
            },
            {
                "Mã Xe Ghép": "XE-7C-DUC-ANH", "Tài Xế": "Đức Anh", "Biển Số": "86B-Y4.56", "Hướng Dẫn Viên": "Quốc Uy", "Lưu Ý Xe": "Khách VIP"
            }
        ])
    return df_b, df_o

def save_system_data(df_b, df_o):
    df_b.to_csv(MASTER_BOOKING_FILE, index=False)
    df_o.to_csv(MASTER_OPS_FILE, index=False)

# Nạp dữ liệu vào phiên làm việc online
if 'bookings' not in st.session_state or 'tour_ops' not in st.session_state:
    st.session_state.bookings, st.session_state.tour_ops = load_system_data()

# --- THANH MENU ĐIỀU HƯỚNG NGHIỆP VỤ ---
menu = st.sidebar.radio("PHÂN HỆ NGHIỆP VỤ", [
    "📥 1. Nhập Liệu Master Log Mới",
    "🎯 2. Điều Phối Điều Xe & HDV (Ops)",
    "💵 3. Kế Toán Thu Hộ & Cọc Khách",
    "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)",
    "🏦 5. Quản Lý Công Nợ Nhà Cung Cấp",
    "🗂️ 6. Bảng Tổng Hợp Dữ Liệu Toàn Diện (Master)"
])

# ==========================================
# --- PHÂN HỆ 1: NHẬP LIỆU MASTER LOG MỚI ---
# ==========================================
if menu == "📥 1. Nhập Liệu Master Log Mới":
    st.subheader("📥 Tiếp nhận dữ liệu Đơn hàng / Tour mới")
    with st.form("master_booking_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### 📝 Thông Tin Hành Trình")
            ma_bk = st.text_input("Mã Đặt Tour (CODE) *", value=f"MTG-{datetime.date.today().strftime('%y%m')}{len(st.session_state.bookings)+1:03d}")
            ngay_di = st.date_input("Ngày khởi hành *", datetime.date(2026, 7, 1))
            gio_don = st.text_input("Giờ đón khách", value="04:30:00")
            dich_vu = st.selectbox("Dịch vụ", ["Tour", "Transfer", "Vé", "Hotel", "Events"])
            loai_hinh = st.text_input("Loại hình (Ví dụ: Ind., Group, Drop-off)", value="Ind.")
            tuyen_di = st.text_input("Tuyến đường / Tên Tour *", value="Mũi Né - Bàu Trắng")
            
        with col2:
            st.markdown("##### 👤 Khách Hàng & Doanh Thu")
            ten_khach = st.text_input("Tên khách hàng / Đại diện đoàn", value="Mr. John Doe")
            so_pax = st.number_input("Số lượng khách (Số PAX) *", min_value=1, step=1, value=2)
            diem_don = st.text_input("Điểm đón khách (Khách sạn/Resort)", value="Centara Resort")
            doi_tac = st.text_input("Đối tác gửi khách / Đại lý", value="Fun&Sun")
            dt_usd = st.number_input("Doanh thu bằng USD (Nếu có)", min_value=0.0, value=0.0)
            dt_vnd = st.number_input("Doanh thu bằng VND *", min_value=0, value=1500000, step=100000)
            
        with col3:
            st.markdown("##### 💰 Chi Phí NCC & Hoa Hồng Sales")
            pt_tt = st.selectbox("Phương thức thanh toán", ["HDV thu khách", "TX thu khách", "Chuyển khoản", "Công nợ", "Tiền mặt"])
            gia_von = st.number_input("Giá vốn phải trả NCC (VND) *", min_value=0, value=900000, step=50000)
            ncc_ten = st.text_input("Tên Nhà cung cấp (NCC dịch vụ)", value="Jeep Trương")
            sales_name = st.text_input("Nhân viên Sales phụ trách *", value="Như")
            ty_le_hh = st.selectbox("Mức trích phần trăm hoa hồng Sales", [0.10, 0.05, 0.0, 0.15], format_func=lambda x: f"{x*100}%")
            ma_xe_gan = st.text_input("Gán Mã Chuyến xe ghép quản lý", value="XE-7C-HUNG")
            luru_y = st.text_area("Ghi chú đặc biệt lưu ý đơn")

        if st.form_submit_button("💾 Lưu Dữ Liệu Vào Master Log"):
            new_row = {
                "Mã BK": ma_bk, "Ngày Đi": ngay_di, "Giờ Đón": gio_don, "Dịch Vụ": dich_vu, "Loại Hình": loai_hinh,
                "Tuyến Đi": tuyen_di, "Mã Xe Ghép": ma_xe_gan, "Số Pax": so_pax, "Đối Tác": doi_tac, "Tên Khách": ten_khach,
                "Điểm Đón": diem_don, "Doanh Thu USD": dt_usd, "Doanh Thu VND": dt_vnd, "Phương Thức TT": pt_tt,
                "Giá Vốn NCC": gia_von, "Nhà Cung Cấp": ncc_ten, "Tên Sales": sales_name, "Tỷ Lệ HH": ty_le_hh, "Lưu Ý": luru_y
            }
            st.session_state.bookings = pd.concat([st.session_state.bookings, pd.DataFrame([new_row])], ignore_index=True)
            save_system_data(st.session_state.bookings, st.session_state.tour_ops)
            st.success(f"✔️ Đã ghi nhận thành công đơn hàng {ma_bk} vào tệp dữ liệu!")
            st.rerun()

    st.write("### 📜 Nhật ký Master Log hiện tại")
    st.dataframe(st.session_state.bookings, use_container_width=True)

# ==========================================
# --- PHÂN HỆ 2: ĐIỀU PHỐI ĐIỀU XE & HDV ---
# ==========================================
elif menu == "🎯 2. Gom Xe & Điều Phối Tour (Ops)":
    st.subheader("🎯 Khai báo thông tin Điều hành phương tiện & Nhân sự (Ops)")
    
    with st.form("ops_form"):
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ma_xe_ops = st.text_input("Nhập Mã Chuyến Xe Ghép điều phối *", value="XE-7C-HUNG")
            tai_xe_ten = st.text_input("Họ tên Tài xế điều hành", value="Nguyễn Văn Thanh")
            bien_so_xe = st.text_input("Biển số xe chạy tuyến", value="86A-123.45")
        with col_o2:
            hdv_ten = st.text_input("Hướng Dẫn Viên đi cùng đoàn (Nếu có)", value="Xuân Lâm")
            note_xe = st.text_input("Lưu ý đặc biệt cho nhà xe", value="Đón đúng giờ")
            
        if st.form_submit_button("💾 Khai Thác Điều Xe"):
            st.session_state.tour_ops = st.session_state.tour_ops[st.session_state.tour_ops["Mã Xe Ghép"] != ma_xe_ops]
            new_ops = {
                "Mã Xe Ghép": ma_xe_ops, "Tài Xế": tai_xe_ten, "Biển Số": bien_so_xe, "Hướng Dẫn Viên": hdv_ten, "Lưu Ý Xe": note_xe
            }
            st.session_state.tour_ops = pd.concat([st.session_state.tour_ops, pd.DataFrame([new_ops])], ignore_index=True)
            save_system_data(st.session_state.bookings, st.session_state.tour_ops)
            st.success(f"✔️ Cập nhật thành công đội ngũ vận hành cho chuyến {ma_xe_ops}!")
            st.rerun()

    st.markdown("### 📋 Danh bạ trạng thái điều phối xe Ops hiện tại")
    st.dataframe(st.session_state.tour_ops, use_container_width=True)

# ==========================================
# --- PHÂN HỆ 3: KẾ TOÁN THU HỘ & CỌC KHÁCH ---
# ==========================================
elif menu == "💵 3. Kế Toán Thu Hộ & Cọc Khách":
    st.subheader("💵 Quản lý dòng tiền thu hộ từ Tài xế & Hướng dẫn viên")
    df_bk = st.session_state.bookings.copy()
    
    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.info("🚎 Dòng tiền Tài xế chịu trách nhiệm thu (TX thu khách)")
        df_tx = df_bk[df_bk["Phương Thức TT"] == "TX thu khách"]
        if not df_tx.empty:
            st.dataframe(df_tx[["Mã BK", "Tên Khách", "Doanh Thu VND", "Nhà Cung Cấp"]], use_container_width=True)
            st.metric("Tổng Quỹ Tài Xế Cần Nộp Về", f"{df_tx['Doanh Thu VND'].sum():,} VND")
        else:
            st.caption("Không có dòng tiền thu hộ của tài xế.")
            
    with c_t2:
        st.success("👨‍💼 Dòng tiền Hướng dẫn viên chịu trách nhiệm thu (HDV thu khách)")
        df_hdv = df_bk[df_bk["Phương Thức TT"] == "HDV thu khách"]
        if not df_hdv.empty:
            st.dataframe(df_hdv[["Mã BK", "Tên Khách", "Doanh Thu VND", "Lưu Ý"]], use_container_width=True)
            st.metric("Tổng Quỹ HDV Cần Nộp Về", f"{df_hdv['Doanh Thu VND'].sum():,} VND")
        else:
            st.caption("Không có dòng tiền thu hộ của HDV.")

# ==========================================
# --- PHÂN HỆ 4: TRUNG TÂM BÁO CÁO TÀI CHÍNH ---
# ==========================================elif menu == "📊 4. Trung Tâm Báo Cáo Tài Chính (P&L)":
    st.subheader("📊 Trung Tâm Phân Tích Kết Quả Kinh Doanh & Hiệu Suất Tài Chính")
    
    # Tạo bản sao dữ liệu tránh ảnh hưởng đến state gốc
    df_b = st.session_state.bookings.copy()
    
    # Chuẩn hóa định dạng ngày tháng để bộ lọc thời gian hoạt động chính xác
    df_b["Ngày"] = pd.to_datetime(df_b["Ngày"]).dt.date
    df_b["Tháng"] = pd.to_datetime(df_b["Ngày"]).dt.to_period("M").astype(str)
    df_b["Năm"] = pd.to_datetime(df_b["Ngày"]).dt.year
    
    # --- BỘ LỌC THỜI GIAN THEO ĐÚNG TIÊU CHUẨN KẾ TOÁN ---
    st.markdown("##### 📅 Cấu hình bộ lọc thời gian đối soát")
    filter_mode = st.radio("Lọc báo cáo tài chính theo:", ["Khoảng Ngày cụ thể", "Tháng", "Năm"], horizontal=True)
    
    if filter_mode == "Khoảng Ngày cụ thể":
        d1, d2 = st.columns(2)
        with d1: 
            start = st.date_input("Từ ngày:", datetime.date(2026, 7, 1))
        with d2: 
            end = st.date_input("Đến ngày:", datetime.date(2026, 12, 31))
        df_filtered = df_b[(df_b["Ngày"] >= start) & (df_b["Ngày"] <= end)]
        
    elif filter_mode == "Tháng":
        m_list = sorted(list(df_b["Tháng"].unique()))
        m_select = st.selectbox("Chọn tháng tài chính:", m_list if m_list else [str(datetime.date.today())[:7]])
        df_filtered = df_b[df_b["Tháng"] == m_select]
        
    elif filter_mode == "Năm":
        y_list = sorted(list(df_b["Năm"].unique()))
        y_select = st.selectbox("Chọn năm tài chính:", y_list if y_list else [datetime.date.today().year])
        df_filtered = df_b[df_b["Năm"] == y_select]
        
    # --- TÍNH TOÁN CÁC CHỈ SỐ THEO ĐÚNG CỘT DỮ LIỆU THỰC TẾ ---
    # Đồng bộ hóa công thức tính dựa trên Doanh Thu VND, Giá Vốn NCC và các khoản hoa hồng trích chi
    df_filtered["Lợi Nhuận Gộp Thực"] = df_filtered["Doanh Thu VND"] - df_filtered["Giá Vốn NCC"]
    
    # Tính tổng hoa hồng trích thưởng (bao gồm cả mức 5% và 10% nếu có phát sinh)
    df_filtered["Tổng Hoa Hồng Chi"] = df_filtered["HH sale 5%"].fillna(0) + df_filtered["HH sale 10%"].fillna(0)
    df_filtered["Lợi Nhuận Thuần Thực"] = df_filtered["Lợi Nhuận Gộp Thực"] - df_filtered["Tổng Hoa Hồng Chi"]
    
    total_rev = df_filtered["Doanh Thu VND"].sum()
    total_cost = df_filtered["Giá Vốn NCC"].sum()
    total_g_profit = df_filtered["Lợi Nhuận Gộp Thực"].sum()
    total_com = df_filtered["Tổng Hoa Hồng Chi"].sum()
    total_net_profit = df_filtered["Lợi Nhuận Thuần Thực"].sum()
    
    # Thiết lập các Tab báo cáo chi tiết trực quan
    t1, t2, t3 = st.tabs(["🏛️ Báo Cáo Lãi Lỗ Doanh Nghiệp (P&L)", "🚎 Doanh Thu - Chi Phí Tour Chi Tiết", "💵 Kiểm Soát Hoa Hồng Sales"])
    
    with t1:
        st.markdown("#### Báo cáo Lợi Nhuận Doanh Nghiệp")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("1. TỔNG DOANH THU (GROSS)", f"{total_rev:,.0f} VND")
        mc2.metric("2. CHI PHÍ GIÁ VỐN NCC", f"{total_cost:,.0f} VND")
        mc3.metric("3. TỔNG CHI HOA HỒNG", f"{total_com:,.0f} VND")
        mc4.metric("4. LỢI NHUẬN THUẦN", f"{total_net_profit:,.0f} VND", delta=f"{((total_net_profit/total_rev)*100) if total_rev > 0 else 0:.1f}% ROS")
        
        p_and_l = pd.DataFrame([
            {"Khoản mục kế toán": "A. TỔNG DOANH THU HOẠT ĐỘNG KINH DOANH", "Số tiền (VND)": total_rev},
            {"Khoản mục kế toán": "B. CHI PHÍ GIÁ VỐN DỊCH VỤ (Trả Nhà xe, Vé, Land tour)", "Số tiền (VND)": total_cost},
            {"Khoản mục kế toán": "C. LỢI NHUẬN GỘP KINH DOANH (A - B)", "Số tiền (VND)": total_g_profit},
            {"Khoản mục kế toán": "D. CHI PHÍ BÁN HÀNG (Hoa hồng trích thưởng cho Sales)", "Số tiền (VND)": total_com},
            {"Khoản mục kế toán": "E. LỢI NHUẬN THUẦN TRƯỚC THUẾ (C - D)", "Số tiền (VND)": total_net_profit}
        ])
        st.table(p_and_l)
        
    with t2:
        st.markdown("#### Bảng Hiệu Suất Kinh Doanh Từng Tuyến Tour / Mã Chuyến Xe Ghép")
        if not df_filtered.empty:
            # Nhóm dữ liệu theo Tuyến để phân tích hiệu năng lãi/lỗ từng dòng tour
            df_tour_perf = df_filtered.groupby("TUYẾN").agg({
                "SỐ PAX": "sum",
                "Doanh Thu VND": "sum",
                "Giá Vốn NCC": "sum",
                "Lợi Nhuận Gộp Thực": "sum"
            }).reset_index().rename(columns={
                "TUYẾN": "Tuyến Đi / Tên Dịch Vụ Tour",
                "SỐ PAX": "Tổng Số Khách (Pax)",
                "Doanh Thu VND": "Tổng Doanh Thu (VND)",
                "Giá Vốn NCC": "Tổng Chi Phí NCC (VND)",
                "Lợi Nhuận Gộp Thực": "Lợi Nhuận Gộp Tour (VND)"
            })
            st.dataframe(df_tour_perf, use_container_width=True)
        else:
            st.info("Không có dữ liệu điều hành trong khoảng thời gian được lọc.")
            
    with t3:
        st.markdown("#### Báo Cáo Trích Chi Hoa Hồng Sales & Đại Lý Đối Tác")
        if not df_filtered.empty:
            # Ưu tiên lấy cột Nhân viên bán chính (SALES 01) xử lý số liệu hoa hồng
            df_sales_perf = df_filtered.groupby("SALES 01").agg({
                "CODE": "count",
                "SỐ PAX": "sum",
                "Doanh Thu VND": "sum",
                "Tổng Hoa Hồng Chi": "sum"
            }).reset_index().rename(columns={
                "SALES 01": "Nhân Viên Sales / Đối Tác",
                "CODE": "Số Đơn Hàng Chốt",
                "SỐ PAX": "Tổng Số Pax Mang Về",
                "Doanh Thu VND": "Doanh Số Mang Về (VND)",
                "Tổng Hoa Hồng Chi": "Tổng Hoa Hồng Nhận Kỳ Này (VND)"
            })
            st.dataframe(df_sales_perf, use_container_width=True)
            st.metric("Tổng Chi Phí Trích Chi Hoa Hồng Kỳ Này", f"{total_com:,.0f} VND")
        else:
            st.info("Chưa phát sinh dữ liệu trích chi hoa hồng trong kỳ đối soát này.")
