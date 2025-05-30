from google.cloud import bigquery
from ..config import PROJECT_ID, DATASET_ID
from .logger import get_logger

logger = get_logger("bq_writer")

def write_to_bigquery(table_name: str, rows: list):
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    try:
        errors = client.insert_rows_json(table_id, rows)
        if errors:
            logger.error(f"BigQuery insert errors: {errors}")
        else:
            logger.info(f"Inserted {len(rows)} rows into {table_id}")

    except Exception as e:
        logger.error(f"Exception during BigQuery insert: {e}")