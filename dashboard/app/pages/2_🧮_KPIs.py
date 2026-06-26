import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="KPIs", page_icon="🧮", layout="wide")

# ====== GIAO DIỆN ======
st.sidebar.header("Chỉ số hiệu suất (KPIs)")
st.title(":mag_right: Trực quan hóa dữ liệu KPIs")
st.subheader("Key Performance Indicator - (Chỉ số hiệu suất chính)")

st.sidebar.write(
    """Công cụ dùng để đo lường hiệu suất và tiến độ hoạt động của Olist
    so với các mục tiêu chiến lược."""
)

# ====== KẾT NỐI DATABASE ======
_mysql_user = os.getenv("MYSQL_USER", "root")
_mysql_password = os.getenv("MYSQL_ROOT_PASSWORD")
_mysql_host = os.getenv("MYSQL_HOST", "mysql")
_mysql_port = os.getenv("MYSQL_PORT", "3306")
_mysql_db = os.getenv("MYSQL_DB", "data_warehouse_olist")

engine = create_engine(
    f"mysql+pymysql://{_mysql_user}:{_mysql_password}@{_mysql_host}:{_mysql_port}/{_mysql_db}?charset=utf8mb4"
)

# ====== KPI 1️⃣ - Biến động phần trăm khối lượng bán hàng ======
st.markdown("---")
st.markdown("#### Biến động phần trăm khối lượng bán hàng (VVV)")
st.text("Mục tiêu: Đánh giá thay đổi phần trăm doanh số theo tháng")
st.text("Tần suất đánh giá: Hàng tháng")
st.text("Giá trị mục tiêu: 10%")

kpi_vvv = pd.read_sql(
    """
        SELECT date(CONCAT(CAST(s.año AS UNSIGNED), '/', CAST(s.mes AS UNSIGNED), "/1")) AS fecha, sum(s.total) AS total
        FROM (
            SELECT avg(year(o.purchase_timestamp)) AS año, avg(month(o.purchase_timestamp)) AS mes, sum(i.price) AS total
            FROM orders AS o
            RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
            WHERE o.status != "canceled" AND o.status != "unavailable"
            GROUP BY o.order_id
        ) AS s
        GROUP BY s.año, s.mes
        HAVING s.año = 2017
        ORDER BY s.año, s.mes DESC;
    """,
    con=engine,
)

kpi_vvv["diff"] = kpi_vvv["total"].pct_change(periods=-1)

left_column, right_column = st.columns([1, 1])
with left_column:
    st.metric(
        label="Tổng doanh số (R$)",
        value=int(kpi_vvv.loc[0, "total"]),
        delta=int(kpi_vvv.loc[0, "total"] - kpi_vvv.loc[1, "total"]),
    )
with right_column:
    st.metric(
        label="Biến động phần trăm",
        value=format(kpi_vvv.loc[0, "diff"], ".2%"),
        delta=format(kpi_vvv.loc[0, "diff"] - kpi_vvv.loc[1, "diff"], ".2%"),
    )

# ====== KPI 2️⃣ - Điểm hài lòng khách hàng (PN) ======
st.markdown("---")
st.markdown("#### Điểm hài lòng khách hàng (PN)")
st.text("Mục tiêu: Đo lường mức độ hài lòng của khách hàng")
st.text("Tần suất đánh giá: Hàng quý")
st.text("Giá trị mục tiêu: 60%")

kpi_pn = pd.read_sql(
    """
    SELECT
        year(orders.delivered_customer_date) AS año,
        month(orders.delivered_customer_date) AS mes,
        SUM(CASE WHEN score > 3 THEN 1 ELSE 0 END) AS reviews_positivas,
        SUM(CASE WHEN score <= 3 THEN 1 ELSE 0 END) AS reviews_negativas,
        COUNT(*) AS total_reviews
    FROM order_reviews
    LEFT JOIN orders ON (order_reviews.order_id = orders.order_id)
    WHERE year(orders.delivered_customer_date) = 2017
    GROUP BY year(orders.delivered_customer_date), month(orders.delivered_customer_date)
    ORDER BY year(orders.delivered_customer_date), month(orders.delivered_customer_date) DESC
    LIMIT 2;
    """,
    con=engine,
)

pct_act_rp = kpi_pn.loc[0, "reviews_positivas"] / kpi_pn.loc[0, "total_reviews"]
pct_ant_rp = kpi_pn.loc[1, "reviews_positivas"] / kpi_pn.loc[1, "total_reviews"]

