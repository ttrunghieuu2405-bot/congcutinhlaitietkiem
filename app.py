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

# ============================================================
# 🔐 TÍNH NĂNG: MỞ KHÓA TIỀN LÃI
# ============================================================

st.markdown("---")
st.header("🔐 Mở khóa tiền lãi")
st.caption(
    "Biến hành trình gửi tiết kiệm thành các cột mốc. "
    "Càng duy trì khoản gửi lâu, bạn càng mở khóa nhiều tiền lãi."
)

# ------------------------------------------------------------
# 1. NHẬP THÔNG TIN
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    unlock_principal = st.number_input(
        "💰 Số tiền gửi",
        min_value=1_000_000,
        value=200_000_000,
        step=1_000_000,
        key="unlock_principal"
    )

with col2:
    unlock_rate = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=30.0,
        value=6.0,
        step=0.1,
        key="unlock_rate"
    )

with col3:
    unlock_term = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1,
        key="unlock_term"
    )

# Người dùng giả lập mình đang ở tháng thứ mấy
current_month = st.slider(
    "⏳ Bạn đã gửi được bao nhiêu tháng?",
    min_value=0,
    max_value=int(unlock_term),
    value=min(3, int(unlock_term)),
    step=1
)

# ------------------------------------------------------------
# 2. TÍNH TOÁN
# ------------------------------------------------------------

monthly_rate = unlock_rate / 100 / 12

# Lãi cuối kỳ theo lãi đơn
total_interest = (
    unlock_principal *
    monthly_rate *
    unlock_term
)

# Lãi đã "mở khóa" đến thời điểm hiện tại
unlocked_interest = (
    unlock_principal *
    monthly_rate *
    current_month
)

remaining_interest = max(
    total_interest - unlocked_interest,
    0
)

progress = (
    current_month / unlock_term
    if unlock_term > 0
    else 0
)

# ------------------------------------------------------------
# 3. HIỂN THỊ TRẠNG THÁI KÉT
# ------------------------------------------------------------

st.subheader("🏦 Két tiết kiệm của bạn")

if current_month >= unlock_term:
    st.success("🔓 KÉT ĐÃ ĐƯỢC MỞ!")
else:
    st.info("🔒 KÉT ĐANG TÍCH LŨY")

st.progress(progress)

st.write(
    f"Bạn đã hoàn thành **{progress * 100:.1f}%** "
    f"kỳ hạn tiết kiệm."
)

# ------------------------------------------------------------
# 4. CÁC CHỈ SỐ
# ------------------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🔓 Lãi đã mở khóa",
        f"{unlocked_interest:,.0f} đ"
    )

with c2:
    st.metric(
        "🔒 Lãi đang chờ",
        f"{remaining_interest:,.0f} đ"
    )

with c3:
    st.metric(
        "🏆 Lãi khi đáo hạn",
        f"{total_interest:,.0f} đ"
    )

# ------------------------------------------------------------
# 5. HỆ THỐNG CỘT MỐC MỞ KHÓA
# ------------------------------------------------------------

st.subheader("🎯 Các cột mốc mở khóa")

# Tạo các mốc 25% - 50% - 75% - 100%
milestones = [
    ("🥉 Khởi động", 0.25),
    ("🥈 Kiên trì", 0.50),
    ("🥇 Gần đích", 0.75),
    ("🏆 Hoàn thành", 1.00)
]

for name, milestone_percent in milestones:

    milestone_month = max(
        1,
        round(unlock_term * milestone_percent)
    )

    milestone_interest = (
        unlock_principal *
        monthly_rate *
        milestone_month
    )

    if current_month >= milestone_month:

        st.success(
            f"🔓 {name} — Tháng {milestone_month}: "
            f"Đã mở khóa {milestone_interest:,.0f} đ"
        )

    else:

        months_left = milestone_month - current_month

        st.info(
            f"🔒 {name} — Tháng {milestone_month}: "
            f"{milestone_interest:,.0f} đ "
            f"• Còn {months_left} tháng"
        )

# ------------------------------------------------------------
# 6. MỤC TIÊU PHẦN THƯỞNG
# ------------------------------------------------------------

st.subheader("🎁 Phần thưởng tôi muốn mở khóa")

reward_name = st.text_input(
    "Bạn muốn dùng tiền lãi để làm gì?",
    placeholder="Ví dụ: Du lịch Đà Lạt"
)

