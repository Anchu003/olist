# pages/4_Method_Delivery.py
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from sqlalchemy import create_engine
import os

# Cấu hình trang
st.set_page_config(page_title="Thanh toán & Giao hàng", page_icon="Package", layout="wide")

st.title("Phân tích Phương thức Thanh toán & Giao hàng")
st.markdown("---")

st.sidebar.header("Thanh toán & Giao hàng")
st.sidebar.write("""
Phân tích chi tiết:
- Tỷ lệ phương thức thanh toán
- Số kỳ trả góp
- Thời gian giao hàng
- Chi phí vận chuyển theo trọng lượng
- Hành trình từ người bán → khách hàng
""")

# Kết nối DB
_mysql_user = os.getenv("MYSQL_USER", "root")
_mysql_password = os.getenv("MYSQL_ROOT_PASSWORD")
_mysql_host = os.getenv("MYSQL_HOST", "mysql")
_mysql_port = os.getenv("MYSQL_PORT", "3306")
_mysql_db = os.getenv("MYSQL_DB", "data_warehouse_olist")

engine = create_engine(
    f"mysql+pymysql://{_mysql_user}:{_mysql_password}@{_mysql_host}:{_mysql_port}/{_mysql_db}?charset=utf8mb4"
)

# Tabs
tab1, tab2, tab3 = st.tabs(["Phương thức thanh toán", "Giao hàng", "Hành trình"])

