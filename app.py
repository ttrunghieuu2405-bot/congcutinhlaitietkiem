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

import streamlit as st
import math
from itertools import combinations

# ============================================================
# 🛒 GIỎ HÀNG MỤC TIÊU 
# ============================================================

st.markdown("---")
st.header("🛒 Giỏ hàng mục tiêu")
st.caption(
    "Biến tiền lãi tiết kiệm thành những mục tiêu thực tế "
    "mà bạn muốn đạt được."
)

# ============================================================
# 0. DỮ LIỆU DEMO
# XÓA PHẦN NÀY nếu app chính đã có các biến tương ứng
# ============================================================

with st.expander("⚙️ Thông tin khoản tiết kiệm", expanded=True):

    c1, c2, c3 = st.columns(3)

    with c1:
        principal = st.number_input(
            "💰 Số tiền gửi",
            min_value=1_000_000,
            value=500_000_000,
            step=1_000_000,
            key="goal_principal"
        )

    with c2:
        annual_rate = st.number_input(
            "📈 Lãi suất (%/năm)",
            min_value=0.0,
            max_value=30.0,
            value=6.0,
            step=0.1,
            key="goal_rate"
        )

    with c3:
        months = st.number_input(
            "📅 Kỳ hạn (tháng)",
            min_value=1,
            max_value=120,
            value=12,
            step=1,
            key="goal_months"
        )

# ============================================================
# 1. TÍNH TIỀN LÃI
# ============================================================

interest_type = st.radio(
    "🧮 Cách tính tiền lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True,
    key="goal_interest_type"
)

monthly_rate = annual_rate / 100 / 12

if interest_type == "Lãi đơn":

    total_interest = (
        principal *
        monthly_rate *
        months
    )

else:

    final_amount = (
        principal *
        (1 + monthly_rate) ** months
    )

    total_interest = (
        final_amount -
        principal
    )

final_amount = principal + total_interest

# ============================================================
# 2. HIỂN THỊ NGÂN SÁCH TỪ TIỀN LÃI
# ============================================================

st.subheader("💰 Ngân sách Lifestyle ROI")

a, b, c = st.columns(3)

with a:
    st.metric(
        "Tiền gốc",
        f"{principal:,.0f} đ"
    )

with b:
    st.metric(
        "Tiền lãi dự kiến",
        f"{total_interest:,.0f} đ"
    )

with c:
    st.metric(
        "Tổng gốc + lãi",
        f"{final_amount:,.0f} đ"
    )

st.success(
    f"✨ Bạn có **{total_interest:,.0f} đ tiền lãi** "
    f"để biến thành các mục tiêu mà không cần sử dụng tiền gốc."
)

# ============================================================
# 3. DANH SÁCH MỤC TIÊU GỢI Ý
# Giá chỉ là giá mẫu để demo.
# Người dùng có thể chỉnh giá trước khi thêm.
# ============================================================

GOALS = {

    "📱 Công nghệ": {
        "📱 Điện thoại": 25_000_000,
        "💻 Laptop": 20_000_000,
        "⌚ Đồng hồ thông minh": 8_000_000,
        "🎧 Tai nghe": 5_000_000,
        "📱 Máy tính bảng": 15_000_000
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
        "📝 Lệ phí chứng chỉ": 5_000_000
    },

    "🏠 Gia đình": {
        "📺 TV": 15_000_000,
        "🧊 Tủ lạnh": 12_000_000,
        "🧺 Máy giặt": 10_000_000,
        "🛋️ Nội thất": 20_000_000
    },

    "🎁 Cá nhân": {
        "🚲 Xe đạp": 8_000_000,
        "📷 Máy ảnh": 20_000_000,
        "🎸 Nhạc cụ": 10_000_000,
        "👟 Shopping": 5_000_000
    }
}

# ============================================================
# 4. KHỞI TẠO GIỎ HÀNG
# ============================================================

if "lifestyle_cart" not in st.session_state:
    st.session_state.lifestyle_cart = []

# ============================================================
# 5. THÊM MỤC TIÊU CÓ SẴN
# ============================================================

st.markdown("---")
st.subheader("🎯 Chọn mục tiêu của bạn")

tab1, tab2 = st.tabs(
    [
        "✨ Mục tiêu gợi ý",
        "✍️ Tự tạo mục tiêu"
    ]
)

with tab1:

    category = st.selectbox(
        "Chọn nhóm mục tiêu",
        list(GOALS.keys()),
        key="goal_category"
    )

    goal_name = st.selectbox(
        "Chọn mục tiêu",
        list(GOALS[category].keys()),
        key="goal_name"
    )

    suggested_price = GOALS[category][goal_name]

    goal_price = st.number_input(
        "💵 Giá mục tiêu",
        min_value=1_000,
        value=int(suggested_price),
        step=100_000,
        key="suggested_goal_price"
    )

    st.caption(
        "💡 Giá trên chỉ dùng để minh họa. "
        "Bạn có thể chỉnh lại theo giá thực tế."
    )

    if st.button(
        "➕ Thêm vào giỏ",
        type="primary",
        use_container_width=True,
        key="add_suggested_goal"
    ):

        st.session_state.lifestyle_cart.append(
            {
                "name": goal_name,
                "price": goal_price,
                "category": category
            }
        )

        st.success(
            f"Đã thêm {goal_name} vào giỏ!"
        )

