# pages/5_Marketing_Reviews.py
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

st.set_page_config(page_title="Marketing & Đánh giá", page_icon="Megaphone", layout="wide")

# Kết nối DB
_mysql_user = os.getenv("MYSQL_USER", "root")
_mysql_password = os.getenv("MYSQL_ROOT_PASSWORD")
_mysql_host = os.getenv("MYSQL_HOST", "mysql")
_mysql_port = os.getenv("MYSQL_PORT", "3306")
_mysql_db = os.getenv("MYSQL_DB", "data_warehouse_olist")

engine = create_engine(
    f"mysql+pymysql://{_mysql_user}:{_mysql_password}@{_mysql_host}:{_mysql_port}/{_mysql_db}?charset=utf8mb4"
)

st.title("Marketing & Đánh giá Khách hàng")
st.markdown("---")

st.sidebar.header("Marketing & Reviews")
st.sidebar.write("""
Phân tích hiệu quả kênh marketing và trải nghiệm khách hàng qua:
- Lượng lead theo kênh
- Tỷ lệ chuyển đổi
- Đánh giá sản phẩm
- Xu hướng hài lòng
""")

tab1, tab2 = st.tabs(["Marketing", "Đánh giá"])

# ================================
# TAB 1: Marketing
# ================================
with tab1:
    col1, col2 = st.columns([3, 2])

    # Biểu đồ đường: Lượng lead theo kênh
    with col1:
        df_mkt = pd.read_sql("""
            SELECT first_contact_date, origin 
            FROM marketing_qualified_leads
            WHERE first_contact_date >= '2017-01-01'
        """, con=engine)
        
        df_mkt['thang'] = pd.to_datetime(df_mkt['first_contact_date']).dt.to_period('M').astype(str)
        df_group = df_mkt.groupby(['origin', 'thang']).size().reset_index(name='so_luong')
        df_group['thang'] = pd.to_datetime(df_group['thang'])

        fig = px.line(
            df_group, x='thang', y='so_luong', color='origin',
            title="Lượng lead theo kênh marketing",
            labels={"thang": "Tháng", "so_luong": "Số lead", "origin": "Kênh"},
            markers=True
        )
        fig.update_layout(hovermode="x unified", legend_title="Kênh")
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **Paid Search & Organic Search** tăng mạnh → SEO & quảng cáo Google hiệu quả.
        - **Direct Traffic** ổn định → thương hiệu đang được biết đến.
        - **Email & Social** thấp → cần đầu tư thêm nội dung, chiến dịch.
        """)

    # Biểu đồ cột: Tỷ lệ chốt đơn
    with col2:
        df_close = pd.read_sql("""
            SELECT 
                COALESCE(m.origin, 'unknown') AS kenh,
                COUNT(c.mql_id) * 100.0 / NULLIF(COUNT(m.mql_id), 0) AS ty_le_chot
            FROM marketing_qualified_leads m
            LEFT JOIN closed_deals c ON m.mql_id = c.mql_id
            GROUP BY kenh
            ORDER BY ty_le_chot DESC
        """, con=engine)

        fig = px.bar(
            df_close, x='kenh', y='ty_le_chot',
            title="Tỷ lệ chốt đơn theo kênh",
            labels={"kenh": "Kênh", "ty_le_chot": "Tỷ lệ chốt (%)"},
            color='ty_le_chot', color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **Unknown dẫn đầu ~15%** → cần cải thiện tracking nguồn.
        - **Paid Search hiệu quả nhất** → ROI cao, nên tăng ngân sách.
        - **Social, Email thấp** → nội dung chưa đủ hấp dẫn.
        """)

# ================================
# TAB 2: Đánh giá
# ================================
with tab2:
    col1, col2 = st.columns(2)

    # Biểu đồ cột ngang: Top 10 danh mục được đánh giá cao
    with col1:
        df_cat = pd.read_sql("""
            SELECT 
                COALESCE(p.category_name, 'Không xác định') AS danh_muc,
                ROUND(AVG(r.score), 2) AS diem_tb
            FROM order_reviews r
            JOIN order_items oi ON r.order_id = oi.order_id
            LEFT JOIN products p ON oi.product_id = p.product_id
            GROUP BY danh_muc
            HAVING COUNT(r.review_id) >= 50  -- Đảm bảo đủ mẫu
            ORDER BY diem_tb DESC
            LIMIT 10
        """, con=engine)

        fig = px.bar(
            df_cat, x='diem_tb', y='danh_muc', orientation='h',
            title="Top 10 danh mục được đánh giá cao nhất",
            labels={"danh_muc": "Danh mục", "diem_tb": "Điểm trung bình"},
            color='diem_tb', color_continuous_scale='Blues'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **CDs, sách, đồ nội thất** được đánh giá cao → chất lượng tốt.
        - **Khách hàng hài lòng với sản phẩm văn hóa, gia dụng**.
        - **Nên ưu tiên nhập hàng từ các danh mục này**.
        """)

    # Biểu đồ đường: Xu hướng đánh giá trung bình
    with col2:
        df_review = pd.read_sql("""
            SELECT r.score, o.purchase_timestamp
            FROM order_reviews r 
            JOIN orders o ON r.order_id = o.order_id
            WHERE o.purchase_timestamp BETWEEN '2017-01-01' AND '2018-09-01'
              AND o.status = 'delivered'
        """, con=engine)

        df_review['thang'] = pd.to_datetime(df_review['purchase_timestamp']).dt.to_period('M').astype(str)
        df_avg = df_review.groupby('thang')['score'].mean().reset_index()
        df_avg['thang'] = pd.to_datetime(df_avg['thang'])

        fig = px.line(
            df_avg, x='thang', y='score',
            title="Xu hướng đánh giá trung bình theo tháng",
            labels={"thang": "Tháng", "score": "Điểm trung bình"},
            markers=True
        )
        fig.update_yaxes(range=[3.5, 4.5])
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **Điểm trung bình ~4.0 - 4.3** → **khách hàng rất hài lòng**.
        - **Giảm mạnh tháng 11/2017** → có thể do quá tải đơn hàng.
        - **Phục hồi tốt từ 2018** → cải thiện dịch vụ thành công.
        """)