# ================================
# TAB 1: Phương thức thanh toán
# ================================
with tab1:
    col1, col2 = st.columns(2)

    # Biểu đồ tròn: Phương thức
    with col1:
        df_pay = pd.read_sql("SELECT type FROM order_payments", con=engine)
        pay_count = df_pay['type'].value_counts().reset_index()
        pay_count.columns = ['phuong_thuc', 'so_luong']
        pay_count['ty_le'] = (pay_count['so_luong'] / pay_count['so_luong'].sum() * 100).round(2)

        fig = px.pie(
            pay_count, values='so_luong', names='phuong_thuc',
            title="Tỷ lệ phương thức thanh toán",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **Thẻ tín dụng chiếm 73.9%** → Phương thức **phổ biến nhất**, phù hợp với xu hướng thanh toán online.
        - **Boleto (19%)** → Phương thức truyền thống, phù hợp với người không dùng thẻ.
        - **Voucher & Thẻ ghi nợ** chiếm tỷ lệ nhỏ → chủ yếu dùng khuyến mãi.
        """)

    # Biểu đồ cột: Số kỳ trả góp
    with col2:
        df_inst = pd.read_sql("SELECT installments FROM order_payments WHERE installments > 0", con=engine)
        inst_count = df_inst['installments'].value_counts().reset_index()
        inst_count.columns = ['ky', 'so_luong']
        inst_count = inst_count.sort_values('ky')

        fig = px.bar(
            inst_count, x='ky', y='so_luong',
            title="Phân bố số kỳ trả góp",
            labels={"ky": "Số kỳ", "so_luong": "Số lượng thanh toán"},
            color='so_luong', color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        st.plotly_chart(fig, use_container_width=True)

        # NHẬN XÉT
        st.markdown("#### Nhận xét:")
        st.write("""
        - **> 50% người dùng chọn trả 1 lần** → Ưu tiên thanh toán nhanh.
        - **2-3 kỳ** chiếm phần lớn còn lại → phù hợp với sản phẩm giá trung bình.
        - **> 10 kỳ** rất ít → Olist chủ yếu bán hàng giá rẻ, không cần trả góp dài.
        """)

# ================================
# TAB 2: Giao hàng
# ================================
with tab2:
    col1, col2 = st.columns(2)

    # Thời gian giao
    with col1:
        df_time = pd.read_sql("""
            SELECT 
                CASE 
                    WHEN dias < 4 THEN 'Dưới 4 ngày'
                    WHEN dias < 7 THEN '4-6 ngày'
                    WHEN dias < 11 THEN '7-10 ngày'
                    WHEN dias < 16 THEN '11-15 ngày'
                    WHEN dias < 20 THEN '16-20 ngày'
                    ELSE 'Trên 20 ngày'
                END AS nhom,
                COUNT(*) AS so_luong
            FROM (
                SELECT DATEDIFF(delivered_customer_date, purchase_timestamp) AS dias
                FROM orders 
                WHERE status = 'delivered' AND delivered_customer_date IS NOT NULL
            ) t
            GROUP BY nhom
            ORDER BY FIELD(nhom, 'Dưới 4 ngày', '4-6 ngày', '7-10 ngày', '11-15 ngày', '16-20 ngày', 'Trên 20 ngày')
        """, con=engine)

        fig = px.bar(df_time, x='nhom', y='so_luong', title="Thời gian giao hàng",
                     labels={"nhom": "Khoảng thời gian", "so_luong": "Số đơn hàng"})
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Nhận xét:")
        st.write("""
        - **Phần lớn đơn hàng giao trong 4-10 ngày** → Hiệu quả logistics tốt.
        - **Dưới 4 ngày** chiếm tỷ lệ nhỏ → Có thể cải thiện bằng kho gần khách.
        - **> 20 ngày** rất ít → Chất lượng dịch vụ ổn định.
        """)

    # Chi phí vận chuyển theo trọng lượng
    with col2:
        df_weight = pd.read_sql("""
            SELECT 
                CASE 
                    WHEN weight_g < 500 THEN 'Dưới 0.5kg'
                    WHEN weight_g < 1000 THEN '0.5-1kg'
                    WHEN weight_g < 5000 THEN '1-5kg'
                    WHEN weight_g < 10000 THEN '5-10kg'
                    WHEN weight_g < 20000 THEN '10-20kg'
                    ELSE 'Trên 20kg'
                END AS nhom,
                AVG(freight_value) AS phi_tb
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.product_id
            WHERE p.weight_g IS NOT NULL
            GROUP BY nhom
            ORDER BY FIELD(nhom, 'Dưới 0.5kg', '0.5-1kg', '1-5kg', '5-10kg', '10-20kg', 'Trên 20kg')
        """, con=engine)

        fig = px.bar(df_weight, x='nhom', y='phi_tb', title="Phí vận chuyển trung bình theo trọng lượng",
                     labels={"nhom": "Trọng lượng", "phi_tb": "Phí trung bình (R$)"})
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Nhận xét:")
        st.write("""
        - **Phí tăng theo trọng lượng** → Hợp lý.
        - **Sản phẩm dưới 5kg chiếm đa số** → Olist tập trung hàng nhẹ, dễ vận chuyển.
        - **> 20kg** có phí cao → Cần tối ưu đóng gói hoặc miễn phí vận chuyển.
        """)

# ================================
# TAB 3: Hành trình (Bản đồ)
# ================================
with tab3:
    col_map, col_text = st.columns([3, 1])

    with col_map:
        df_map = pd.read_sql("""
            SELECT 
                AVG(cg.latitude) AS kh_lat, AVG(cg.longitude) AS kh_lon,
                AVG(sg.latitude) AS nb_lat, AVG(sg.longitude) AS nb_lon
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN sellers s ON oi.seller_id = s.seller_id
            LEFT JOIN geolocations cg ON c.zip_code = cg.zip_code
            LEFT JOIN geolocations sg ON s.zip_code = sg.zip_code
            WHERE cg.latitude IS NOT NULL AND sg.latitude IS NOT NULL
            GROUP BY oi.order_id
            ORDER BY RAND()
            LIMIT 3000
        """, con=engine)

        if df_map.empty:
            st.warning("Không có dữ liệu vị trí.")
        else:
            view = pdk.data_utils.compute_view(df_map[["kh_lon", "kh_lat"]])
            view.zoom = 3.5
            view.pitch = 40

            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v10",
                initial_view_state=view,
                layers=[pdk.Layer(
                    "ArcLayer",
                    data=df_map,
                    get_source_position=["nb_lon", "nb_lat"],
                    get_target_position=["kh_lon", "kh_lat"],
                    get_source_color=[0, 255, 0, 120],
                    get_target_color=[255, 50, 50, 120],
                    line_width_min_pixels=1.2,
                    pickable=True
                )]
            ))

    with col_text:
        st.markdown("#### Nhận xét:")
        st.write("""
        - **Miền Nam & Đông Nam Brazil** là trung tâm → tập trung người bán & khách hàng.
        - **Đường đi từ xanh (người bán) → đỏ (khách)** → rõ ràng, trực quan.
        - **Miền Bắc ít hoạt động** → Cơ hội mở rộng thị trường.
        """)
        st.caption("Mẫu ngẫu nhiên 3.000 đơn hàng")