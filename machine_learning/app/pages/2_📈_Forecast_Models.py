import streamlit as st
import pandas as pd
import sqlalchemy as sql
import pickle as pkl
import datetime as dt
import plotly.express as px

# ===================== GIAO DIỆN =====================
st.set_page_config(page_title="Dự báo doanh số Olist", page_icon="📈", layout="wide")
st.title("📊 Dự báo doanh số bán hàng")
st.write("Ứng dụng các mô hình **ARIMA** và **Prophet** để dự đoán xu hướng doanh số trong tương lai.")

# ===================== KẾT NỐI DATABASE =====================
engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

# ===================== NẠP MÔ HÌNH =====================
with open("models/total_model.pkl", "rb") as f:
    total_model = pkl.load(f)

with open("models/model_prophet.pkl", "rb") as f:
    model_prophet = pkl.load(f)

# ===================== DỮ LIỆU LỊCH SỬ =====================
df_history = pd.read_sql(
    """
    SELECT
        o.purchase_timestamp AS time,
        oi.price AS sales
    FROM orders AS o 
    LEFT JOIN order_items AS oi ON (o.order_id = oi.order_id)
    """,
    con=engine,
)

df_history.dropna(inplace=True)
df_history["time"] = pd.to_datetime(df_history["time"])
df_history.set_index("time", inplace=True)

# Tổng hợp dữ liệu theo tuần
df_history_w = df_history["sales"].resample("W").sum().reset_index()
df_history_w["type"] = "Dữ liệu thực tế"

# Danh sách tuần tương lai để chọn dự báo
future = [dt.date(2018, 9, 9) + dt.timedelta(weeks=i) for i in range(1, 40)]

# ===================== TABs =====================
tab1, tab2 = st.tabs(["ARIMA", "Prophet"])

# ----------------- TAB ARIMA -----------------
with tab1:
    st.subheader("🔹 Dự báo doanh số bằng mô hình ARIMA")

    date = st.select_slider("Chọn ngày dự báo:", options=future, key="arima")

    try:
        forecast_arima = total_model.predict(start=87, end=date, dynamic=True)
        forecast_arima = forecast_arima.reset_index()
        forecast_arima.rename(columns={"index": "time", "predicted_mean": "sales"}, inplace=True)
        forecast_arima["type"] = "Dự báo (ARIMA)"

        df_plot = pd.concat([df_history_w, forecast_arima.iloc[1:]], axis=0, ignore_index=True)

        fig = px.line(
            df_plot,
            x="time",
            y="sales",
            color="type",
            title="Biểu đồ dự báo doanh số - Mô hình ARIMA",
            labels={"time": "Thời gian", "sales": "Doanh số (R$)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Lỗi khi dự báo bằng ARIMA: {e}")

# ----------------- TAB 2PROPHET -----------------
with tab2:
    st.subheader("🔹 Dự báo doanh số bằng mô hình Prophet")

    date = st.select_slider("Chọn ngày dự báo:", options=future, key="prophet")
    weeks = future.index(date)

    try:
        future_df = model_prophet.make_future_dataframe(periods=weeks + 23, freq="W")
        forecast_prophet = model_prophet.predict(future_df)

        forecast_prophet = forecast_prophet[["ds", "yhat"]]
        forecast_prophet.rename(columns={"ds": "time", "yhat": "sales"}, inplace=True)
        forecast_prophet["type"] = "Dự báo (Prophet)"

        df_plot = pd.concat([df_history_w, forecast_prophet.iloc[88:]], axis=0, ignore_index=True)

        fig = px.line(
            df_plot,
            x="time",
            y="sales",
            color="type",
            title="Biểu đồ dự báo doanh số - Mô hình Prophet",
            labels={"time": "Thời gian", "sales": "Doanh số (R$)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Lỗi khi dự báo bằng Prophet: {e}")
