import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Hệ Thống Điều Hành & Tài Chính Tour Ghép", layout="wide")
st.title("🏛️ HỆ THỐNG ĐIỀU HÀNH & TÀI CHÍNH TOUR GHÉP TOÀN DIỆN")
st.caption("Giao diện vận hành Cloud: Quản lý khách ghép, Điều hành Ops, Tính hoa hồng & Quản lý công nợ Nhà cung cấp")

# --- KHỞI TẠO CƠ SỞ DỮ LIỆU MẪU BAN ĐẦU ---
if 'tours' not in st.session_state:
    st.session_state.tours = ["Hà Nội - Hạ Long 2N1Đ", "Sài Gòn - Phú Quốc 3N2Đ", "Đà Nẵng - Hội An 4N3Đ"]

if 'bookings' not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {
            "Mã BK": "BK001", "Tour": "Hà Nội - Hạ Long 2N1Đ", "Ngày Đi": datetime.date(2026, 11, 5), 
            "Khách": "Anh Hùng", "Số Khách": 4, "Điểm Đón": "Nhà Hát Lớn", "Mã Xe Ghép": "XE-HALONG-0511", 
            "Nguồn Khách": "Sales Nội Bộ", "Người Bán/Đối Tác": "Nguyễn Văn Tuấn (Sales)", "Mức HH/Khách": 50000,
            "Giá Bán/Khách": 1500000, "Hình Thức HH": "Công ty chi trả sau", "Trạng Thái Thu": "Đã thu đủ"
        },
        {
            "Mã BK": "BK002", "Tour": "Hà Nội - Hạ Long 2N1Đ", "Ngày Đi": datetime.date(2026, 11, 5), 
            "Khách": "Chị Lan", "Số Khách": 6, "Điểm Đón": "12 Chùa Bộc", "Mã Xe Ghép": "XE-HALONG-0511", 
            "Nguồn Khách": "Đối Tác Bên Ngoài", "Người Bán/Đối Tác": "Đại lý Tourgiare (Anh Minh)", "Mức HH/Khách": 150000,
            "Giá Bán/Khách": 1500000, "Hình Thức HH": "Trừ thẳng khi thanh toán (Thu hộ)", "Trạng Thái Thu": "Đã thu đủ"
        },
        {
            "Mã BK": "BK003", "Tour": "Hà Nội - Hạ Long 2N1Đ", "Ngày Đi": datetime.date(2026, 11, 5), 
            "Khách": "Cô Mai", "Số Khách": 2, "Điểm Đón": "KS Daewoo", "Mã Xe Ghép": "XE-HALONG-0511", 
            "Nguồn Khách": "Đối Tác Bên Ngoài", "Người Bán/Đối Tác": "Đại lý Flamingo", "Mức HH/Khách": 100000,
            "Giá Bán/Khách": 1400000, "Hình Thức HH": "Công ty chi trả sau", "Trạng Thái Thu": "Đã thu đủ"
        }
    ])

if 'tour_ops' not in st.session_state:
    st.session_state.tour_ops = pd.DataFrame([
        {
            "Mã Xe Ghép": "XE-HALONG-0511", 
            "Tài Xế": "Lê Hoàng Nam", "Biển Số": "29B-456.78", "Chi Phí Xe (VND)": 2000000, 
            "Hướng Dẫn Viên": "Trần Văn Tâm", "Chi Phí HDV (VND)": 800000,
            "Nhà Hàng": "Hồng Hạnh Hạ Long", "Khách Sạn": "Paradise Sails", "Vé Tham Quan": "Vé Tuyến 2",
            "Chi Phí Tour/Khách (VND)": 600000, "Ghi Chú": "Nhóm BK002 có 1 khách dị ứng hải sản."
        }
    ])

# --- THANH MENU ĐIỀU HƯỚNG ---
menu = st.sidebar.radio("PHÂN HỆ NGHIỆP VỤ", [
    "📥 1. Nhập Đặt Tour Mới",
    "🎯 2. Gom Xe & Điều Phối Tour (Ops)",
    "💵 3. Quyết Toán Hoa Hồng Sales & Đại Lý",
    "📊 4. Báo Cáo Doanh Thu Lợi Nhuận Đối Tác",
    "🏦 5. Quản Lý Công Nợ Nhà Cung Cấp"
])