reward_price = st.number_input(
    "💵 Số tiền cần cho mục tiêu",
    min_value=0,
    value=5_000_000,
    step=500_000
)

if reward_name and reward_price > 0:

    reward_progress = min(
        unlocked_interest / reward_price,
        1.0
    )

    st.write(f"### 🎯 {reward_name}")

    st.progress(reward_progress)

    percentage = (
        unlocked_interest /
        reward_price *
        100
    )

    st.write(
        f"Tiền lãi hiện tại đã đạt "
        f"**{percentage:.1f}%** mục tiêu."
    )

    if unlocked_interest >= reward_price:

        money_left = (
            unlocked_interest -
            reward_price
        )

        st.success(
            f"🎉 MỤC TIÊU ĐÃ ĐƯỢC MỞ KHÓA!\n\n"
            f"Bạn đã đủ tiền lãi cho **{reward_name}** "
            f"và còn dư **{money_left:,.0f} đ**."
        )

    else:

        money_needed = (
            reward_price -
            unlocked_interest
        )

        # Số lãi tạo ra mỗi tháng
        interest_per_month = (
            unlock_principal *
            monthly_rate
        )

        if interest_per_month > 0:

            months_needed = (
                money_needed /
                interest_per_month
            )

            st.warning(
                f"🔒 Chưa mở khóa.\n\n"
                f"Bạn còn thiếu **{money_needed:,.0f} đ**.\n\n"
                f"Ước tính cần thêm khoảng "
                f"**{months_needed:.1f} tháng** "
                f"để đạt mục tiêu nếu lãi suất không đổi."
            )

# ------------------------------------------------------------
# 7. TÍNH NĂNG "PHÁ KÉT"
# ------------------------------------------------------------

st.markdown("---")
st.subheader("🔨 Nếu tôi phá két ngay bây giờ?")

st.write(
    "Mô phỏng số tiền lãi bạn có thể bỏ lỡ "
    "nếu dừng khoản tiết kiệm trước khi đáo hạn."
)

early_rate = st.number_input(
    "Lãi suất rút trước hạn (%/năm)",
    min_value=0.0,
    max_value=30.0,
    value=0.5,
    step=0.1
)

early_interest = (
    unlock_principal *
    (early_rate / 100) *
    (current_month / 12)
)

early_total = (
    unlock_principal +
    early_interest
)

maturity_total = (
    unlock_principal +
    total_interest
)

lost_interest = max(
    total_interest -
    early_interest,
    0
)

if current_month == 0:

    st.info(
        "Hãy kéo thanh thời gian phía trên để "
        "mô phỏng việc rút tiền trước hạn."
    )

elif current_month >= unlock_term:

    st.success(
        "🎉 Khoản tiết kiệm đã đến ngày đáo hạn. "
        "Bạn không cần phá két nữa!"
    )

else:

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "💵 Rút ngay",
            f"{early_total:,.0f} đ"
        )

    with p2:
        st.metric(
            "🏆 Chờ đáo hạn",
            f"{maturity_total:,.0f} đ"
        )

    with p3:
        st.metric(
            "💸 Lãi có thể bỏ lỡ",
            f"{lost_interest:,.0f} đ"
        )

    st.warning(
        f"""
        ⚠️ Nếu phá két ở **tháng thứ {current_month}**:

        Bạn nhận khoảng **{early_total:,.0f} đ**.

        Nếu tiếp tục đến hết **{unlock_term} tháng**,
        bạn dự kiến nhận **{maturity_total:,.0f} đ**.

        👉 Phần tiền lãi chênh lệch là
        **{lost_interest:,.0f} đ**.
        """
    )

# ------------------------------------------------------------
# 8. THÔNG ĐIỆP CUỐI
# ------------------------------------------------------------

st.markdown("---")

if current_month >= unlock_term:

    st.balloons()

    st.success(
        f"""
        🏆 **MATURITY UNLOCKED!**

        Bạn đã hoàn thành kỳ hạn **{unlock_term} tháng**.

        💰 Tiền gốc: **{unlock_principal:,.0f} đ**

        💵 Tiền lãi: **{total_interest:,.0f} đ**

        🔓 Tổng nhận: **{maturity_total:,.0f} đ**
        """
    )

else:

    months_remaining = (
        unlock_term -
        current_month
    )

    st.info(
        f"🔐 Còn **{months_remaining} tháng** "
        f"để mở khóa toàn bộ "
        f"**{total_interest:,.0f} đ tiền lãi**."
    )