# ============================================================
# 6. TỰ TẠO MỤC TIÊU
# ============================================================

with tab2:

    custom_name = st.text_input(
        "🎯 Tôi muốn...",
        placeholder="Ví dụ: Mua xe máy",
        key="custom_goal_name"
    )

    custom_price = st.number_input(
        "💵 Giá mục tiêu",
        min_value=0,
        value=30_000_000,
        step=500_000,
        key="custom_goal_price"
    )

    custom_category = st.selectbox(
        "📂 Nhóm",
        [
            "📱 Công nghệ",
            "✈️ Du lịch",
            "🎓 Học tập",
            "🏠 Gia đình",
            "🎁 Cá nhân",
            "⭐ Khác"
        ],
        key="custom_category"
    )

    if st.button(
        "➕ Thêm mục tiêu của tôi",
        type="primary",
        use_container_width=True,
        key="add_custom_goal"
    ):

        if custom_name.strip() == "":

            st.warning(
                "Vui lòng nhập tên mục tiêu."
            )

        elif custom_price <= 0:

            st.warning(
                "Giá mục tiêu phải lớn hơn 0."
            )

        else:

            st.session_state.lifestyle_cart.append(
                {
                    "name": custom_name,
                    "price": custom_price,
                    "category": custom_category
                }
            )

            st.success(
                f"Đã thêm {custom_name} vào giỏ!"
            )

# ============================================================
# 7. HIỂN THỊ GIỎ HÀNG
# ============================================================

st.markdown("---")
st.subheader("🛒 Giỏ hàng của tôi")

cart = st.session_state.lifestyle_cart

if len(cart) == 0:

    st.info(
        "Giỏ hàng đang trống. "
        "Hãy thêm ít nhất một mục tiêu ở phía trên."
    )

