import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:
   
    df = pd.read_csv(
        filepath_or_buffer=data_path,
        usecols=[
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
        ],
    )


    df.rename(
        columns={
            "review_score": "score",
            "review_comment_title": "comment_title",
            "review_comment_message": "comment_message",
        },
        inplace=True,
    )


    with engine.connect() as conn:
   
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`order_reviews` (
                `review_id` VARCHAR(45) NOT NULL,
                `order_id` VARCHAR(45) NOT NULL,
                `score` INT NOT NULL,
                `comment_title` VARCHAR(55),
                `comment_message` VARCHAR(255),
                FOREIGN KEY (`order_id`) REFERENCES `data_warehouse_olist`.`orders` (`order_id`)
                );
                """
        )


    df.to_sql(
        name="order_reviews",
        con=engine,
        index=False,
        if_exists="append",
    )
