from itertools import combinations
import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 CHÔNG VỢ HÀI ĐẾN TỪ CHÂU ÂU _ TRẦN TRUNG HIẾU ")

st.write(
    "Ứng dụng hỗ trợ tính tiền lãi gửi tiết kiệm theo "
    "**lãi đơn** và **lãi kép**."
)

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📌 Nhập thông tin gửi tiết kiệm")

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100000000.0,
    step=1000000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn gửi (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1
)

hinh_thuc_gui = st.selectbox(
    "Chọn phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh_lai = st.selectbox(
    "Chọn hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# TÍNH TOÁN
# =========================
if st.button("💵 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif lai_suat <= 0:
        st.error("Vui lòng nhập lãi suất lớn hơn 0.")

    else:
        # Chuyển lãi suất năm sang dạng thập phân
        lai_suat_nam = lai_suat / 100

        # ---------------------------------
        # 1. XÁC ĐỊNH KỲ LÃNH LÃI
        # ---------------------------------
        if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
            so_thang_moi_ky = 1

        elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
            so_thang_moi_ky = 3

        else:
            # Cuối kỳ = toàn bộ kỳ hạn
            so_thang_moi_ky = ky_han

        # ---------------------------------
        # 2. LÃI ĐƠN
        # ---------------------------------
        if hinh_thuc_gui == "Lãi đơn":

            # Tổng tiền lãi
            tong_tien_lai = (
                so_tien_gui
                * lai_suat_nam
                * ky_han
                / 12
            )

            # Tiền lãi định kỳ
            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat_nam
                * so_thang_moi_ky
                / 12
            )

            # Nếu kỳ cuối ngắn hơn kỳ lãnh lãi
            if so_thang_moi_ky > ky_han:
                tien_lai_dinh_ky = tong_tien_lai

            tong_goc_va_lai = so_tien_gui + tong_tien_lai

        # ---------------------------------
        # 3. LÃI KÉP
        # ---------------------------------
        else:
            # Lãi suất của một kỳ ghép lãi
            lai_suat_moi_ky = (
                lai_suat_nam
                * so_thang_moi_ky
                / 12
            )

            # Số kỳ đầy đủ
            so_ky_day_du = ky_han // so_thang_moi_ky

            # Số tháng còn lại
            thang_con_lai = ky_han % so_thang_moi_ky

            # Số tiền sau các kỳ ghép lãi đầy đủ
            tong_goc_va_lai = (
                so_tien_gui
                * (1 + lai_suat_moi_ky) ** so_ky_day_du
            )

            # Tính phần tháng còn lại nếu có
            if thang_con_lai > 0:
                tong_goc_va_lai *= (
                    1
                    + lai_suat_nam
                    * thang_con_lai
                    / 12
                )

            tong_tien_lai = tong_goc_va_lai - so_tien_gui

            # Tiền lãi của kỳ đầu tiên
            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat_moi_ky
            )

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================
        st.divider()
        st.subheader("📊 Kết quả")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                dinh_dang_tien(tien_lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        with col3:
            st.metric(
                "Tổng gốc và lãi",
                dinh_dang_tien(tong_goc_va_lai)
            )

        # =========================
        # THÔNG TIN CHI TIẾT
        # =========================
        st.session_state["tong_tien_lai"] = tong_tien_lai
        st.success("✅ Tính toán thành công!")

        st.write("### 📝 Thông tin khoản gửi")

        st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat}%/năm")
        st.write(f"**Phương pháp:** {hinh_thuc_gui}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_lanh_lai}")

        # =========================
        # GIẢI THÍCH CÔNG THỨC
        # =========================
        with st.expander("📖 Xem cách tính"):

            if hinh_thuc_gui == "Lãi đơn":
                st.write("**Công thức lãi đơn:**")
                st.latex(
                    r"I = P \times r \times \frac{n}{12}"
                )

                st.write("""
                Trong đó:

                - **P**: Số tiền gửi ban đầu
                - **r**: Lãi suất năm
                - **n**: Số tháng gửi
                - **I**: Tiền lãi
                """)

            else:
                st.write("**Công thức lãi kép:**")
                st.latex(
                    r"A = P(1+r)^n"
                )

                st.write("""
                Trong đó:

                - **P**: Số tiền gửi ban đầu
                - **r**: Lãi suất của mỗi kỳ
                - **n**: Số kỳ ghép lãi
                - **A**: Tổng số tiền sau khi ghép lãi
                """)

