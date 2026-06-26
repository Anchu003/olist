import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(
        filepath_or_buffer=data_path, usecols=["seller_id", "seller_zip_code_prefix"]
    )


    df.rename(columns={"seller_zip_code_prefix": "zip_code"}, inplace=True)


    with engine.connect() as conn:
 
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`sellers` (
                `seller_id` VARCHAR(45) NOT NULL,
                `zip_code` INT NOT NULL,
                PRIMARY KEY (`seller_id`),
                FOREIGN KEY (`zip_code`) REFERENCES `data_warehouse_olist`.`geolocations` (`zip_code`)
                );
                """
        )


    df.to_sql(
        name="sellers",
        con=engine,
        index=False,
        if_exists="append",
    )
