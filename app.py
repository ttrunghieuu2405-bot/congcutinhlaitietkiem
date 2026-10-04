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
# code phần tính lãi phía trên
# ...

# ============================================================
# 🛒 GIỎ HÀNG MỤC TIÊU
# ============================================================

from itertools import combinations
import streamlit as st

st.markdown("---")
st.header("🛒 Giỏ hàng mục tiêu")

st.write(
    "Hãy biến tiền lãi tiết kiệm thành những mục tiêu thực tế "
    "mà bạn muốn đạt được."
)

# ============================================================
# LƯU Ý:
# Phần code tính lãi phía trên cần có biến:
#
# total_interest = tổng số tiền lãi nhận được
#
# Ví dụ:
# total_interest = 30_000_000
#
# Nếu biến tổng tiền lãi trong app của bạn có tên khác,
# hãy thay total_interest bằng tên biến đó.
# ============================================================


# ============================================================
# 1. HIỂN THỊ NGÂN SÁCH TỪ TIỀN LÃI
# ============================================================

st.subheader("💰 Ngân sách từ tiền lãi")

st.metric(
    "Tổng tiền lãi có thể sử dụng",
    f"{total_interest:,.0f} đ"
)

st.success(
    f"✨ Bạn đang có **{total_interest:,.0f} đ tiền lãi** "
    f"để thực hiện các mục tiêu mà không cần sử dụng tiền gốc."
)


# ============================================================
# 2. DANH SÁCH MỤC TIÊU GỢI Ý
# ============================================================

GOALS = {

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
        "🛋️ Nội thất": 20_000_000,
        "🤖 Robot hút bụi": 8_000_000
    },

    "🎁 Cá nhân": {
        "🏍️ Xe máy": 40_000_000,
        "📷 Máy ảnh": 20_000_000,
        "🎸 Nhạc cụ": 10_000_000,
        "👟 Mua sắm cá nhân": 5_000_000,
        "🎁 Quà tặng": 3_000_000
    }
}


# ============================================================
# 3. KHỞI TẠO GIỎ HÀNG
# ============================================================

if "goal_cart" not in st.session_state:
    st.session_state.goal_cart = []


# ============================================================
# 4. CHỌN MỤC TIÊU
# ============================================================

st.markdown("---")
st.subheader("🎯 Thêm mục tiêu")

tab1, tab2 = st.tabs([
    "✨ Mục tiêu gợi ý",
    "✍️ Tự tạo mục tiêu"
])


# ============================================================
# TAB 1 - MỤC TIÊU GỢI Ý
# ============================================================

with tab1:

    category = st.selectbox(
        "📂 Chọn nhóm mục tiêu",
        list(GOALS.keys()),
        key="goal_category"
    )

    selected_goal = st.selectbox(
        "🎯 Chọn mục tiêu",
        list(GOALS[category].keys()),
        key="selected_goal"
    )

    suggested_price = GOALS[category][selected_goal]

    goal_price = st.number_input(
        "💵 Giá mục tiêu",
        min_value=1_000,
        value=int(suggested_price),
        step=100_000,
        key="goal_price"
    )

    st.caption(
        "💡 Mức giá trên chỉ mang tính minh họa. "
        "Bạn có thể nhập lại giá thực tế."
    )

    if st.button(
        "🛒 Thêm vào giỏ hàng",
        type="primary",
        use_container_width=True,
        key="add_goal"
    ):

        st.session_state.goal_cart.append({
            "name": selected_goal,
            "price": goal_price,
            "category": category
        })

        st.success(
            f"✅ Đã thêm {selected_goal} vào giỏ hàng."
        )


# ============================================================
# TAB 2 - TỰ TẠO MỤC TIÊU
# ============================================================