# =========================
# CHÚ THÍCH
# =========================
st.divider()

st.caption(
    "Lưu ý: Kết quả mang tính tham khảo. "
    "Cách tính thực tế có thể khác tùy quy định của từng ngân hàng."
)
import streamlit as st
from datetime import date

import streamlit as st
import math
from itertools import combinations
# code phần tính lãi phía trên
# ...
# ============================================================
# 🛒 GIỎ HÀNG MỤC TIÊU
# ============================================================

st.divider()
st.header("🛒 Giỏ hàng mục tiêu")

st.write(
    "Sử dụng **tiền lãi tiết kiệm** để xem bạn có thể "
    "thực hiện được những mục tiêu nào mà không cần dùng đến tiền gốc."
)

# ============================================================
# 1. KIỂM TRA ĐÃ CÓ KẾT QUẢ TÍNH LÃI CHƯA
# ============================================================

if "tong_tien_lai" not in st.session_state:

    st.info(
        "👆 Hãy nhấn **TÍNH TIỀN LÃI** ở phía trên trước "
        "khi sử dụng Giỏ hàng mục tiêu."
    )

else:

    ngan_sach = st.session_state["tong_tien_lai"]

    # ========================================================
    # 2. HIỂN THỊ NGÂN SÁCH
    # ========================================================

    st.subheader("💰 Ngân sách từ tiền lãi")

    st.metric(
        "Tiền lãi có thể sử dụng",
        dinh_dang_tien(ngan_sach)
    )

    st.success(
        f"✨ Bạn có **{dinh_dang_tien(ngan_sach)}** tiền lãi "
        "để thực hiện các mục tiêu của mình."
    )

    # ========================================================
    # 3. DANH SÁCH MỤC TIÊU GỢI Ý
    # ========================================================

    danh_sach_muc_tieu = {

        "📱 Công nghệ": {
            "📱 Điện thoại": 25_000_000,
            "💻 Laptop": 20_000_000,
            "📱 Máy tính bảng": 15_000_000,
            "⌚ Đồng hồ thông minh": 8_000_000,
            "🎧 Tai nghe": 5_000_000
        },

        "✈️ Du lịch": {
            "🇯🇵 Du lịch Nhật Bản": 30_000_000,
            "🇰🇷 Du lịch Hàn Quốc": 25_000_000,
            "🇹🇭 Du lịch Thái Lan": 12_000_000,
            "🏖️ Du lịch Phú Quốc": 10_000_000,
            "⛰️ Du lịch Đà Lạt": 5_000_000
        },

        "🎓 Học tập": {
            "📚 Khóa học ngoại ngữ": 10_000_000,
            "🎓 Học phí một học kỳ": 20_000_000,
            "💻 Khóa học công nghệ": 8_000_000,
            "📝 Lệ phí thi chứng chỉ": 5_000_000
        },

        "🏠 Gia đình": {
            "📺 TV": 15_000_000,
            "🧊 Tủ lạnh": 12_000_000,
            "🧺 Máy giặt": 10_000_000,
            "🤖 Robot hút bụi": 8_000_000,
            "🛋️ Nội thất": 20_000_000
        },

        "🎁 Cá nhân": {
            "🏍️ Xe máy": 40_000_000,
            "📷 Máy ảnh": 20_000_000,
            "🎸 Nhạc cụ": 10_000_000,
            "👟 Mua sắm cá nhân": 5_000_000,
            "🎁 Quà tặng": 3_000_000
        }
    }

    # ========================================================
    # 4. KHỞI TẠO GIỎ HÀNG
    # ========================================================

    if "gio_hang_muc_tieu" not in st.session_state:
        st.session_state["gio_hang_muc_tieu"] = []

    # ========================================================
    # 5. THÊM MỤC TIÊU
    # ========================================================

    st.divider()
    st.subheader("🎯 Thêm mục tiêu")

    tab1, tab2 = st.tabs([
        "✨ Chọn mục tiêu",
        "✍️ Tự tạo mục tiêu"
    ])

    # ========================================================
    # TAB 1: MỤC TIÊU GỢI Ý
    # ========================================================

    with tab1:

        nhom = st.selectbox(
            "📂 Chọn nhóm mục tiêu",
            list(danh_sach_muc_tieu.keys()),
            key="nhom_muc_tieu"
        )

        muc_tieu = st.selectbox(
            "🎯 Chọn mục tiêu",
            list(danh_sach_muc_tieu[nhom].keys()),
            key="muc_tieu_co_san"
        )

        gia_mac_dinh = danh_sach_muc_tieu[nhom][muc_tieu]

        gia_muc_tieu = st.number_input(
            "💵 Giá mục tiêu (VNĐ)",
            min_value=1_000,
            value=int(gia_mac_dinh),
            step=100_000,
            format="%d",
            key="gia_muc_tieu_co_san"
        )

        st.caption(
            "Giá trên chỉ là mức gợi ý. "
            "Bạn có thể nhập lại giá thực tế."
        )

        if st.button(
            "➕ Thêm vào giỏ hàng",
            type="primary",
            use_container_width=True,
            key="them_muc_tieu_co_san"
        ):

            st.session_state["gio_hang_muc_tieu"].append({
                "ten": muc_tieu,
                "gia": gia_muc_tieu,
                "nhom": nhom
            })

            st.rerun()

    # ========================================================
    # TAB 2: TỰ TẠO MỤC TIÊU
    # ========================================================

    with tab2:

        ten_tu_tao = st.text_input(
            "🎯 Mục tiêu của bạn",
            placeholder="Ví dụ: Mua xe máy mới",
            key="ten_muc_tieu_tu_tao"
        )

        gia_tu_tao = st.number_input(
            "💵 Số tiền cần cho mục tiêu (VNĐ)",
            min_value=0,
            value=10_000_000,
            step=500_000,
            format="%d",
            key="gia_muc_tieu_tu_tao"
        )

        nhom_tu_tao = st.selectbox(
            "📂 Nhóm mục tiêu",
            [
                "📱 Công nghệ",
                "✈️ Du lịch",
                "🎓 Học tập",
                "🏠 Gia đình",
                "🎁 Cá nhân",
                "⭐ Khác"
            ],
            key="nhom_muc_tieu_tu_tao"
        )

        if st.button(
            "➕ Thêm mục tiêu của tôi",
            type="primary",
            use_container_width=True,
            key="them_muc_tieu_tu_tao"
        ):

            if ten_tu_tao.strip() == "":

                st.warning(
                    "⚠️ Vui lòng nhập tên mục tiêu."
                )

            elif gia_tu_tao <= 0:

                st.warning(
                    "⚠️ Giá mục tiêu phải lớn hơn 0."
                )

            else:

                st.session_state["gio_hang_muc_tieu"].append({
                    "ten": ten_tu_tao.strip(),
                    "gia": gia_tu_tao,
                    "nhom": nhom_tu_tao
                })

                st.rerun()

    # ========================================================
    # 6. HIỂN THỊ GIỎ HÀNG
    # ========================================================

    st.divider()
    st.subheader("🛒 Giỏ hàng của tôi")

    gio_hang = st.session_state["gio_hang_muc_tieu"]

    if len(gio_hang) == 0:

        st.info(
            "Giỏ hàng đang trống. "
            "Hãy thêm một hoặc nhiều mục tiêu."
        )

    else:

        # ====================================================
        # HIỂN THỊ TỪNG MỤC TIÊU
        # ====================================================

        for i, item in enumerate(gio_hang):

            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:

                st.markdown(
                    f"**{item['ten']}**"
                )

                st.caption(
                    item["nhom"]
                )

            with col2:

                st.markdown(
                    f"**{dinh_dang_tien(item['gia'])}**"
                )

            with col3:

                if st.button(
                    "🗑️",
                    key=f"xoa_muc_tieu_{i}"
                ):

                    st.session_state[
                        "gio_hang_muc_tieu"
                    ].pop(i)

                    st.rerun()

        # ====================================================
        # 7. TÍNH TỔNG GIÁ TRỊ GIỎ HÀNG
        # ====================================================

        tong_gia_tri_gio = sum(
            item["gia"]
            for item in gio_hang
        )

        chenh_lech = (
            ngan_sach
            - tong_gia_tri_gio
        )

        # ====================================================
        # 8. TỔNG QUAN
        # ====================================================

        st.divider()
        st.subheader("📊 Tổng quan giỏ hàng")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🛒 Tổng mục tiêu",
                dinh_dang_tien(tong_gia_tri_gio)
            )

        with col2:

            st.metric(
                "💰 Tiền lãi",
                dinh_dang_tien(ngan_sach)
            )

        with col3:

            if chenh_lech >= 0:

                st.metric(
                    "💵 Còn dư",
                    dinh_dang_tien(chenh_lech)
                )

            else:

                st.metric(
                    "📌 Còn thiếu",
                    dinh_dang_tien(abs(chenh_lech))
                )

        # ====================================================
        # 9. TIẾN ĐỘ HOÀN THÀNH
        # ====================================================

        if tong_gia_tri_gio > 0:

            ty_le_hoan_thanh = (
                ngan_sach
                / tong_gia_tri_gio
                * 100
            )

        else:

            ty_le_hoan_thanh = 0

        ty_le_progress = min(
            ty_le_hoan_thanh / 100,
            1.0
        )

        st.subheader("🎯 Tiến độ hoàn thành mục tiêu")

        st.progress(ty_le_progress)

        st.markdown(
            f"### {ty_le_hoan_thanh:.1f}%"
        )

        # ====================================================
        # 10. ĐÁNH GIÁ TOÀN BỘ GIỎ
        # ====================================================

        if ngan_sach >= tong_gia_tri_gio:

            st.success(
                f"""
### 🎉 Bạn đã đủ tiền lãi cho toàn bộ giỏ hàng!

Tổng giá trị các mục tiêu là
**{dinh_dang_tien(tong_gia_tri_gio)}**.

Tiền lãi hiện có là
**{dinh_dang_tien(ngan_sach)}**.

Sau khi thực hiện toàn bộ mục tiêu,
bạn vẫn còn:

### 💵 {dinh_dang_tien(chenh_lech)}

Bạn có thể hoàn thành toàn bộ giỏ hàng
**mà không cần sử dụng đến tiền gốc.**
"""
            )

        else:

            so_tien_con_thieu = (
                tong_gia_tri_gio
                - ngan_sach
            )

            st.warning(
                f"""
### 🔒 Chưa đủ tiền lãi cho toàn bộ giỏ hàng

Bạn đã đạt được
**{ty_le_hoan_thanh:.1f}%**
tổng giá trị mục tiêu.

Bạn còn thiếu:

### 📌 {dinh_dang_tien(so_tien_con_thieu)}
"""
            )

        # ====================================================
        # 11. KIỂM TRA TỪNG MỤC TIÊU
        # ====================================================

        st.divider()
        st.subheader("🔍 Khả năng đạt từng mục tiêu")

        for item in gio_hang:

            gia = item["gia"]

            if gia > 0:

                ty_le = (
                    ngan_sach
                    / gia
                    * 100
                )

            else:

                ty_le = 0

            if ngan_sach >= gia:

                tien_con_lai = (
                    ngan_sach
                    - gia
                )

                st.success(
                    f"""
✅ **{item['ten']}**

💵 Giá mục tiêu:
**{dinh_dang_tien(gia)}**

🎯 Tiền lãi hiện tại đáp ứng:
**{ty_le:.0f}%**

Nếu thực hiện riêng mục tiêu này,
bạn còn:

**{dinh_dang_tien(tien_con_lai)}**
"""
                )

            else:

                tien_thieu = (
                    gia
                    - ngan_sach
                )

                st.info(
                    f"""
🔒 **{item['ten']}**

💵 Giá mục tiêu:
**{dinh_dang_tien(gia)}**

🎯 Tiến độ:
**{ty_le:.1f}%**

📌 Còn thiếu:
**{dinh_dang_tien(tien_thieu)}**
"""
                )

        # ====================================================
        # 12. TÌM TỔ HỢP MỤC TIÊU PHÙ HỢP NHẤT
        # ====================================================

        st.divider()
        st.subheader("🧠 Gợi ý giỏ hàng phù hợp")

        st.write(
            "Hệ thống sẽ tự tìm tổ hợp mục tiêu có tổng giá trị "
            "gần nhất với số tiền lãi hiện có "
            "nhưng không vượt quá ngân sách."
        )

        to_hop_tot_nhat = []
        gia_tri_tot_nhat = 0

        # Giới hạn 15 mục tiêu để ứng dụng không bị chậm
        danh_sach_tim = gio_hang[:15]

        for so_luong in range(
            1,
            len(danh_sach_tim) + 1
        ):

            for to_hop in combinations(
                danh_sach_tim,
                so_luong
            ):

                tong_to_hop = sum(
                    item["gia"]
                    for item in to_hop
                )

                if (
                    tong_to_hop <= ngan_sach
                    and tong_to_hop > gia_tri_tot_nhat
                ):

                    gia_tri_tot_nhat = tong_to_hop
                    to_hop_tot_nhat = to_hop

        # ====================================================
        # 13. HIỂN THỊ GỢI Ý
        # ====================================================

        if to_hop_tot_nhat:

            st.markdown(
                "### ✨ Với số tiền lãi hiện tại, "
                "bạn có thể chọn:"
            )

            for item in to_hop_tot_nhat:

                st.write(
                    f"✅ {item['ten']} — "
                    f"**{dinh_dang_tien(item['gia'])}**"
                )

            tien_con_lai_sau_goi_y = (
                ngan_sach
                - gia_tri_tot_nhat
            )

            if ngan_sach > 0:

                ty_le_su_dung = (
                    gia_tri_tot_nhat
                    / ngan_sach
                    * 100
                )

            else:

                ty_le_su_dung = 0

            st.success(
                f"""
### 🛒 Phương án đề xuất

Tổng giá trị:
**{dinh_dang_tien(gia_tri_tot_nhat)}**

Sử dụng:
**{ty_le_su_dung:.1f}% tiền lãi**

Tiền lãi còn lại:

### 💵 {dinh_dang_tien(tien_con_lai_sau_goi_y)}
"""
            )

        # ====================================================
        # KHÔNG ĐỦ CHO BẤT KỲ MỤC TIÊU NÀO
        # ====================================================

        else:

            muc_tieu_re_nhat = min(
                gio_hang,
                key=lambda x: x["gia"]
            )

            tien_thieu_re_nhat = max(
                0,
                muc_tieu_re_nhat["gia"]
                - ngan_sach
            )

            st.warning(
                f"""
### 🎯 Mục tiêu gần nhất

Tiền lãi hiện tại chưa đủ cho bất kỳ
mục tiêu nào trong giỏ.

Mục tiêu gần nhất của bạn là:

**{muc_tieu_re_nhat['ten']}**

Giá:
**{dinh_dang_tien(muc_tieu_re_nhat['gia'])}**

Bạn chỉ còn thiếu:

### 📌 {dinh_dang_tien(tien_thieu_re_nhat)}
"""
            )

        # ====================================================
        # 14. XÓA TOÀN BỘ GIỎ
        # ====================================================

        st.divider()

        if st.button(
            "🗑️ Xóa toàn bộ giỏ hàng",
            use_container_width=True,
            key="xoa_toan_bo_gio"
        ):

            st.session_state["gio_hang_muc_tieu"] = []

            st.rerun()

    # ========================================================
    # GHI CHÚ
    # ========================================================

    st.caption(
        "💡 Giá các mục tiêu gợi ý chỉ mang tính minh họa. "
        "Bạn có thể điều chỉnh theo mức giá thực tế."
    )