pct_act_rn = kpi_pn.loc[0, "reviews_negativas"] / kpi_pn.loc[0, "total_reviews"]
pct_ant_rn = kpi_pn.loc[1, "reviews_negativas"] / kpi_pn.loc[1, "total_reviews"]

pct_act_pn = pct_act_rp - pct_act_rn
pct_ant_pn = pct_ant_rp - pct_ant_rn

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.metric(
        label="Tỷ lệ đánh giá tích cực",
        value=format(pct_act_rp, ".2%"),
        delta=format(pct_act_rp - pct_ant_rp, ".2%"),
    )
with middle_column:
    st.metric(
        label="Tỷ lệ đánh giá tiêu cực",
        value=format(pct_act_rn, ".2%"),
        delta=format(pct_act_rn - pct_ant_rn, ".2%"),
        delta_color="inverse",
    )
with right_column:
    st.metric(
        label="Điểm hài lòng ròng (PN)",
        value=format(pct_act_pn, ".2%"),
        delta=format(pct_act_pn - pct_ant_pn, ".2%"),
    )

# ====== KPI 3️⃣ - Độ trung thành khách hàng (FC) ======
st.markdown("---")
st.markdown("#### Độ trung thành khách hàng (FC)")
st.text("Mục tiêu: Đo tỷ lệ khách hàng quay lại mua hàng")
st.text("Tần suất đánh giá: Hàng quý")
st.text("Giá trị mục tiêu: 5%")

kpi_fc = pd.read_sql(
    sql=""" 
    WITH current_quarter AS ( SELECT 2017 AS year, 4 AS quarter)
    SELECT 
        (SELECT year FROM current_quarter) AS año,
        (SELECT quarter FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter FROM current_quarter)
    AND customers.unique_id IN (
        SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
        WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
        AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable"
    UNION 
    SELECT 
        (SELECT year FROM current_quarter) AS año,
        (SELECT quarter - 1 FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
    AND customers.unique_id IN (
        SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
        WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
        AND quarter(orders.purchase_timestamp) = (SELECT quarter - 2 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable";
    """,
    con=engine,
)

kpi_fc_total = pd.read_sql(
    sql=""" 
        SELECT 
            year(orders.purchase_timestamp) AS año, 
            quarter(orders.purchase_timestamp) AS mes, 
            count(DISTINCT customers.unique_id) AS cantidad_total_clientes
        FROM orders
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
        WHERE  year(orders.purchase_timestamp) = 2017
        AND orders.status != "canceled" AND orders.status != "unavailable"
        GROUP BY año, mes
        ORDER BY año, mes DESC
        LIMIT 2;
    """,
    con=engine,
)

pct_act_fc = (
    kpi_fc.loc[0, "clientes_fieles"] / kpi_fc_total.loc[0, "cantidad_total_clientes"]
)
pct_ant_fc = (
    kpi_fc.loc[1, "clientes_fieles"] / kpi_fc_total.loc[1, "cantidad_total_clientes"]
)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.metric(
        label="Số khách hàng trung thành",
        value=int(kpi_fc.loc[0, "clientes_fieles"]),
        delta=int(kpi_fc.loc[0, "clientes_fieles"] - kpi_fc.loc[1, "clientes_fieles"]),
    )
with middle_column:
    st.metric(
        label="Tổng số khách hàng",
        value=int(kpi_fc_total.loc[0, "cantidad_total_clientes"]),
        delta=int(
            kpi_fc_total.loc[0, "cantidad_total_clientes"]
            - kpi_fc_total.loc[1, "cantidad_total_clientes"]
        ),
    )
with right_column:
    st.metric(
        label="Tỷ lệ trung thành khách hàng",
        value=format(pct_act_fc, ".2%"),
        delta=format(pct_act_fc - pct_ant_fc, ".2%"),
    )

# ====== KPI 4️⃣ - Tỷ lệ chuyển đổi (TC) ======
st.markdown("---")
st.markdown("#### Tỷ lệ chuyển đổi (TC)")
st.text("Mục tiêu: Đo số lượng khách hàng tiềm năng trở thành khách hàng thực tế")
st.text("Tần suất đánh giá: Hàng quý")
st.text("Giá trị mục tiêu: 15%")

kpi_tc = pd.read_sql(
    """
    SELECT 
        max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 4
    UNION
    SELECT 
        max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 3;
    """,
    con=engine,
)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.metric(
        label="Số khách hàng tiềm năng",
        value=int(kpi_tc.loc[0, "cantidad_interesados"]),
        delta=int(
            kpi_tc.loc[0, "cantidad_interesados"]
            - kpi_tc.loc[1, "cantidad_interesados"]
        ),
    )