with tab2:

    custom_name = st.text_input(
        "🎯 Mục tiêu của bạn",
        placeholder="Ví dụ: Mua xe máy",
        key="custom_goal_name"
    )

    custom_price = st.number_input(
        "💵 Số tiền cần cho mục tiêu",
        min_value=0,
        value=10_000_000,
        step=500_000,
        key="custom_goal_price"
    )

    custom_category = st.selectbox(
        "📂 Nhóm mục tiêu",
        [
            "📱 Công nghệ",
            "✈️ Du lịch",
            "🎓 Học tập",
            "🏠 Gia đình",
            "🎁 Cá nhân",
            "⭐ Khác"
        ],
        key="custom_goal_category"
    )

    if st.button(
        "🛒 Thêm mục tiêu của tôi",
        type="primary",
        use_container_width=True,
        key="add_custom_goal"
    ):

        if custom_name.strip() == "":
            st.warning(
                "⚠️ Vui lòng nhập tên mục tiêu."
            )

        elif custom_price <= 0:
            st.warning(
                "⚠️ Số tiền của mục tiêu phải lớn hơn 0."
            )

        else:

            st.session_state.goal_cart.append({
                "name": custom_name,
                "price": custom_price,
                "category": custom_category
            })

            st.success(
                f"✅ Đã thêm {custom_name} vào giỏ hàng."
            )


# ============================================================
# 5. HIỂN THỊ GIỎ HÀNG
# ============================================================

st.markdown("---")
st.subheader("🛒 Giỏ hàng của tôi")

cart = st.session_state.goal_cart


if len(cart) == 0:

    st.info(
        "🛒 Giỏ hàng đang trống. "
        "Hãy thêm một hoặc nhiều mục tiêu ở phía trên."
    )


else:

    # ========================================================
    # HIỂN THỊ TỪNG MỤC TIÊU
    # ========================================================

    for index, item in enumerate(cart):

        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:

            st.markdown(
                f"**{item['name']}**"
            )

            st.caption(
                item["category"]
            )

        with col2:

            st.markdown(
                f"**{item['price']:,.0f} đ**"
            )

        with col3:

            if st.button(
                "🗑️",
                key=f"delete_goal_{index}"
            ):

                st.session_state.goal_cart.pop(index)
                st.rerun()


    # ========================================================
    # 6. TỔNG GIÁ TRỊ GIỎ HÀNG
    # ========================================================

    total_cart = sum(
        item["price"]
        for item in cart
    )

    difference = total_interest - total_cart


    st.markdown("---")
    st.subheader("📊 Tổng quan mục tiêu")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🛒 Tổng giá trị mục tiêu",
            f"{total_cart:,.0f} đ"
        )


    with col2:

        st.metric(
            "💰 Tiền lãi hiện có",
            f"{total_interest:,.0f} đ"
        )


    with col3:

        if difference >= 0:

            st.metric(
                "💵 Còn dư",
                f"{difference:,.0f} đ"
            )

        else:

            st.metric(
                "📌 Còn thiếu",
                f"{abs(difference):,.0f} đ"
            )


    # ========================================================
    # 7. THANH TIẾN ĐỘ
    # ========================================================

    if total_cart > 0:

        completion_percent = (
            total_interest /
            total_cart *
            100
        )

    else:

        completion_percent = 0


    progress_value = min(
        completion_percent / 100,
        1.0
    )


    st.subheader("🎯 Tiến độ hoàn thành mục tiêu")

    st.progress(progress_value)

    st.markdown(
        f"### {completion_percent:.1f}%"
    )

    st.write(
        "Tiền lãi hiện tại đã đáp ứng được "
        f"**{completion_percent:.1f}%** "
        "tổng giá trị các mục tiêu."
    )


    # ========================================================
    # 8. KẾT QUẢ TOÀN BỘ GIỎ HÀNG
    # ========================================================

    if total_interest >= total_cart:

        st.success(
            f"""
### 🎉 Bạn đã đạt đủ ngân sách cho toàn bộ giỏ hàng!

🛒 Tổng giá trị mục tiêu: **{total_cart:,.0f} đ**

💰 Tiền lãi của bạn: **{total_interest:,.0f} đ**

💵 Sau khi hoàn thành tất cả mục tiêu,
bạn vẫn còn **{difference:,.0f} đ tiền lãi**.

✨ Bạn có thể thực hiện toàn bộ các mục tiêu
**mà không cần sử dụng đến tiền gốc.**
"""
        )


    else:

        shortage = total_cart - total_interest

        st.warning(
            f"""
### 🔒 Bạn chưa đủ ngân sách cho toàn bộ giỏ hàng

🛒 Tổng giá trị mục tiêu: **{total_cart:,.0f} đ**

💰 Tiền lãi hiện có: **{total_interest:,.0f} đ**

📌 Bạn còn thiếu **{shortage:,.0f} đ**
để hoàn thành toàn bộ mục tiêu.
"""
        )


    # ========================================================
    # 9. PHÂN TÍCH TỪNG MỤC TIÊU
    # ========================================================

    st.markdown("---")
    st.subheader("🔍 Khả năng đạt từng mục tiêu")


    for item in cart:

        price = item["price"]

        percent = (
            total_interest /
            price *
            100
        )

        if total_interest >= price:

            money_left = (
                total_interest -
                price
            )

            st.success(
                f"""
✅ **{item['name']}**

Giá mục tiêu: **{price:,.0f} đ**

🎯 Đã đạt: **{percent:.0f}%**

💵 Nếu thực hiện mục tiêu này,
bạn còn **{money_left:,.0f} đ tiền lãi**.
"""
            )

        else:

            missing = (
                price -
                total_interest
            )

            st.info(
                f"""
🔒 **{item['name']}**

Giá mục tiêu: **{price:,.0f} đ**

🎯 Đã đạt: **{percent:.1f}%**

📌 Còn thiếu: **{missing:,.0f} đ**
"""
            )


    # ========================================================
    # 10. GỢI Ý GIỎ HÀNG PHÙ HỢP
    # ========================================================

    st.markdown("---")
    st.subheader("💡 Gợi ý sử dụng tiền lãi")

    st.write(
        "Hệ thống sẽ tìm tổ hợp mục tiêu có tổng giá trị "
        "gần nhất với số tiền lãi hiện có mà không vượt ngân sách."
    )


    best_combo = []
    best_value = 0


    # Giới hạn tối đa 15 mục tiêu
    # để tránh xử lý quá nhiều tổ hợp
    search_cart = cart[:15]


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


    # ========================================================
    # 11. HIỂN THỊ PHƯƠNG ÁN GỢI Ý
    # ========================================================

    if best_combo:

        st.markdown(
            "### ✨ Với tiền lãi hiện tại, "
            "bạn có thể thực hiện:"
        )


        for item in best_combo:

            st.write(
                f"✅ {item['name']} "
                f"— **{item['price']:,.0f} đ**"
            )


        remaining_after_combo = (
            total_interest -
            best_value
        )


        usage_percent = (
            best_value /
            total_interest *
            100
            if total_interest > 0
            else 0
        )


        st.success(
            f"""
🛒 **Tổng giá trị mục tiêu:** {best_value:,.0f} đ

💰 **Tiền lãi hiện có:** {total_interest:,.0f} đ

📊 **Sử dụng:** {usage_percent:.1f}% tiền lãi

💵 **Còn lại:** {remaining_after_combo:,.0f} đ
"""
        )


    else:

        cheapest_item = min(
            cart,
            key=lambda x: x["price"]
        )

        missing_cheapest = max(
            0,
            cheapest_item["price"]
            - total_interest
        )


        st.warning(
            f"""
### 🎯 Mục tiêu gần nhất

Hiện tại tiền lãi chưa đủ để hoàn thành
mục tiêu nào trong giỏ hàng.

Mục tiêu gần nhất là:

**{cheapest_item['name']}**

💵 Giá: **{cheapest_item['price']:,.0f} đ**

📌 Bạn còn thiếu:
**{missing_cheapest:,.0f} đ**
"""
        )


    # ========================================================
    # 12. XÓA TOÀN BỘ GIỎ HÀNG
    # ========================================================

    st.markdown("---")


    if st.button(
        "🗑️ Xóa toàn bộ giỏ hàng",
        use_container_width=True,
        key="clear_goal_cart"
    ):

        st.session_state.goal_cart = []

        st.rerun()


# ============================================================
# 13. GHI CHÚ
# ============================================================

st.markdown("---")

st.caption(
    "💡 Giá của các mục tiêu gợi ý chỉ mang tính minh họa. "
    "Người dùng có thể điều chỉnh theo nhu cầu và mức giá thực tế."
)
