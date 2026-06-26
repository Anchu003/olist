import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hệ thống gợi ý sản phẩm", page_icon="🛒", layout="wide")
st.title("🔍 Mô hình gợi ý sản phẩm")

tab1, tab2 = st.tabs(["Sản phẩm - Sản phẩm", "Người dùng - Sản phẩm"])

# ============================= TAB 1: PRODUCT-PRODUCT =============================
with tab1:
    st.header("**Bộ lọc theo nội dung** (sản phẩm - sản phẩm)")

    with st.expander("Cách hoạt động của mô hình"):
        st.write(
            """
            Mô hình gợi ý sản phẩm tương tự dựa trên đặc điểm sản phẩm (content-based).  
            Hữu ích khi dữ liệu người dùng chưa nhiều (cold start).
            """
        )

    st.write("Bạn có thể:")

    # Load dữ liệu sản phẩm
    df_products = pd.read_pickle("models/recomendacion_producto.pkl")
    df_products_unique = df_products[["product_id", "category_name"]].drop_duplicates()

    # Tạo mapping: nhãn dễ đọc -> product_id đầy đủ
    product_map = {f"{row['category_name']} ({row['product_id'][:6]}...{row['product_id'][-6:]})": row['product_id']
                   for _, row in df_products_unique.iterrows()}

    # Selectbox với nhãn dễ đọc
    product_label = st.selectbox("Chọn một sản phẩm:", list(product_map.keys()))
    selected_product_id = product_map[product_label]

    st.write("hoặc")
    product1 = st.text_input("Nhập mã sản phẩm:")

    btn = st.button("**Gợi ý sản phẩm**")

    def recommend_products(product_id):
        df_ml = pd.read_pickle("models/recomendacion_producto.pkl")
        filtro_aux = df_ml["product_id"] == product_id
        if filtro_aux.sum() == 0:
            return pd.DataFrame()  # trả về bảng rỗng nếu không tìm thấy
        categoria = df_ml[filtro_aux]["category_name"]
        group = df_ml[filtro_aux]["group"]
        filtro = (
            (df_ml["group"] == group.values[0])
            & (df_ml["category_name"] == categoria.values[0])
            & (df_ml["product_id"] != product_id)
        )
        df = df_ml[filtro].sort_values(by="ventas_producto", ascending=False)
        return df.head(3)

    if btn:
        try:
            if product1 != "":
                result = recommend_products(product1)
            else:
                result = recommend_products(selected_product_id)
            if result.empty:
                st.error("Mã sản phẩm không hợp lệ. Vui lòng thử lại.", icon="🚨")
            else:
                st.dataframe(result)
        except Exception as e:
            st.error(f"Lỗi xảy ra: {e}", icon="🚨")

# ============================= TAB 2: USER-PRODUCT =============================
with tab2:
    st.header("**Bộ lọc cộng tác** (người dùng - sản phẩm)")

    with st.expander("Cách hoạt động của mô hình"):
        st.write(
            """
            Gợi ý sản phẩm dựa trên lịch sử và hành vi người dùng (collaborative filtering).  
            Hiệu quả khi có cơ sở dữ liệu người dùng phong phú.
            """
        )

    st.write("Bạn có thể:")

    # Load dữ liệu người dùng
    top_five_ranked = pd.read_pickle("models/recomendacion_colaborativa.pkl")
    users_unique = top_five_ranked["unique_id"].drop_duplicates()

    # Mapping nhãn -> user_id đầy đủ
    user_map = {f"Người dùng {i+1} ({uid[:6]}...{uid[-6:]})": uid
                for i, uid in enumerate(users_unique)}

    usuario_label = st.selectbox("Chọn một người dùng:", list(user_map.keys()))
    selected_user_id = user_map[usuario_label]

    st.write("hoặc")
    usuario1 = st.text_input("Nhập ID người dùng:")

    btn2 = st.button("**Dự đoán sản phẩm phù hợp**")

    def recommend_products2(usuario):
        df = top_five_ranked.loc[top_five_ranked["unique_id"] == usuario]
        return df

    if btn2:
        try:
            if usuario1 != "":
                result = recommend_products2(usuario1)
            else:
                result = recommend_products2(selected_user_id)
            if result.empty:
                st.error("ID người dùng không hợp lệ. Vui lòng thử lại.", icon="🚨")
            else:
                st.dataframe(result)
        except Exception as e:
            st.error(f"Lỗi xảy ra: {e}", icon="🚨")
