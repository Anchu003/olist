import streamlit as st
from PIL import Image

# ==============================
# TRANG CHỦ: OLIST'S MACHINE LEARNING MODELS
# Mục đích: Giới thiệu tổng quan về các mô hình ML của Olist
# Nội dung: Tiêu đề, hình ảnh, và đoạn giới thiệu ngắn
# ==============================

# Tạo layout 3 cột để căn giữa nội dung chính
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Tiêu đề chính
    st.header("Olist's Machine Learning Models")

    # Hiển thị hình ảnh minh họa (biểu tượng AI/ML)
    image = Image.open("src/brain.png")
    st.image(image, caption="", use_column_width=True)

    # Khoảng cách dọc
    st.write("")

    st.markdown(
        """
        <div style="text-align: justify; font-size: 16px; color: #333;">
        <p>
        Olist sử dụng <strong>các mô hình học máy tiên tiến</strong> để tối ưu hóa quy trình kinh doanh trên nền tảng thương mại điện tử. 
        Từ <strong>dự đoán doanh thu</strong>, <strong>gợi ý sản phẩm</strong>, đến <strong>phát hiện gian lận</strong> và 
        <strong>phân tích cảm xúc khách hàng</strong> — tất cả đều được hỗ trợ bởi AI.
        </p>
        <p>
        Khám phá các mô hình ML đã và đang giúp Olist nâng cao trải nghiệm người dùng và tăng trưởng bền vững.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )