# Home.py
import streamlit as st

st.set_page_config(page_title="Olist Dashboard", page_icon="Home", layout="wide")
st.sidebar.header("Home")
st.sidebar.write("**Chào mừng đến với Olist BI Dashboard**")

st.title("Dự Án Cuối Khóa - Olist Dashboard")

col1, col2 = st.columns(2)
st.markdown("---")

with col1:
    st.markdown("### Tư Vấn Dữ Liệu")
    st.markdown(
        """
        Phân tích dữ liệu từ **Olist** – nền tảng thương mại điện tử Brazil – để:
        - Hiểu hành vi khách hàng
        - Tối ưu doanh thu
        - Cải thiện dịch vụ
        """
    )

with col2:
    st.markdown("### Mục Tiêu")
    st.markdown(
        """
        Xây dựng **Dashboard BI** với:
        - **6 KPIs chính**
        - Biểu đồ tương tác
        - Bản đồ địa lý
        - Phân tích marketing & review
        """
    )

st.header("Olist là gì?")
try:
    video_file = open("src/Olist.mp4", "rb")
    st.video(video_file.read())
except:
    st.warning("Video không tìm thấy. Vui lòng kiểm tra `src/Olist.mp4`")