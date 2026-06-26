import pandas as pd
import sqlalchemy as sql


def etl(
    data_path: str,
    zip_code_data_path: str,
    customer_data_path: str,
    seller_data_path: str,
    engine: sql.engine.Engine,
) -> None:
 


    df_geolocations = pd.read_csv(
        filepath_or_buffer=data_path,
        usecols=[
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_state",
        ],
    )


    df_zip_codes = pd.read_csv(filepath_or_buffer=zip_code_data_path)


    df_zip_codes["zip_code"] = df_zip_codes["zip_code"].str.split("-", expand=True)[0]
    df_zip_codes["zip_code"] = pd.to_numeric(df_zip_codes["zip_code"])


    df_customers = pd.read_csv(
        filepath_or_buffer=customer_data_path,
        usecols=["customer_zip_code_prefix", "customer_state"],
    )

 
    df_customers_missing = df_customers[
        ~df_customers["customer_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_customers

   
    df_sellers = pd.read_csv(
        filepath_or_buffer=seller_data_path,
        usecols=["seller_zip_code_prefix", "seller_state"],
    )

   
    df_sellers_missing = df_sellers[
        ~df_sellers["seller_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_sellers


    df_geolocations = pd.concat(
        objs=[df_geolocations, df_customers_missing, df_sellers_missing]
    )


    filter_ = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["customer_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_, "customer_zip_code_prefix"
    ]
    df_geolocations.loc[filter_, "geolocation_state"] = df_geolocations.loc[
        filter_, "customer_state"
    ]

 
    filter_ = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["seller_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_, "seller_zip_code_prefix"
    ]
    df_geolocations.loc[filter_, "geolocation_state"] = df_geolocations.loc[
        filter_, "seller_state"
    ]


    df_geolocations.drop(
        columns=[
            "customer_zip_code_prefix",
            "seller_zip_code_prefix",
            "customer_state",
            "seller_state",
        ],
        inplace=True,
    )


    df_geolocations["geolocation_zip_code_prefix"] = df_geolocations[
        "geolocation_zip_code_prefix"
    ].astype("int64")


    df_zip_codes.sort_values(by="zip_code", inplace=True)
    df_geolocations.sort_values(by="geolocation_zip_code_prefix", inplace=True)


    df = pd.merge_asof(
        left=df_geolocations,
        right=df_zip_codes,
        left_on="geolocation_zip_code_prefix",
        right_on="zip_code",
        direction="backward",
    )

    del df_geolocations
    del df_zip_codes


    df.drop(
        columns=[
            "zip_code",
        ],
        inplace=True,
    )

    # Reemplazarla valores faltantes en las columnas de latitud y longitud
    filter_ = df["geolocation_lat"].isna() & df["geolocation_lng"].isna()

    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    # Calcula la variación porcentual de los valores originales con los de referencia
    df["latitude_%"] = (
        abs((df["geolocation_lat"] - df["latitude"]) / df["latitude"]) * 100
    )
    df["longitude_%"] = (
        abs((df["geolocation_lng"] - df["longitude"]) / df["longitude"]) * 100
    )

    # Reemplaza los valores que difieren mas de un 1% con los valores de referencia
    filter_ = df["latitude_%"] > 1
    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]

    filter_ = df["longitude_%"] > 1
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    # Eliminar columnas innecesarias
    df.drop(
        columns=["latitude", "longitude", "latitude_%", "longitude_%"], inplace=True
    )

    # Agrupa por zip_code y saca el promedio de la latitud y la longitud
    df = (
        df.groupby("geolocation_zip_code_prefix")
        .aggregate(
            func={
                "geolocation_lat": "mean",
                "geolocation_lng": "mean",
                "geolocation_state": "first",
                "city_name": "first",
            }
        )
        .reset_index()
    )

    # Renombra las columnas
    df.rename(
        columns={
            "geolocation_lat": "latitude",
            "geolocation_lng": "longitude",
            "geolocation_state": "state",
            "city_name": "city",
            "geolocation_zip_code_prefix": "zip_code",
        },
        inplace=True,
    )

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "geolocations" si no existe
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`geolocations` (
                `zip_code` INT NOT NULL,
                `city` VARCHAR(45) NOT NULL,
                `state` VARCHAR(45) NOT NULL,
                `latitude` DECIMAL(7,5) NOT NULL,
                `longitude` DECIMAL(7,5) NOT NULL,
                PRIMARY KEY (`zip_code`)
                );
            """
        )

    # Cargar los datos en la tabla "geolocations"
    df.to_sql(
        name="geolocations",
        con=engine,
        index=False,
        if_exists="append",
    )