else:

    # --------------------------------------------------------
    # Hiển thị từng sản phẩm
    # --------------------------------------------------------

    for index, item in enumerate(cart):

        col_name, col_price, col_delete = st.columns(
            [5, 2, 1]
        )

        with col_name:

            st.write(
                f"**{item['name']}**"
            )

            st.caption(
                item["category"]
            )

        with col_price:

            st.write(
                f"**{item['price']:,.0f} đ**"
            )

        with col_delete:

            if st.button(
                "🗑️",
                key=f"delete_goal_{index}"
            ):

                st.session_state.lifestyle_cart.pop(index)
                st.rerun()

    # ========================================================
    # 8. TỔNG GIÁ TRỊ GIỎ HÀNG
    # ========================================================

    total_cart = sum(
        item["price"]
        for item in cart
    )

    remaining_money = (
        total_interest -
        total_cart
    )

    if total_cart > 0:

        goal_percentage = (
            total_interest /
            total_cart *
            100
        )

    else:

        goal_percentage = 0

    st.markdown("---")

    x1, x2, x3 = st.columns(3)

    with x1:

        st.metric(
            "🛒 Tổng giỏ hàng",
            f"{total_cart:,.0f} đ"
        )

    with x2:

        st.metric(
            "💰 Tiền lãi",
            f"{total_interest:,.0f} đ"
        )

    with x3:

        if remaining_money >= 0:

            st.metric(
                "💵 Còn dư",
                f"{remaining_money:,.0f} đ"
            )

        else:

            st.metric(
                "❗ Còn thiếu",
                f"{abs(remaining_money):,.0f} đ"
            )

    # ========================================================
    # 9. PROGRESS BAR
    # ========================================================

    st.subheader("📊 Mức độ hoàn thành giỏ hàng")

    progress = min(
        goal_percentage / 100,
        1.0
    )

    st.progress(progress)

    st.write(
        f"Tiền lãi hiện tại đáp ứng được "
        f"**{goal_percentage:.1f}%** "
        f"giá trị giỏ hàng."
    )

    # ========================================================
    # 10. PHÂN TÍCH KẾT QUẢ
    # ========================================================

    if total_interest >= total_cart:

        st.success(
            f"""
🎉 **LIFESTYLE GOAL UNLOCKED!**

Tiền lãi của bạn đủ để hoàn thành
**toàn bộ {len(cart)} mục tiêu trong giỏ hàng**.

🛒 Tổng giá trị mục tiêu: **{total_cart:,.0f} đ**

💰 Tiền lãi: **{total_interest:,.0f} đ**

💵 Sau khi hoàn thành các mục tiêu,
bạn vẫn còn **{remaining_money:,.0f} đ tiền lãi**.

👉 Và quan trọng nhất:
**Bạn chưa cần sử dụng đến tiền gốc.**
"""
        )

        st.balloons()

    else:

        shortage = (
            total_cart -
            total_interest
        )

        st.warning(
            f"""
🔒 **Bạn chưa hoàn thành toàn bộ giỏ hàng.**

Giỏ hàng cần: **{total_cart:,.0f} đ**

Tiền lãi hiện có: **{total_interest:,.0f} đ**

Bạn còn thiếu: **{shortage:,.0f} đ**
"""
        )

        # ====================================================
        # 11. TÍNH THỜI GIAN CẦN THÊM
        # ====================================================

        if principal > 0 and annual_rate > 0:

            if interest_type == "Lãi đơn":

                monthly_interest = (
                    principal *
                    annual_rate /
                    100 /
                    12
                )

                required_total_months = (
                    total_cart /
                    monthly_interest
                )

            else:

                target_ratio = (
                    1 +
                    total_cart /
                    principal
                )

                required_total_months = (
                    math.log(target_ratio) /
                    math.log(1 + monthly_rate)
                )

            additional_months = max(
                0,
                required_total_months - months
            )

            st.info(
                f"⏳ Với giả định lãi suất **{annual_rate:.2f}%/năm** "
                f"không đổi, bạn cần khoảng "
                f"**{additional_months:.1f} tháng nữa** "
                f"để tiền lãi đạt giá trị của toàn bộ giỏ hàng."
            )

    # ========================================================
    # 12. KIỂM TRA TỪNG MỤC TIÊU
    # ========================================================

    st.markdown("---")
    st.subheader("🔎 Tiền lãi đủ cho mục tiêu nào?")

    affordable_items = []

    for item in cart:

        if total_interest >= item["price"]:

            affordable_items.append(item)

            percentage = (
                total_interest /
                item["price"] *
                100
            )

            st.success(
                f"✅ {item['name']} — "
                f"{item['price']:,.0f} đ "
                f"• Đạt {percentage:.0f}%"
            )

        else:

            missing = (
                item["price"] -
                total_interest
            )

            percentage = (
                total_interest /
                item["price"] *
                100
            )

            st.info(
                f"🔒 {item['name']} — "
                f"{item['price']:,.0f} đ "
                f"• Đạt {percentage:.0f}% "
                f"• Thiếu {missing:,.0f} đ"
            )

    # ========================================================
    # 13. SMART CART
    # TÌM TỔ HỢP MỤC TIÊU TỐT NHẤT
    # ========================================================

    st.markdown("---")
    st.subheader("🧠 Smart Cart")

    st.caption(
        "App tự tìm tổ hợp mục tiêu có tổng giá trị "
        "gần nhất với tiền lãi nhưng không vượt quá ngân sách."
    )

    best_combo = []
    best_value = 0

    # Giới hạn để tránh quá nhiều tổ hợp
    max_items_for_search = min(
        len(cart),
        15
    )

    search_cart = cart[:max_items_for_search]

    for r in range(
        1,
        len(search_cart) + 1
    ):

        for combo in combinations(
            search_cart,
            r
        ):

            combo_value = sum(
                item["price"]
                for item in combo
            )

            if (
                combo_value <= total_interest
                and combo_value > best_value
            ):

                best_value = combo_value
                best_combo = combo

    if best_combo:

        st.write(
            "### ✨ Với tiền lãi hiện tại, "
            "bạn có thể hoàn thành:"
        )

        for item in best_combo:

            st.write(
                f"✅ {item['name']} "
                f"— **{item['price']:,.0f} đ**"
            )

        money_after_combo = (
            total_interest -
            best_value
        )

        st.success(
            f"""
🛍️ Tổng giá trị: **{best_value:,.0f} đ**

💰 Tiền lãi của bạn: **{total_interest:,.0f} đ**

💵 Sau khi hoàn thành các mục tiêu trên,
bạn còn **{money_after_combo:,.0f} đ**.
"""
        )

    else:

        cheapest_item = min(
            cart,
            key=lambda x: x["price"]
        )

        missing_cheapest = (
            cheapest_item["price"] -
            total_interest
        )

        st.warning(
            f"""
Hiện tại tiền lãi chưa đủ cho mục tiêu nào trong giỏ.

🎯 Mục tiêu gần nhất:

**{cheapest_item['name']}**

Giá: **{cheapest_item['price']:,.0f} đ**

Bạn còn thiếu khoảng
**{max(0, missing_cheapest):,.0f} đ**.
"""
        )

    # ========================================================
    # 14. NÚT XÓA TOÀN BỘ GIỎ
    # ========================================================

    st.markdown("---")

    if st.button(
        "🗑️ Xóa toàn bộ giỏ hàng",
        use_container_width=True,
        key="clear_lifestyle_cart"
    ):

        st.session_state.lifestyle_cart = []
        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "💡 Giỏ hàng mục tiêu chỉ mang tính mô phỏng. "
    "Giá mục tiêu và lãi suất có thể thay đổi theo thời gian."
)
