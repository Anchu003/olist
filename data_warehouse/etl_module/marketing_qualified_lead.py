import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:


    df = pd.read_csv(
        filepath_or_buffer=data_path,
        usecols=["mql_id", "first_contact_date", "origin"],
        parse_dates=["first_contact_date"],
    )


    df["origin"].fillna("other", inplace=True)


    with engine.connect() as conn:
       
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`marketing_qualified_leads` (
                `mql_id` VARCHAR(45) NOT NULL,
                `first_contact_date` DATE NOT NULL,
                `origin` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`mql_id`)
                );
                """
        )

 
    df.to_sql(
        name="marketing_qualified_leads",
        con=engine,
        index=False,
        if_exists="append",
    )
