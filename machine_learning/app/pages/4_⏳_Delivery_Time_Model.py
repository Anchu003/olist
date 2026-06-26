import streamlit as st
import pandas as pd
import pickle as pkl
import sqlalchemy as sql
from datetime import date, datetime
from xgboost.sklearn import XGBRegressor
import pydeck as pdk

st.set_page_config(page_title="Dự báo thời gian giao hàng", page_icon="🚚", layout="wide")
st.header("📦 Mô hình dự báo thời gian giao hàng")

# ====== KẾT NỐI DATABASE ======
engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)
DF = pd.read_sql(
    "SELECT zip_code, latitude, longitude FROM data_warehouse_olist.geolocations;",
    con=engine,
)

# ====== DỮ LIỆU ĐẦU VÀO ======
zip_vendedor = st.number_input("🏪 Mã bưu chính (ZIP code) của người bán", min_value=1001, value=1001)
filtro_vendedor = DF["zip_code"] == zip_vendedor
lat_vend = DF[filtro_vendedor]["latitude"].values[0]
long_vend = DF[filtro_vendedor]["longitude"].values[0]

zip_comprador = st.number_input("📍 Mã bưu chính (ZIP code) của người mua", min_value=1001, value=1001)
filtro_comprador = DF["zip_code"] == zip_comprador
lat_comp = DF[filtro_comprador]["latitude"].values[0]
long_comp = DF[filtro_comprador]["longitude"].values[0]

start_date = date(2017, 12, 31)
min_date = date(2016, 6, 1)
max_date = date(2018, 12, 31)
dia_compra = st.date_input("🗓️ Ngày khách hàng thực hiện mua hàng", value=start_date, min_value=min_date, max_value=max_date)
fecha_completa = datetime.combine(dia_compra, datetime.min.time())
timestamp = fecha_completa.timestamp()

flete = st.number_input("💰 Phí vận chuyển (R$)")
peso = st.number_input("⚖️ Trọng lượng sản phẩm (kg)", value=1)

# ====== TẠO DATAFRAME CHO DỰ ĐOÁN ======
df_input = pd.DataFrame([[lat_comp, long_comp, lat_vend, long_vend, timestamp, flete, peso]],
                        columns=["lat_comp", "long_comp", "lat_vend", "long_vend", "dia_compra", "flete", "peso"])

def dias_espera(datos):
    modelo = pd.read_pickle("models/dias_espera.pkl")
    pred = modelo.predict(datos)
    return pred[0]

btn = st.button("🔍 Dự báo số ngày giao hàng")

if btn:
    dias = int(dias_espera(df_input))
    st.success(f"🕒 Thời gian giao hàng dự kiến là **{dias} ngày**.")

    # ====== DỮ LIỆU CHO BẢN ĐỒ ======
    # Marker cho người bán và người mua
    markers = pd.DataFrame([
        {"lat": lat_vend, "lon": long_vend, "name": f"Người bán (ZIP {zip_vendedor})", "color": [0, 128, 255]},
        {"lat": lat_comp, "lon": long_comp, "name": f"Người mua (ZIP {zip_comprador})", "color": [255, 0, 0]},
    ])

    # Line nối từ người bán đến người mua
    route = pd.DataFrame([{
        "start_lat": lat_vend, "start_lon": long_vend,
        "end_lat": lat_comp, "end_lon": long_comp
    }])

    # Layer đường đi
    line_layer = pdk.Layer(
        "LineLayer",
        data=route,
        get_source_position=["start_lon", "start_lat"],
        get_target_position=["end_lon", "end_lat"],
        get_color=[0, 255, 0],
        get_width=5
    )

    # Layer marker
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=markers,
        get_position=["lon", "lat"],
        get_fill_color="color",
        get_radius=1000,  
        pickable=True,
        tooltip=True
    )

    # View trung tâm giữa hai điểm
    view_state = pdk.ViewState(
        latitude=(lat_vend + lat_comp)/2,
        longitude=(long_vend + long_comp)/2,
        zoom=5
    )

    deck = pdk.Deck(layers=[line_layer, scatter_layer], initial_view_state=view_state)
    st.pydeck_chart(deck)