with middle_column:
    st.metric(
        label="Số khách hàng đã chuyển đổi",
        value=int(kpi_tc.loc[0, "cantidad_convertidos"]),
        delta=int(
            kpi_tc.loc[0, "cantidad_convertidos"]
            - kpi_tc.loc[1, "cantidad_convertidos"]
        ),
    )
with right_column:
    st.metric(
        label="Tỷ lệ chuyển đổi",
        value=format(kpi_tc.loc[0, "tasa_conversion"], ".2%"),
        delta=format(
            kpi_tc.loc[0, "tasa_conversion"] - kpi_tc.loc[1, "tasa_conversion"], ".2%"
        ),
    )

# ====== KPI 5️⃣ - Tỷ lệ giao hàng đúng hạn (PE) ======
st.markdown("---")
st.markdown("#### Tỷ lệ giao hàng đúng hạn (PE)")
st.text("Mục tiêu: Đo tỷ lệ đơn hàng được giao đúng thời gian dự kiến")
st.text("Tần suất đánh giá: Hàng tháng")
st.text("Giá trị mục tiêu: 95%")

kpi_pe = pd.read_sql(
    """
    SELECT 
        year(ord.fecha) AS año,
        month(ord.fecha) AS mes,
        sum(ord.a_tiempo) AS cantidad_a_tiempo,
        count(*) AS cantidad_total,
        sum(ord.a_tiempo)/count(*) AS puntualidad
    FROM (
        SELECT
            purchase_timestamp AS fecha,
            (CASE WHEN datediff(estimated_delivery_date, delivered_customer_date) >= 0 THEN 1 ELSE 0 END) AS a_tiempo
        FROM orders
        WHERE status = "delivered" AND year(purchase_timestamp) = 2017
    ) AS ord
    GROUP BY año, mes
    ORDER BY año, mes DESC
    LIMIT 2;
    """,
    con=engine,
)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.metric(
        label="Tổng số đơn hàng",
        value=int(kpi_pe.loc[0, "cantidad_total"]),
        delta=int(kpi_pe.loc[0, "cantidad_total"] - kpi_pe.loc[1, "cantidad_total"]),
    )
with middle_column:
    st.metric(
        label="Số đơn giao đúng hạn",
        value=int(kpi_pe.loc[0, "cantidad_a_tiempo"]),
        delta=int(
            kpi_pe.loc[0, "cantidad_a_tiempo"] - kpi_pe.loc[1, "cantidad_a_tiempo"]
        ),
    )
with right_column:
    st.metric(
        label="Tỷ lệ giao hàng đúng hạn",
        value=format(kpi_pe.loc[0, "puntualidad"], ".2%"),
        delta=format(
            kpi_pe.loc[0, "puntualidad"] - kpi_pe.loc[1, "puntualidad"], ".2%"
        ),
    )

# ====== KPI 6️⃣ - Thời gian xử lý đơn hàng trung bình (TTP) ======
st.markdown("---")
st.markdown("#### Thời gian xử lý đơn hàng trung bình (TTP)")
st.text("Mục tiêu: Đánh giá và tối ưu thời gian từ khi mua đến khi giao hàng")
st.text("Tần suất đánh giá: Hàng tháng")
st.text("Giá trị mục tiêu: 8 ngày")

kpi_ttp = pd.read_sql(
    sql="""
        SELECT 
            year(purchase_timestamp) AS año,
            month(purchase_timestamp) AS mes,
            avg(datediff(delivered_customer_date,purchase_timestamp)) AS tiempo_prom
        FROM orders
        WHERE year(purchase_timestamp) = 2017 AND status = "delivered"
        GROUP BY año, mes
        ORDER BY año, mes DESC;
    """,
    con=engine,
)

graf_col, kpi_col = st.columns([2, 1])
with graf_col:
    fig = px.area(
        data_frame=kpi_ttp,
        x="mes",
        y="tiempo_prom",
        title="Biểu đồ thời gian giao hàng trung bình theo tháng",
        range_y=[6, 16],
        labels={"mes": "Tháng", "tiempo_prom": "Thời gian trung bình (ngày)"},
    )
    st.plotly_chart(figure_or_data=fig)
with kpi_col:
    st.metric(
        label="Thời gian xử lý trung bình (ngày)",
        value=round(float(kpi_ttp.loc[0, "tiempo_prom"]), 2),
        delta=round(
            float(kpi_ttp.loc[0, "tiempo_prom"] - kpi_ttp.loc[1, "tiempo_prom"]), 2
        ),
        delta_color="inverse",
    )

st.markdown("---")
