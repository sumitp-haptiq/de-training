from prefect import flow, task
from prefect.logging import get_run_logger
import requests
import pandas as pd
from sqlalchemy import create_engine

@task
def extract():
    logger = get_run_logger()
    logger.info("Extracting data from API")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    logger.info("Extracted users data from API")
    return df

@task
def transform(df):
    logger = get_run_logger()
    logger.info("Transforming data")
    df = df.drop(columns=['address', 'company'])
    logger.info("Transformed data")
    return df

@task
def load_to_postgres(df):
    logger = get_run_logger()
    logger.info("Loading data to Postgres")
    engine = create_engine("postgresql://dbt_user:dbt_pass@db:5432/dbt_demo")
    df.to_sql("users_api", engine, if_exists="replace", index=False)
    logger.info(f"Loaded {len(df)} rows into table 'users_api'")
    logger.info("Loaded data to Postgres")

@flow
def main():
    logger = get_run_logger()
    logger.info("Starting flow")
    df = extract()
    df = transform(df)
    load_to_postgres(df)
    logger.info("Flow completed successfully")

if __name__ == "__main__":
    main()