# ==========================================
# --- PHÂN HỆ 1: NHẬP ĐẶT TOUR MỚI ---
# ==========================================
if menu == "📥 1. Nhập Đặt Tour Mới":
    st.subheader("📥 Tiếp nhận dữ liệu đặt tour lẻ / Đoàn ghép lẻ")
    with st.form("main_booking_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            tour = st.selectbox("Chọn Tour du lịch", st.session_state.tours)
            ngay_di = st.date_input("Ngày khởi hành", datetime.date(2026, 11, 5))
            ten_khach = st.text_input("Tên khách / Đại diện nhóm *")
            so_khach = st.number_input("Số lượng khách (Pax) *", min_value=1, step=1, value=2)
            diem_don = st.text_input("Địa điểm đón khách chi tiết")
        with col2:
            gia_ban = st.number_input("Giá bán/Khách (VND)", min_value=0, value=1500000, step=50000)
            nguon_khach = st.selectbox("Nguồn khách hàng *", ["Sales Nội Bộ", "Đối Tác Bên Ngoài"])
            nguoi_ban = st.text_input("Tên Nhân viên Sales / Tên Đại lý bên ngoài *")
            ma_xe_ban_dau = st.text_input("Gán mã chuyến xe ghép (Nếu có)", value="XE-HALONG-0511")
        with col3:
            hh_pax = st.number_input("Mức hoa hồng chi trả / 1 Khách (VND)", min_value=0, value=100000, step=10000)
            hinh_thuc_hh = st.selectbox("Hình thức xử lý hoa hồng *", ["Công ty chi trả sau", "Trừ thẳng khi thanh toán (Thu hộ)"])
            trang_thai_thu = st.selectbox("Trạng thái thu tiền gốc", ["Đã thu đủ", "Chờ chuyển tiền"])
            
        if st.form_submit_button("💾 Lưu Thông Tin Đặt Tour"):
            if ten_khach and nguoi_ban:
                ma_bk = f"BK{len(st.session_state.bookings) + 101}"
                new_bk = {
                    "Mã BK": ma_bk, "Tour": tour, "Ngày Đi": ngay_di, "Khách": ten_khach, "Số Khách": so_khach, 
                    "Điểm Đón": diem_don, "Mã Xe Ghép": ma_xe_ban_dau, "Nguồn Khách": nguon_khach, 
                    "Người Bán/Đối Tác": nguoi_ban, "Mức HH/Khách": hh_pax, "Giá Bán/Khách": gia_ban, 
                    "Hình Thức HH": hinh_thuc_hh, "Trạng Thái Thu": trang_thai_thu
                }
                st.session_state.bookings = pd.concat([st.session_state.bookings, pd.DataFrame([new_bk])], ignore_index=True)
                st.success(f"✔️ Đã lưu thành công Booking {ma_bk} vào hệ thống!")
                st.rerun()
                
    st.write("### 📜 Toàn bộ danh sách booking hiện tại trên hệ thống")
    st.dataframe(st.session_state.bookings, use_container_width=True)

# ==========================================
# --- PHÂN HỆ 2: GOM XE & ĐIỀU PHỐI (OPS) ---
# ==========================================
elif menu == "🎯 2. Gom Xe & Điều Phối Tour (Ops)":
    st.subheader("🎯 Quản lý Điều Hành: Gộp khách lẻ vào xe & Khai báo chi phí dịch vụ")
    with st.expander("🔀 Gán hoặc Thay đổi chuyến xe ghép nhanh cho Khách lẻ"):
        with st.form("quick_assign_form"):
            bk_select = st.selectbox("Chọn mã Booking lẻ cần xếp xe", st.session_state.bookings["Mã BK"].tolist())
            ma_xe_nhap = st.text_input("Nhập Mã Xe Ghép / Mã Chuyến đi")
            if st.form_submit_button("Xác nhận gán xe nhanh"):
                st.session_state.bookings.loc[st.session_state.bookings["Mã BK"] == bk_select, "Mã Xe Ghép"] = ma_xe_nhap
                st.success(f"Đã chuyển khách hàng {bk_select} vào xe {ma_xe_nhap}!")
                st.rerun()

    list_chuyen = list(set(st.session_state.bookings["Mã Xe Ghép"].tolist()))
    list_chuyen = [x for x in list_chuyen if pd.notna(x) and x != "Chưa xếp xe"]
    
    if list_chuyen:
        chuyen_chon = st.selectbox("🔍 Chọn mã Chuyến xe ghép để thiết lập Điều Tour & Xe:", list_chuyen)
        khach_thuoc_chuyen = st.session_state.bookings[st.session_state.bookings["Mã Xe Ghép"] == chuyen_chon]
        tong_pax = khach_thuoc_chuyen["Số Khách"].sum()
        st.info(f"📊 Xe ghép {chuyen_chon} hiện đang có {tong_pax} khách.")
        
        current_op = st.session_state.tour_ops[st.session_state.tour_ops["Mã Xe Ghép"] == chuyen_chon]
        
        with st.form("ops_main_form"):
            col_o1, col_o2 = st.columns(2)
            with col_o1:
                st.markdown("##### 🚎 Chi Phí Vận Chuyển Cố Định")
                tai_xe = st.text_input("Họ tên Tài xế", value=str(current_op["Tài Xế"].values[0]) if not current_op.empty else "")
                bien_so = st.text_input("Biển số xe", value=str(current_op["Biển Số"].values[0]) if not current_op.empty else "")
                cost_xe = st.number_input("Giá thuê xe trọn gói chuyến (VND) *", min_value=0, value=int(current_op["Chi Phí Xe (VND)"].values[0]) if not current_op.empty else 2000000)
            with col_o2:
                st.markdown("##### 🏨 Chi Phí Dịch Vụ Tour & Nhân Sự")
                hdv = st.text_input("Hướng Dẫn Viên", value=str(current_op["Hướng Dẫn Viên"].values[0]) if not current_op.empty else "")
                cost_hdv = st.number_input("Tiền công tác phí HDV (VND) *", min_value=0, value=int(current_op["Chi Phí HDV (VND)"].values[0]) if not current_op.empty else 800000)
                n_hang = st.text_input("Nhà hàng ăn uống", value=str(current_op["Nhà Hàng"].values[0]) if not current_op.empty else "")
                k_san = st.text_input("Khách sạn / Nhà Tàu", value=str(current_op["Khách Sạn"].values[0]) if not current_op.empty else "")
                v_tq = st.text_input("Vé thắng cảnh / Điểm tham quan", value=str(current_op["Vé Tham Quan"].values[0]) if not current_op.empty else "")
                cost_tour_pax = st.number_input("Chi phí dịch vụ tính trên ĐẦU NGƯỜI", min_value=0, value=int(current_op["Chi Phí Tour/Khách (VND)"].values[0]) if not current_op.empty else 600000)
            ghi_chu_ops = st.text_area("Yêu cầu đặc biệt cho nhà xe/hướng dẫn viên", value=str(current_op["Ghi Chú"].values[0]) if not current_op.empty else "")
            
            if st.form_submit_button("💾 Cập Nhật Bảng Điều Hành Tour"):
                st.session_state.tour_ops = st.session_state.tour_ops[st.session_state.tour_ops["Mã Xe Ghép"] != chuyen_chon]
                new_op_data = {
                    "Mã Xe Ghép": chuyen_chon, "Tài Xế": tai_xe, "Biển Số": bien_so, "Chi Phí Xe (VND)": cost_xe,
                    "Hướng Dẫn Viên": hdv, "Chi Phí HDV (VND)": cost_hdv, "Nhà Hàng": n_hang, "Khách Sạn": k_san,
                    "Vé Tham Quan": v_tq, "Chi Phí Tour/Khách (VND)": cost_tour_pax, "Ghi Chú": ghi_chu_ops
                }
                st.session_state.tour_ops = pd.concat([st.session_state.tour_ops, pd.DataFrame([new_op_data])], ignore_index=True)
                st.success(f"Cập nhật thành công thông tin Ops cho tuyến xe {chuyen_chon}!")
                st.rerun()

        st.markdown("### 📋 Danh sách điều hành các tuyến xe")
        st.dataframe(st.session_state.tour_ops, use_container_width=True)
    else:
        st.warning("Hiện tại chưa có Booking nào được gán mã xe ghép.")

# ==========================================
# --- PHÂN HỆ 3: QUYẾT TOÁN HOA HỒNG ---
# ==========================================
elif menu == "💵 3. Quyết Toán Hoa Hồng Sales & Đại Lý":st.subheader("💵 Phân hệ kiểm soát và tính toán hoa hồng thực chi")
df_bk = st.session_state.bookings.copy()
df_bk["Tổng Doanh Thu"] = df_bk["Số Khách"] * df_bk["Giá Bán/Khách"]
df_bk["Tổng Hoa Hồng"] = df_bk["Số Khách"] * df_bk["Mức HH/Khách"]
st.markdown("##### 🔍 Chi tiết nghĩa vụ hoa hồng theo phương thức xử lý")
col_t1, col_t2 = st.columns(2)
with col_t1:
st.info("🔹 Loại 1: Công ty chi trả sau")
df_tra_sau = df_bk[df_bk["Hình Thức HH"] == "Công ty chi trả sau"]
if not df_tra_sau.empty:
st.dataframe(df_tra_sau[["Mã BK", "Người Bán/Đối Tác", "Số Khách", "Tổng Hoa Hồng", "Trạng Thái Thu"]], use_container_width=True)
st.metric("Tổng Hoa Hồng Cần Trả Sau", f"{df_tra_sau['Tổng Hoa Hồng'].sum():,} VND")
else:
st.caption("Chưa có dữ liệu hoa hồng chi trả sau.")
with col_t2:
st.success("🔹 Loại 2: Trừ thẳng khi thanh toán (Thu hộ)")
df_tru_thang = df_bk[df_bk["Hình Thức HH"] == "Trừ thẳng khi thanh toán (Thu hộ)"]
if not df_tru_thang.empty:
st.dataframe(df_tru_thang[["Mã BK", "Người Bán/Đối Tác", "Số Khách", "Tổng Hoa Hồng", "Tổng Doanh Thu"]], use_container_width=True)
st.metric("Tổng Số Tiền Thực Thu Hộ", f"{(df_tru_thang['Tổng Doanh Thu'].sum() - df_tru_thang['Tổng Hoa Hồng'].sum()):,} VND")
else:
st.caption("Chưa có dữ liệu đại lý trừ thẳng hoa hồng.")

==========================================


--- PHÂN HỆ 4: BÁO CÁO DOANH THU & LỢI NHUẬN ---


==========================================

elif menu == "📊 4. Báo Cáo Doanh Thu Lợi Nhuận Đối Tác":
st.subheader("📊 Báo cáo kết quả kinh doanh gộp (P&L) theo từng mã xe ghép")
list_chuyen = list(set(st.session_state.bookings["Mã Xe Ghép"].tolist()))
for chuyen in list_chuyen:
if pd.isna(chuyen) or chuyen == "Chưa xếp xe":
continue
st.markdown(f"#### 🚎 BÁO CÁO TOÁN CHUYẾN: {chuyen}")
df_bk_chuyen = st.session_state.bookings[st.session_state.bookings["Mã Xe Ghép"] == chuyen]
df_ops_chuyen = st.session_state.tour_ops[st.session_state.tour_ops["Mã Xe Ghép"] == chuyen]
tong_pax = df_bk_chuyen["Số Khách"].sum()
revenue = (df_bk_chuyen["Số Khách"] * df_bk_chuyen["Giá Bán/Khách"]).sum()
total_hh = (df_bk_chuyen["Số Khách"] * df_bk_chuyen["Mức HH/Khách"]).sum()
# Kiểm tra an toàn để tránh lỗi sập phần mềm khi Ops chưa cập nhật thông tin
if not df_ops_chuyen.empty:
cost_xe_co_dinh = int(df_ops_chuyen["Chi Phí Xe (VND)"].values[0]) + int(df_ops_chuyen["Chi Phí HDV (VND)"].values[0])
cost_bien_doi_pax = tong_pax * int(df_ops_chuyen["Chi Phí Tour/Khách (VND)"].values[0])
total_ops_cost = cost_xe_co_dinh + cost_bien_doi_pax
st.markdown(f"""

Tài xế: {df_ops_chuyen['Tài Xế'].values[0]} ({df_ops_chuyen['Biển Số'].values[0]}) | HDV: {df_ops_chuyen['Hướng Dẫn Viên'].values[0]}
Nhà hàng: {df_ops_chuyen['Nhà Hàng'].values[0]} | Khách sạn: {df_ops_chuyen['Khách Sạn'].values[0]} | Ghi chú: {df_ops_chuyen['Ghi Chú'].values[0]}

""", unsafe_allow_html=True)
else:
total_ops_cost = 0
st.warning(f"Chuyến xe {chuyen} chưa được khai báo chi phí vận hành bên Phân hệ 2.")
profit = revenue - total_hh - total_ops_cost
c1, c2, c3, c4 = st.columns(4)
c1.metric("Tổng thu khách lẻ (Gross)", f"{revenue:,} VND")
c2.metric("Chi phí Hoa hồng", f"{total_hh:,} VND")
c3.metric("Chi phí Vận hành (Ops)", f"{total_ops_cost:,} VND")
c4.metric("Lợi nhuận gộp chuyến", f"{profit:,} VND", delta=f"{((profit/revenue)*100) if revenue > 0 else 0:.1f}% Tỷ suất")
st.markdown("---")

==========================================


--- PHÂN HỆ 5: QUẢN LÝ CÔNG NỢ NHÀ CUNG CẤP ---


==========================================

elif menu == "🏦 5. Quản Lý Công Nợ Nhà Cung Cấp":
st.subheader("🏦 Bảng phân rã & Đối soát công nợ các dịch vụ cấu thành Tour")
df_ops = st.session_state.tour_ops.copy()
if not df_ops.empty:
records_debt = []
for index, row in df_ops.iterrows():
chuyen = row["Mã Xe Ghép"]
df_bk_chuyen = st.session_state.bookings[st.session_state.bookings["Mã Xe Ghép"] == chuyen]
tong_pax = df_bk_chuyen["Số Khách"].sum()
if row["Tài Xế"]:
records_debt.append({"Nhà Cung Cấp": f"Đội xe {row['Tài Xế']} ({row['Biển Số']})", "Nội Dung": f"Thuê xe tuyến {chuyen}", "Số Tiền Phải Trả": row["Chi Phí Xe (VND)"], "Trạng Thái": "Chưa thanh toán"})
if row["Hướng Dẫn Viên"]:
records_debt.append({"Nhà Cung Cấp": f"HDV {row['Hướng Dẫn Viên']}", "Nội Dung": f"Công tác phí {chuyen}", "Số Tiền Phải Trả": row["Chi Phí HDV (VND)"], "Trạng Thái": "Chưa thanh toán"})
if row["Nhà Hàng"]:
records_debt.append({"Nhà Cung Cấp": row["Nhà Hàng"], "Nội Dung": f"Suất ăn ghép xe {chuyen}", "Số Tiền Phải Trả": row["Chi Phí Tour/Khách (VND)"] * tong_pax, "Trạng Thái": "Chưa thanh toán"})
if records_debt:
df_debt_final = pd.DataFrame(records_debt)
st.dataframe(df_debt_final, use_container_width=True)
st.metric("Tổng Công Nợ Phải Trả Nhà Cung Cấp (Tạm tính)", f"{df_debt_final['Số Tiền Phải Trả'].sum():,} VND")
else:
st.info("Chưa phát sinh công nợ phải trả nhà cung cấp.")
else:
st.info("Chưa có dữ liệu vận hành từ điều hành Tour (Ops) để tổng hợp công nợ.")
