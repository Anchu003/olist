import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:



    df = pd.read_csv(
        filepath_or_buffer=data_path,
        date_parser=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )


    df.rename(
        columns={
            "order_status": "status",
            "order_purchase_timestamp": "purchase_timestamp",
            "order_approved_at": "approved_at",
            "order_delivered_carrier_date": "delivered_carrier_date",
            "order_delivered_customer_date": "delivered_customer_date",
            "order_estimated_delivery_date": "estimated_delivery_date",
        },
        inplace=True,
    )

    with engine.connect() as conn:

        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`orders` (
                `order_id` VARCHAR(45) NOT NULL,
                `customer_id` VARCHAR(45) NOT NULL,
                `status` VARCHAR(45) NOT NULL,
                `purchase_timestamp` DATE NOT NULL,
                `approved_at` DATE,
                `delivered_carrier_date` DATE,
                `delivered_customer_date` DATE,
                `estimated_delivery_date` DATE,
                PRIMARY KEY (`order_id`),
                FOREIGN KEY (`customer_id`) REFERENCES `data_warehouse_olist`.`customers` (`customer_id`)
                );
                """
        )


    df.to_sql(
        name="orders",
        con=engine,
        index=False,
        if_exists="append",
    )
