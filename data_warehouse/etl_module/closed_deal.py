import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:
    


    df = pd.read_csv(
        filepath_or_buffer=data_path,
        usecols=[
            "mql_id",
            "won_date",
            "business_segment",
            "lead_type",
            "business_type",
        ],
        parse_dates=["won_date"],
    )


    df["business_segment"].fillna(value="other", inplace=True)
    df["lead_type"].fillna(value="other", inplace=True)
    df["business_type"].fillna(value="other", inplace=True)


    with engine.connect() as conn:
        
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`closed_deals` (
                `mql_id` VARCHAR(45) NOT NULL,
                `won_date` DATE NOT NULL,
                `business_segment` VARCHAR(45) NOT NULL,
                `lead_type` VARCHAR(45) NOT NULL,
                `business_type` VARCHAR(45) NOT NULL,
                FOREIGN KEY (`mql_id`) REFERENCES `data_warehouse_olist`.`marketing_qualified_leads` (`mql_id`)
                );
                """
        )

 
    df.to_sql(
        name="closed_deals",
        con=engine,
        index=False,
        if_exists="append",
    )
